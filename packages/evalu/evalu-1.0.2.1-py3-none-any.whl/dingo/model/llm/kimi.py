import json

from openai import OpenAI

from dingo.model import Model
from dingo.model.modelres import ModelRes
from dingo.model.llm.base import BaseLLM

@Model.llm_register('kimi')
class Kimi(BaseLLM):
    key = ''
    path = 'moonshot-v1-8k'
    api_url = 'https://api.moonshot.cn/v1'

    client = None
    general_filter = """
        Please rate the following sentences based on their fluency, completeness, and level of repetition. 
        The scores from low to high indicate the quality of the sentences, with values ranging from 0 to 10 and reasons given. 
        Please provide a JSON format reply containing the specified key and value.
        requirement:
        -The returned content must be in JSON format and there should be no extra content.
        -The first key returned is score, which is an integer between 0 and 10.
        -The second key returned is type, with a value of one of the following: unsmooth, incomplete, or repetitive. If the sentence is correct, this value is empty.
        -The third key returned is reason, and the value is the reason for scoring.
        -If the sentence is empty, please give it a score of 0.
        
        
        %s
        
    """

    @classmethod
    def create_client(cls):
        cls.client = OpenAI(api_key=cls.key, base_url=cls.api_url)

    @classmethod
    def call_api(cls, input_data: str) -> ModelRes:
        if cls.client is None:
            cls.create_client()
        messages = [
            {"role": "system",
             "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            # {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"},
            {"role": "user", "content": cls.general_filter % input_data}
        ]

        completion = cls.client.chat.completions.create(
            model = cls.path,
            messages = messages,
            temperature = 0.3,
        )

        try:
            response = completion.choices[0].message.content
            response = json.loads(response)

            return ModelRes(
                error_status=False if response['score'] > 6 else True,
                error_type=response['type'],
                error_reason=response['reason']
            )
        except RuntimeError:
            return ModelRes(
                error_status=True,
                error_type='API_LOSS',
                error_reason=''
            )
