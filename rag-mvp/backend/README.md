# RAG FAQ Backend

快速开始（Windows/PowerShell）：

1. 创建并激活虚拟环境，安装依赖：
   `powershell
   cd rag-mvp/backend
   python -m venv .venv
   .\\.venv\\Scripts\\Activate.ps1
   pip install -r requirements.txt
   `

2. 复制环境变量，并按需填写（至少选一个 LLM 方案）：
   `powershell
   copy .env.example .env
   `

3. 放入文档至 data/raw/FAQ/（支持 txt/md/pdf/docx），示例文件已提供。

4. 构建向量索引：
   `powershell
   python .\\scripts\\ingest.py
   `

5. 启动服务：
   `powershell
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   `

6. 健康检查：http://127.0.0.1:8000/api/health
