from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen:7b")

# 创建一个链式架构来生成故事的标题
template = """<s><|user|>
根据{summary}阐述的故事生成一个标题. 只返回标题.<|end|>
<|assistant|>"""
title_prompt = PromptTemplate(template=template, input_variables=["summary"])

# 使用新的RunnableSequence语法
title_chain = title_prompt | llm | StrOutputParser()

# title = title_chain.invoke({"summary": "一个小女孩失去了她的妈妈，她很伤心。"})

# 使用故事梗概和标题创建一个链式架构来生成角色描述
character_template = """<s><|user|>
根据{summary}和{title}生成一个故事的主角描述. 只返回描述.<|end|>
<|assistant|>"""
character_prompt = PromptTemplate(
    template=character_template, input_variables=["summary", "title"]
)
character_chain = character_prompt | llm | StrOutputParser()

# 使用故事梗概、标题和角色描述创建一个链式架构来生成故事
template = """<s><|user|>
根据{summary}和{title}用中文生成一个故事. 故事的主角是{character}. 返回标题、描述和故事, 故事不能超过一个段落.
<|end|>
<|assistant|>"""
story_prompt = PromptTemplate(
    template=template, input_variables=["summary", "title", "character"]
)
story_chain = story_prompt | llm | StrOutputParser()


# 创建组合链式架构
def create_story_chain():
    # 第一步：生成标题
    title_step = RunnablePassthrough.assign(
        title=title_chain
    )
    
    # 第二步：生成角色描述
    character_step = RunnablePassthrough.assign(
        character=character_chain
    )
    
    # 第三步：生成故事并指定output_key
    story_step = RunnablePassthrough.assign(
        story=story_chain
    )
    
    # 组合所有步骤
    full_chain = title_step | character_step | story_step
    
    return full_chain

# 创建并执行链式架构
story_chain_complete = create_story_chain()
result = story_chain_complete.invoke({"summary": "一个小女孩失去了她的妈妈，她很伤心。"})

print(f"生成的标题: {result.get('title', 'N/A')}")
print(f"生成的角色: {result.get('character', 'N/A')}")
print(f"生成的故事: {result.get('story', 'N/A')}")
