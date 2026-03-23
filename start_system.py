#!/usr/bin/env python
"""
CAU综测问答系统启动脚本
自动检查配置并启动系统
"""

import os
import sys
import subprocess
from pathlib import Path

def check_env_file():
    """检查.env文件是否存在"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        print("=" * 60)
        print("⚠️  未找到 .env 文件")
        print("=" * 60)
        
        if env_example.exists():
            print("\n正在从 .env.example 创建 .env 文件...")
            import shutil
            shutil.copy(env_example, env_file)
            print("✅ 已创建 .env 文件")
            print("\n请编辑 .env 文件并填入 DashScope API Key：")
            print("  DASHSCOPE_API_KEY=sk-...（来自 DashScope 控制台，不是 RAM AccessKey）")
            print("获取地址: https://dashscope.console.aliyun.com/")
            return False
        else:
            print("错误：.env.example 文件也不存在")
            return False
    return True

def check_api_key():
    """检查API密钥是否配置"""
    # 加载环境变量
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("正在安装 python-dotenv...")
        subprocess.run([sys.executable, "-m", "pip", "install", "python-dotenv"])
        from dotenv import load_dotenv
        load_dotenv()
    
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if api_key and api_key != "your_api_key_here":
        print("✅ 已配置 DashScope API Key")
        return True

    # 常见误配：只填了 RAM AccessKey
    ak = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    if ak and ak != "your_access_key_id_here":
        print("=" * 60)
        print("⚠️  检测到 ALIBABA_CLOUD_ACCESS_KEY_ID，但通义千问需要 DashScope API Key")
        print("请在 .env 中设置 DASHSCOPE_API_KEY（控制台「API-KEY」），")
        print("RAM 的 AccessKey 不能用于本项目的模型调用。")
        print("获取: https://dashscope.console.aliyun.com/")
        print("=" * 60)

    print("=" * 60)
    print("❌ 错误：未配置有效的 DASHSCOPE_API_KEY")
    print("=" * 60)
    print("\n在 .env 中设置（来自 DashScope 控制台，不是 RAM AccessKey）：")
    print("  DASHSCOPE_API_KEY=sk-xxxxxxxx")
    print("\n获取地址: https://dashscope.console.aliyun.com/")
    print("\n配置完成后，请重新运行此脚本")
    return False

def check_dependencies():
    """检查依赖是否安装"""
    required_packages = [
        "streamlit",
        "langchain",
        "langchain-community",
        "PyPDF2",
        "python-dotenv"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n缺少以下依赖包：{', '.join(missing_packages)}")
        print("正在安装...")
        for package in missing_packages:
            subprocess.run([sys.executable, "-m", "pip", "install", package])
        print("✅ 依赖安装完成")
    else:
        print("✅ 所有依赖已安装")
    
    return True

def start_streamlit():
    """启动Streamlit应用"""
    print("\n" + "=" * 60)
    print("🚀 正在启动CAU综测问答系统...")
    print("=" * 60)
    print("\n系统将在浏览器中自动打开")
    print("如果没有自动打开，请访问: http://localhost:8501")
    print("\n按 Ctrl+C 停止系统")
    print("=" * 60 + "\n")
    
    try:
        subprocess.run(["streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n\n系统已停止")
    except Exception as e:
        print(f"\n启动失败：{e}")
        print("请尝试手动运行: streamlit run app.py")

def main():
    """主函数"""
    print("=" * 60)
    print("CAU综测问答系统 - 启动检查")
    print("=" * 60)
    
    # 检查环境文件
    if not check_env_file():
        print("\n请配置 .env 文件后重新运行")
        sys.exit(1)
    
    # 检查API密钥
    if not check_api_key():
        sys.exit(1)
    
    # 检查依赖
    check_dependencies()
    
    # 启动系统
    start_streamlit()

if __name__ == "__main__":
    main()
