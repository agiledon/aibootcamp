import json
from pydantic import BaseModel, field_validator
from langchain_core.prompts import StringPromptTemplate

delimiter = "####"
PROMPT = f"""将每个用户的信息用{delimiter}分割，并按照JSON格式提取姓名、职业和爱好信息。
示例如下："""

class PersonInfoPromptTemplate(StringPromptTemplate, BaseModel):
    """自定义提示词模板，用于生成Person的JSON格式信息"""

    @field_validator('input_variables', mode='before')
    def validate_input_variables(cls, value):
        if "name" not in value:
            raise ValueError("name is required")
        if "occupation" not in value:
            raise ValueError("occupation is required")
        if "hobbies" not in value:
            raise ValueError("hobbies is required")
        return value
    
    def format(self, **kwargs) -> str:
        person_info = {
            "name": kwargs['name'],
            "occupation": kwargs['occupation'],
            "hobbies": kwargs['hobbies']
        }
        return PROMPT + json.dumps(person_info, ensure_ascii=False)
    
    def _prompt_template(self) -> str:
        return "person-info"
    
person_info_prompt_template = PersonInfoPromptTemplate(input_variables=["name", "occupation", "hobbies"])
prompt_output = person_info_prompt_template.format(
    name="张三", 
    occupation="工程师", 
    hobbies=["读书", "编程", "旅行"])
print(prompt_output)