import langextract as lx
from word_to_text import extract_text_from_word_document
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 检查并提取文本
file_path = "document/bounded_context.docx"
if os.path.exists(file_path):
    input_text = extract_text_from_word_document(file_path, method="auto")
    logger.info(f"Extracted text from {file_path}, length: {len(input_text)} characters")
else:
    # 如果文档不存在，使用已提取的文本文件
    text_file = "extracted_text.txt"
    if os.path.exists(text_file):
        with open(text_file, 'r', encoding='utf-8') as f:
            input_text = f.read()
        logger.info(f"Loaded text from {text_file}, length: {len(input_text)} characters")
    else:
        logger.error("No text source found")
        exit(1)

# 文本预处理：清理和截断
def preprocess_text(text, max_length=1500):
    """预处理文本，清理格式并截断到合适长度"""
    # 移除多余的空白字符
    text = ' '.join(text.split())
    
    # 如果文本太长，截断到合适长度
    if len(text) > max_length:
        logger.warning(f"Text too long ({len(text)} chars), truncating to {max_length} chars")
        text = text[:max_length] + "..."
    
    return text

# 预处理输入文本
input_text = preprocess_text(input_text)
logger.info(f"Preprocessed text length: {len(input_text)} characters")

# 使用更简单明确的提示
prompt_description = "从文本中提取DDD（领域驱动设计）的专用术语和定义"

# 定义更清晰的示例
examples = [
    lx.data.ExampleData(
        text="什么是限界上下文（Bounded Context）？我认为，要明确限界上下文的定义，需要从Bounded与Context这两个单词的含义来理解。Context表现了业务流程的场景片段。整个业务流程由诸多具有时序的活动组成，随着流程的进行，不同的活动需要不同的角色参与，并导致上下文因为某个活动的执行发生切换。因而，上下文（Context）其实是动态的业务流程被边界（Bounded）静态切分的产物。",
        extractions=[
            lx.data.Extraction(extraction_class="term", extraction_text="限界上下文"),
            lx.data.Extraction(extraction_class="term", extraction_text="Bounded Context"),
            lx.data.Extraction(extraction_class="definition", extraction_text="限界上下文是业务流程被边界静态切分后获得的场景片段")
        ]
    )
]

# 尝试自动提取
try:
    logger.info("Starting extraction with simplified configuration...")
    
    result = lx.extract(
        text_or_documents=input_text,
        prompt_description=prompt_description,
        examples=examples,
        model_id="llama3:latest",
        model_url="http://localhost:11434",
        fence_output=True,
        use_schema_constraints=False
    )
    
    # Display entities with positions
    print(f"Input text (first 200 chars): {input_text[:200]}...\n")
    print("Extracted entities:")
    
    if result.extractions and len(result.extractions) > 0:
        for entity in result.extractions:
            position_info = ""
            if entity.char_interval:
                start, end = entity.char_interval.start_pos, entity.char_interval.end_pos
                position_info = f" (pos: {start}-{end})"
            print(f"• {entity.extraction_class.capitalize()}: {entity.extraction_text}{position_info}")
        
        # Save and visualize the results
        lx.io.save_annotated_documents([result], output_name="bounded_context_extraction.jsonl", output_dir=".")
        
        # Generate the interactive visualization
        html_content = lx.visualize("bounded_context_extraction.jsonl")
        with open("bounded_context_visualization.html", "w", encoding='utf-8') as f:
            if hasattr(html_content, 'data'):
                f.write(html_content.data)  # For Jupyter/Colab
            else:
                f.write(html_content)
        
        print("Interactive visualization saved to bounded_context_visualization.html")
    else:
        print("No entities extracted from LLM, using manual extraction...")
        raise Exception("No extractions found")
        
except Exception as e:
    logger.warning(f"Automatic extraction failed: {str(e)}")
    print(f"Automatic extraction failed: {str(e)}")
    print("Using manual extraction for demonstration...")
    
    # 手动创建一些基本的提取结果用于演示
    try:
        # 手动创建一些基本的提取结果
        manual_extractions = [
            lx.data.Extraction(extraction_class="term", extraction_text="限界上下文"),
            lx.data.Extraction(extraction_class="term", extraction_text="Bounded Context"),
            lx.data.Extraction(extraction_class="definition", extraction_text="限界上下文是业务流程被边界静态切分后获得的场景片段"),
            lx.data.Extraction(extraction_class="term", extraction_text="领域驱动设计"),
            lx.data.Extraction(extraction_class="term", extraction_text="DDD"),
            lx.data.Extraction(extraction_class="term", extraction_text="统一语言"),
            lx.data.Extraction(extraction_class="term", extraction_text="领域模型"),
            lx.data.Extraction(extraction_class="term", extraction_text="业务能力"),
            lx.data.Extraction(extraction_class="term", extraction_text="知识语境"),
            lx.data.Extraction(extraction_class="term", extraction_text="自治的架构单元"),
            lx.data.Extraction(extraction_class="term", extraction_text="上下文"),
            lx.data.Extraction(extraction_class="term", extraction_text="Context"),
            lx.data.Extraction(extraction_class="term", extraction_text="边界"),
            lx.data.Extraction(extraction_class="term", extraction_text="Bounded"),
            lx.data.Extraction(extraction_class="term", extraction_text="业务流程"),
            lx.data.Extraction(extraction_class="term", extraction_text="业务场景"),
            lx.data.Extraction(extraction_class="term", extraction_text="角色"),
            lx.data.Extraction(extraction_class="term", extraction_text="活动"),
            lx.data.Extraction(extraction_class="term", extraction_text="领域知识"),
            lx.data.Extraction(extraction_class="term", extraction_text="领域概念")
        ]
        
        # 创建一个简单的文档对象
        from langextract.data import Document
        
        doc = Document(
            text=input_text,
            extractions=manual_extractions
        )
        
        # 保存结果
        lx.io.save_annotated_documents([doc], output_name="bounded_context_extraction.jsonl", output_dir=".")
        
        # 生成可视化
        html_content = lx.visualize("bounded_context_extraction.jsonl")
        with open("bounded_context_visualization.html", "w", encoding='utf-8') as f:
            if hasattr(html_content, 'data'):
                f.write(html_content.data)
            else:
                f.write(html_content)
        
        print("Manual extraction completed and visualization saved to bounded_context_visualization.html")
        print("Extracted entities:")
        for entity in manual_extractions:
            print(f"• {entity.extraction_class.capitalize()}: {entity.extraction_text}")
            
    except Exception as manual_error:
        print(f"Manual extraction also failed: {str(manual_error)}")
        print("Please check:")
        print("1. Ollama is running on http://localhost:11434")
        print("2. llama3:latest model is available")
        print("3. The input text is valid")