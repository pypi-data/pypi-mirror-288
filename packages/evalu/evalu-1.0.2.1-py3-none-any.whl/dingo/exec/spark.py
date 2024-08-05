from typing import Callable, List, Generator, Union, Any, Dict
import os
import time
# import orjson

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, Row, DataFrame
from pyspark.sql.functions import explode, count, col, format_number
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, ArrayType
from pyspark.sql.functions import col, regexp_replace

from dingo.exec.base import Executor
from dingo.data import dataset_map, datasource_map, Dataset
from dingo.config import GlobalConfig
from dingo.model import Model
from dingo.model.modelres import ModelRes
from dingo.model.rule.base import BaseRule
from dingo.io import RawInputModel, InputModel, SummaryModel
from dingo.utils import log

QUALITY_MAP = Model.rule_metric_type_map


@Executor.register('spark')
class SparkExecutor(Executor):
    """
    Spark executor
    """

    def __init__(self, raw_input: RawInputModel,
                 spark: SparkSession = None,
                 spark_conf: SparkConf = None):
        # eval param
        self.model_type = None
        self.model_name = None
        self.model = None
        self.error_info = None
        self.error_count = {}
        self.dataset_id = time.strftime('%Y%m%d_%H%M%S', time.localtime())

        # init param
        self.raw_input = raw_input
        self.spark = spark
        self.spark_conf = spark_conf

    def load_data(self) -> Generator[Any, None, None]:
        """
        Reads data from given path. Returns generator of raw data.

        **Run in executor.**

        Returns:
            Generator[Any, None, None]: Generator of raw data.
        """
        new_raw_input = self.raw_input
        dataset_type = "spark"
        source = self.raw_input.datasource if self.raw_input.datasource != "" else self.raw_input.dataset
        dataset_cls = dataset_map[dataset_type]
        dataset: Dataset = dataset_cls(source=datasource_map[source](raw_input=new_raw_input))
        self.dataset_id = dataset.digest
        return dataset.get_data()

    def execute(self):
        current_time = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        print("============= Init pyspark =============")
        if self.spark is not None:
            spark = self.spark
            sc = spark.sparkContext
        else:
            sc = SparkContext("spark://127.0.0.1:7077", f"Dingo_Data_Evaluation_{current_time}")
            spark = SparkSession(sc)
        print("============== Init Done ===============")

        # Model init
        if len(self.raw_input.eval_models) != 1:
            raise RuntimeError("Len of Spark evaluation model must be 1.")
        self.get_model_list(self.raw_input.eval_models[0])

        # Exec Eval
        data_rdd = sc.parallelize(self.load_data(), 3)

        record_list = data_rdd.map(self.evaluate)
        record_list.cache()

        # calculate count
        record = record_list.reduce(reduce_records)
        record['input_model'] = self.model_name
        record['input_path'] = self.raw_input.input_path
        record['output_path'] = self.raw_input.output_path
        record['num_good'] = record['total'] - record['num_bad']
        record['score'] = round(record['num_good'] / record['total'] * 100, 2)

        error_info = record_list.map(map_record_to_error_info)

        def record_error_info_filter(ei):
            if len(ei) == 0:
                return False
            return True

        self.error_info = error_info.filter(record_error_info_filter)
        for q_s in QUALITY_MAP:
            self.error_count[q_s] = self.error_info.filter(
                lambda x: x[0]['quality_issue'] == q_s).count()

        spark.stop()
        return self.summarize(record)

    def summarize(self, record) -> SummaryModel:
        summary = SummaryModel(
            dataset_id=self.dataset_id,
            input_model=record['input_model'],
            input_path=record['input_path'],
            output_path=record['output_path'],
            score=record['score'],
            num_good=record['num_good'],
            num_bad=record['num_bad'],
            total=record['total'],
            error_ratio={}
        )

        # calculate
        for quality_signal in self.error_count:
            summary.error_ratio[quality_signal] = 0
            if self.error_count[quality_signal] == 0:
                continue
            summary.error_ratio[quality_signal] = round(self.error_count[quality_signal] / record['total'],
                                                        6)
        return summary

    def evaluate(self, data_rdd_item) -> Dict[str, Any]:

        # eval with models ( Big Data Caution ）
        return execute_rule_spark(self.model, data_rdd_item)

    def save_data(self, start_time):
        output_path = self.raw_input.output_path + start_time
        model_path = output_path + '/' + self.model_name
        if not os.path.exists(model_path):
            os.makedirs(model_path)

    def get_model_list(self, model_name):
        self.model_name = model_name
        log.debug(f"[GlobalConfig.config]: {GlobalConfig.config}")
        if model_name in Model.llm_models:
            log.debug(f"[Load llm model {model_name}]")
            raise RuntimeError("LLM models are not supported yet.")
        elif model_name in Model.rule_groups:
            log.debug(f"[Load rule model {model_name}]")
            self.model: List[BaseRule] = Model.rule_groups[model_name]
            model_type = 'rule'
        elif GlobalConfig.config and GlobalConfig.config.custom_rule_list:
            log.debug("[Load custom rule]")
            self.model: List[BaseRule] = []
            for rule in GlobalConfig.config.custom_rule_list:
                assert isinstance(rule, str)
                if rule not in Model.rule_name_map:
                    raise KeyError(
                        f"{rule} not in Model.rule_name_map, there are {str(Model.rule_name_map.keys())}")
                self.model.append(Model.rule_name_map[rule])
            model_type = 'rule'
        else:
            raise KeyError('no such model: ' + self.model_name)

        # record for this
        self.model_type = model_type


