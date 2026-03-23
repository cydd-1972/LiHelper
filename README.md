# CAU综测问答系统 - 快速开始指南

## 🚀 快速启动（3步完成）

### 第1步：配置API密钥
编辑 `.env` 文件（已自动创建），将默认密钥替换为您的实际密钥：

```bash
# 编辑 .env 文件
DASHSCOPE_API_KEY=your_actual_api_key_here  # 替换为您的真实密钥
```

**获取API密钥：**
1. 访问 [阿里云DashScope控制台](https://dashscope.console.aliyun.com/)
2. 注册/登录账号
3. 创建API密钥
4. 复制密钥到 `.env` 文件

### 第2步：运行启动脚本
```bash
python start_system.py
```

启动脚本会自动：
- ✅ 检查环境配置
- ✅ 验证API密钥
- ✅ 安装缺失的依赖
- ✅ 启动Web界面

### 第3步：开始使用
系统启动后会自动在浏览器打开：http://localhost:8501

## 📝 测试问题示例

### 基础问题
- "什么是综合素质测评？"
- "综测包含哪几个方面？"
- "德智体美劳各占多少比例？"

### 竞赛加分
- "数学建模比赛属于什么级别？"
- "省级竞赛一等奖能加多少分？"
- "ACM竞赛如何加分？"

### 个人查询
- "查询我的综测成绩"
- "我这学期的排名是多少？"
- "帮我计算综测分数"

### 报告生成
- "生成我的综测报告"
- "分析我的综测情况"

## ⚠️ 常见问题

### 1. API密钥错误
**问题：** 提示"DASHSCOPE_API_KEY 未配置或为默认值"
**解决：** 
- 确保已编辑 `.env` 文件
- 确保密钥正确（不是默认的 your_api_key_here）
- 确保密钥有效且未过期

### 2. 依赖安装失败
**问题：** 某些包安装失败
**解决：**
```bash
# 手动安装依赖
pip install -r requirements.txt
pip install python-dotenv
```

### 3. 端口被占用
**问题：** 提示端口8501已被占用
**解决：**
```bash
# 使用其他端口
streamlit run app.py --server.port 8502
```

## 📂 项目结构

```
cau_bot/
├── .env                   # API密钥配置（需要编辑）
├── .env.example          # 配置示例
├── app.py                # 主应用
├── start_system.py       # 启动脚本
├── test_system.py        # 测试脚本
├── README_CAU.md         # 详细文档
├── QUICK_START.md        # 本文档
├── data/processed/       # PDF转换后的数据
├── prompts/             # 提示词文件（已更新）
└── agent/tools/         # 工具定义（已更新）
```

## 🔧 高级配置

### 使用其他模型
如需使用OpenAI或其他模型，请：
1. 在 `.env` 中添加相应的API密钥
2. 修改 `model/factory.py` 中的模型配置

### 添加更多PDF文档
1. 将PDF放入项目根目录
2. 运行 `python convert_pdfs.py`
3. 重启系统

## 📞 获取帮助

- 查看详细文档：`README_CAU.md`
- 运行系统测试：`python test_system.py`
- 检查日志文件：`logs/` 目录

---

**提示：** 首次使用建议先运行 `python test_system.py` 验证所有组件是否正常。

祝您使用愉快！🎉
