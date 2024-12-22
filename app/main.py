
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd

# FastAPI 애플리케이션 초기화
app = FastAPI()

# "static" 폴더를 정적 파일 서버로 설정
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 기본 루트 경로
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        </head>
        <body>
            <h1>Welcome to Trading Visualization</h1>
            <p>Trading data visualization page</p>
        </body>
    </html>
    """

# 데이터 불러오기 예시
@app.get("/data")
async def get_data():
    try:
        data = pd.read_csv("data/trading_data.csv")
        return data.head().to_dict()  # 데이터의 첫 번째 5개 행을 반환
    except FileNotFoundError:
        return {"error": "Data file not found."}

