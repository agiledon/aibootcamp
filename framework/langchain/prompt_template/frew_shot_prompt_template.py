from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate

example_prompt = PromptTemplate(
    template=" 问题：{input} 答案：{output}",
    input_variables=["input", "output"]
)

template = FewShotPromptTemplate(
    examples=[
        {"input": "1+1等于多少？", "output": "2"},
        {"input": "3+2等于多少？", "output": "5"},
    ],
    example_prompt=example_prompt,
    input_variables=["input"],
    suffix="问题：{input}"
)
prompt = template.format(input="5-3等于多少？")
print(prompt)