"""
文档转换器模块 - 将各种文档类型转换为PDF进行预览
"""

import os
import tempfile
import io
from typing import Optional
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import markdown2
from docx import Document


class DocumentConverter:
    """文档转换器类，将各种文档类型转换为PDF"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_fonts()
    
    def _setup_fonts(self):
        """设置中文字体支持"""
        try:
            # 尝试注册中文字体
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
            self.chinese_font = 'STSong-Light'
        except:
            # 如果中文字体不可用，使用默认字体
            self.chinese_font = 'Helvetica'
    
    def _create_paragraph_style(self):
        """创建段落样式"""
        style = ParagraphStyle(
            'CustomStyle',
            parent=self.styles['Normal'],
            fontName=self.chinese_font,
            fontSize=12,
            leading=16,
            spaceAfter=12,
            leftIndent=0,
            rightIndent=0
        )
        return style
    
    def convert_to_pdf(self, content: str, file_extension: str, max_pages: int = 5) -> Optional[bytes]:
        """
        将文档内容转换为PDF
        
        Args:
            content: 文档内容
            file_extension: 文件扩展名
            max_pages: 最大页数
            
        Returns:
            PDF字节数据或None
        """
        try:
            # 创建临时PDF文件
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
                doc = SimpleDocTemplate(temp_pdf.name, pagesize=A4)
                story = []
                style = self._create_paragraph_style()
                
                # 根据文件类型处理内容
                if file_extension.lower() in ['.md', '.markdown']:
                    # 将Markdown转换为HTML，再转换为纯文本
                    html = markdown2.markdown(content)
                    # 简单的HTML到文本转换
                    import re
                    text_content = re.sub(r'<[^>]+>', '', html)
                    text_content = re.sub(r'\n\s*\n', '\n\n', text_content)
                elif file_extension.lower() in ['.txt']:
                    text_content = content
                elif file_extension.lower() in ['.csv']:
                    # CSV文件特殊处理
                    lines = content.split('\n')
                    text_content = '\n'.join([f"第{i+1}行: {line}" for i, line in enumerate(lines[:50])])  # 限制行数
                else:
                    text_content = content
                
                # 将文本内容分段
                paragraphs = text_content.split('\n\n')
                
                # 限制段落数量以控制页数
                max_paragraphs = max_pages * 3  # 每页大约3个段落
                paragraphs = paragraphs[:max_paragraphs]
                
                for para_text in paragraphs:
                    if para_text.strip():
                        # 处理长段落，避免单行过长
                        if len(para_text) > 500:
                            para_text = para_text[:500] + "..."
                        
                        para = Paragraph(para_text.strip(), style)
                        story.append(para)
                        story.append(Spacer(1, 12))
                
                # 如果内容被截断，添加提示
                if len(paragraphs) >= max_paragraphs:
                    truncate_para = Paragraph(f"<i>注意：内容已截断，仅显示前{max_pages}页内容</i>", style)
                    story.append(truncate_para)
                
                # 生成PDF
                doc.build(story)
                
                # 读取PDF内容
                with open(temp_pdf.name, 'rb') as f:
                    pdf_content = f.read()
                
                # 清理临时文件
                os.unlink(temp_pdf.name)
                
                return pdf_content
                
        except Exception as e:
            print(f"PDF转换失败: {e}")
            return None
    
    def convert_docx_to_pdf(self, docx_content: bytes, max_pages: int = 5) -> Optional[bytes]:
        """
        将DOCX文档转换为PDF
        
        Args:
            docx_content: DOCX文件字节数据
            max_pages: 最大页数
            
        Returns:
            PDF字节数据或None
        """
        try:
            # 创建临时DOCX文件
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_docx:
                temp_docx.write(docx_content)
                temp_docx.flush()
                
                # 读取DOCX内容
                doc = Document(temp_docx.name)
                text_content = ""
                
                for paragraph in doc.paragraphs:
                    text_content += paragraph.text + "\n\n"
                
                # 清理临时文件
                os.unlink(temp_docx.name)
                
                # 转换为PDF
                return self.convert_to_pdf(text_content, '.txt', max_pages)
                
        except Exception as e:
            print(f"DOCX转换失败: {e}")
            return None
