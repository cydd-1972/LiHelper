"""
PDF转换脚本 - 将综测相关PDF文档转换为JSON格式
由于系统未安装Java，暂时使用PyPDF2作为备选方案
"""

import json
import os
import shutil
from pathlib import Path
import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    """使用PyPDF2提取PDF文本"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
                text += "\n\n"  # 页面之间添加分隔
                
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None
    
    return text

def clean_text(text):
    """清理提取的文本"""
    if not text:
        return ""
    
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text)
    
    # 修复常见的OCR错误
    text = text.replace('　', ' ')  # 替换全角空格
    
    # 按句子分割，便于后续处理
    sentences = re.split(r'[。！？]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences

def process_pdf_to_json(pdf_path, output_path):
    """处理单个PDF文件并保存为JSON"""
    print(f"Processing {pdf_path}...")
    
    # 提取文本
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print(f"Failed to extract text from {pdf_path}")
        return False
    
    # 清理文本
    sentences = clean_text(text)
    
    # 构建JSON结构
    pdf_name = Path(pdf_path).stem
    json_data = {
        "source": pdf_name,
        "title": pdf_name,
        "content": text,
        "sentences": sentences,
        "metadata": {
            "type": "综测政策文件",
            "pages": len(sentences) // 20 + 1  # 估算页数
        }
    }
    
    # 保存为JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved to {output_path}")
    return True

def main():
    """主函数"""
    # PDF文件列表
    pdf_files = [
        "附件1：理学院本科生综合素质测评实施细则.pdf",
        "附件2：中国农业大学学科竞赛级别认定（2024-2025年）.pdf"
    ]
    
    # 创建输出目录
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 处理每个PDF
    for pdf_file in pdf_files:
        if not os.path.exists(pdf_file):
            print(f"Warning: {pdf_file} not found, skipping...")
            continue
            
        output_file = output_dir / f"{Path(pdf_file).stem}.json"
        process_pdf_to_json(pdf_file, output_file)
    
    print("\nConversion completed!")
    print(f"JSON files saved in {output_dir}")
    
    # 合并所有JSON文件为一个综合文档
    all_documents = []
    for json_file in output_dir.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            doc = json.load(f)
            all_documents.append(doc)
    
    # 保存合并文档
    combined_file = output_dir / "combined_documents.json"
    with open(combined_file, 'w', encoding='utf-8') as f:
        json.dump(all_documents, f, ensure_ascii=False, indent=2)
    
    print(f"Combined document saved to {combined_file}")

    # 供向量库加载：chroma 仅扫描 data/ 根目录下允许后缀的文件，复制合并结果便于入库
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    data_combined = data_dir / "combined_documents.json"
    shutil.copy2(combined_file, data_combined)
    print(f"已复制至 {data_combined}（建库请运行 rag/vectore_store 的 load_document，并视情况清空 chroma_db 与 md5.text）")

if __name__ == "__main__":
    # 首先尝试使用opendataloader-pdf（如果Java已安装）
    try:
        import opendataloader_pdf
        
        print("Using opendataloader-pdf for conversion...")
        
        # 创建输出目录
        output_dir = Path("data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 转换PDF文件
        pdf_files = [
            "附件1：理学院本科生综合素质测评实施细则.pdf",
            "附件2：中国农业大学学科竞赛级别认定（2024-2025年）.pdf"
        ]
        
        existing_files = [f for f in pdf_files if os.path.exists(f)]
        
        if existing_files:
            opendataloader_pdf.convert(
                input_path=existing_files,
                output_dir=str(output_dir),
                format="json,markdown"
            )
            print("Conversion completed using opendataloader-pdf!")
        else:
            print("No PDF files found!")
            
    except Exception as e:
        print(f"opendataloader-pdf failed (likely due to missing Java): {e}")
        print("Falling back to PyPDF2...")
        
        # 尝试使用PyPDF2
        try:
            main()
        except ImportError:
            print("PyPDF2 not installed. Installing...")
            import subprocess
            subprocess.run(["pip", "install", "PyPDF2"])
            main()
