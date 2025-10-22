# 🚀 ML Deploy Demo – FastAPI + Docker

A lightweight **FastAPI application** demonstrating how to deploy a simple machine learning pipeline inside a Docker container.  
The project showcases how to serve ML models or any Python backend service with FastAPI, following clean and reproducible deployment practices.

---

## 🧱 Project Overview

This repository demonstrates:
- ✅ Building a minimal and production-ready **Docker image** using `python:3.11-slim`
- ✅ Serving a **FastAPI API** (e.g., `/predict`, `/health`)
- ✅ Clean dependency management with `requirements.txt`
- ✅ Good logging practices, environment setup, and container orchestration readiness

---


## ⚙️ Setup & Local Development

### 1️⃣ Create a virtual environment
```bash
python -m venv .venv
.\.venv\Scripts\activate      # Windows PowerShell
# source .venv/bin/activate   # macOS / Linux
```

### 2️⃣ Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
### 3️⃣ Run locally (without Docker)
```bash
uvicorn app.main:app --reload
```
Then open 👉 http://localhost:8000/docs

Optional health check: http://localhost:8000/health

---

## 🐳 Run with Docker

### 1️⃣ Build the image
```bash
docker build -t ml-deploy-demo .
```
### 2️⃣ Run the container
```bash
docker run -d -p 8000:8000 --name ml-deploy-demo ml-deploy-demo:latest
```
### 3️⃣ Test in your browser

Swagger UI: http://localhost:8000/docs

Optional health check: http://localhost:8000/health

---

# 👨‍💻 Author

Jan Dyndor

💼 AXA XL – IDA Graduate Program

🎯 Aspiring Cloud AI Engineer | Python Backend | FastAPI | Azure | MLOps

📧 [LinkedIn](https://www.linkedin.com/in/jan-dyndor)