def get_quality_signal(rule: Callable):
    for quality_signal in QUALITY_MAP:
        for rule_class in QUALITY_MAP[quality_signal]:
            if rule.__name__ == rule_class.__name__:
                return quality_signal

    raise RuntimeError('this rule can not find its quality_signal: ' + rule.__name__)


def execute_rule_spark(rule_map, d: InputModel) -> Dict[str, Any]:
    good_flag = True
    record = {
        'input_model': '',
        'input_path': '',
        'output_path': '',
        'score': 0,
        'num_good': 0,
        'num_bad': 0,
        'total': 1,
        'error_info': [],
    }
    if_qs_good = {}
    error_info = {}
    for q_s in QUALITY_MAP:
        error_info[q_s] = {'count': 0}
        if_qs_good[q_s] = True

    log.debug("[RuleMap]: " + str(rule_map))
    if not isinstance(d, InputModel):
        raise TypeError(f'input data must be an instance of InputModel: {str(d)}')
    for r in rule_map:
        rule_name = r.__name__
        # execute rule
        if rule_name.startswith('Prompt'):
            tmp: ModelRes = r.eval([d.prompt, d.content])
        else:
            tmp: ModelRes = r.eval([d.content])
        # analyze result
        if not tmp.error_status:
            continue
        good_flag = False
        q_s = get_quality_signal(r)
        if_qs_good[q_s] = False
        record['error_info'].append(
            {'data_id': d.data_id,
             'prompt': d.prompt,
             'content': d.content,
             'error_reason': tmp.error_reason,
             'quality_issue': q_s,
             'rule_name': rule_name,
             'good_flag': good_flag
             }
        )

    if not good_flag:
        record['num_bad'] += 1
    return record


def reduce_records(record_a, record_b) -> Dict[str, Any]:
    return {
        'input_model': record_a['input_model'],
        'input_path': record_a['input_path'],
        'output_path': record_a['output_path'],
        'score': 0,
        'num_good': 0,
        'num_bad': record_a['num_bad'] + record_b['num_bad'],
        'total': record_a['total'] + record_b['total'],
    }


def map_record_to_error_info(record: Dict[str, Any]) -> Dict[str, Any]:
    return record['error_info']
