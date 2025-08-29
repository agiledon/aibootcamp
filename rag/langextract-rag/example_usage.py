"""
Word文档转文本使用示例

这个文件展示了如何使用word_to_text模块的各种功能。
"""

from word_to_text import (
    extract_text_from_word_document,
    convert_documents_to_text,
    save_text_to_file
)


def example_single_file():
    """示例：处理单个Word文档"""
    print("=== 处理单个Word文档 ===")
    
    # 处理单个文件
    file_path = "document/bounded_context.docx"
    text = extract_text_from_word_document(file_path, method="auto")
    
    if text:
        print(f"成功提取文本，长度: {len(text)} 字符")
        print("前200个字符:")
        print(text[:200] + "..." if len(text) > 200 else text)
        
        # 保存到文件
        save_text_to_file(text, "output/single_document.txt")
    else:
        print("提取文本失败")


def example_folder_processing():
    """示例：处理整个文件夹"""
    print("\n=== 处理整个文件夹 ===")
    
    # 处理document文件夹下的所有Word文档
    combined_text = convert_documents_to_text(
        folder_path="document",
        file_pattern="*.docx",
        method="auto",
        combine_all=True,
        separator="\n\n" + "="*80 + "\n\n"
    )
    
    if combined_text:
        print(f"成功提取文本，总长度: {len(combined_text)} 字符")
        
        # 保存合并的文本
        save_text_to_file(combined_text, "output/combined_documents.txt")
        
        # 显示每个文档的统计信息
        documents = combined_text.split("="*80)
        for i, doc in enumerate(documents):
            if doc.strip():
                lines = doc.strip().split('\n')
                title = lines[0] if lines else f"Document {i+1}"
                char_count = len(doc.strip())
                print(f"  {title}: {char_count} 字符")
    else:
        print("没有提取到文本")


def example_separate_files():
    """示例：分别处理每个文件"""
    print("\n=== 分别处理每个文件 ===")
    
    # 获取所有文档的文本列表
    texts = convert_documents_to_text(
        folder_path="document",
        file_pattern="*.docx",
        method="auto",
        combine_all=False
    )
    
    for i, text in enumerate(texts):
        if text.strip():
            filename = f"output/document_{i+1}.txt"
            save_text_to_file(text, filename)
            print(f"保存文档 {i+1}: {filename} ({len(text)} 字符)")


def example_with_different_methods():
    """示例：使用不同的提取方法"""
    print("\n=== 使用不同的提取方法 ===")
    
    file_path = "document/bounded_context.docx"
    methods = ["auto", "python-docx", "mammoth"]
    
    for method in methods:
        print(f"\n使用方法: {method}")
        text = extract_text_from_word_document(file_path, method=method)
        
        if text:
            print(f"  提取成功，长度: {len(text)} 字符")
            print(f"  前100个字符: {text[:100]}...")
        else:
            print(f"  提取失败")


if __name__ == "__main__":
    # 创建输出目录
    import os
    os.makedirs("output", exist_ok=True)
    
    # 运行示例
    example_single_file()
    example_folder_processing()
    example_separate_files()
    example_with_different_methods()
    
    print("\n=== 所有示例完成 ===")
    print("输出文件保存在 'output' 目录中")
