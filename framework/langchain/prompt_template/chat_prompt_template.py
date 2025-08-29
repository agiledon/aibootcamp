from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

system_message = SystemMessagePromptTemplate.from_template(
    "你是一个专业的翻译助手，可以将{input_language}翻译为{output_language}。"
)

human_message = HumanMessagePromptTemplate.from_template("{talk}")

chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message])

messages = chat_prompt.format_prompt(
    input_language="英语",
    output_language="中文",
    talk="Hello, how are you?"
).to_messages()

for message in messages:
    print(message)