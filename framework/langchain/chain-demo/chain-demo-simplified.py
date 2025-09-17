from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaLLM

# 初始化 LLM 和解析器
llm = OllamaLLM(model="qwen:7b")
parser = StrOutputParser()

# 使用现代化的 LangChain 语法 - 更简洁的提示模板定义
def create_chain(template: str):
    """创建标准化的链"""
    return PromptTemplate.from_template(template) | llm | parser

# 定义所有提示模板
templates = {
    "title": "<s><|user|>\n根据{summary}阐述的故事生成一个标题. 只返回标题.<|end|>\n<|assistant|>",
    "character": "<s><|user|>\n根据{summary}和{title}生成一个故事的主角描述. 只返回描述.<|end|>\n<|assistant|>",
    "story": "<s><|user|>\n根据{summary}和{title}用中文生成一个故事. 故事的主角是{character}. 返回标题、描述和故事, 故事不能超过一个段落.\n<|end|>\n<|assistant|>"
}

# 使用最新的 LangChain API - 超级简洁的链式构建
story_pipeline = (
    RunnablePassthrough.assign(title=create_chain(templates["title"]))
    .assign(character=create_chain(templates["character"]))
    .assign(story=create_chain(templates["story"]))
)

# 执行链式架构
if __name__ == "__main__":
    result = story_pipeline.invoke({"summary": "一个小女孩失去了她的妈妈，她很伤心。"})
    
    # 使用更现代的 f-string 格式化输出
    print(f"""
    📖 故事生成结果:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🏷️  标题: {result.get('title', 'N/A')}
    
    👤 角色: {result.get('character', 'N/A')}
    
    📚 故事: {result.get('story', 'N/A')}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
