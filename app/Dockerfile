
FROM python:3.10
WORKDIR /app
COPY app/main.py /app/main.py
COPY app/requirements.txt /app/requirements.txt
COPY app/data/ /app/data/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
