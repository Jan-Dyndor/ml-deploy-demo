FROM python:3.11-slim

# System deps (wheel builds) — small and sufficient
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

# Workdir inside the container
WORKDIR /app

# Install Python deps first to leverage Docker layer cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app - to workdir
COPY . .

# Good defaults
ENV PYTHONUNBUFFERED=1

# Expose FastAPI port
EXPOSE 8000

# FastAPI app object is named "app" in app/main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]