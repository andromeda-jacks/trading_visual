from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from datetime import datetime

app = FastAPI()

# 공공데이터 API URL (예시로 사용)
api_url = "https://api.example.com/trading-data"  # 실제 API URL로 변경하세요

# API에서 데이터를 가져오는 함수
def get_trading_data():
    response = requests.get(api_url)
    data = response.json()  # API에서 JSON 형식으로 데이터 가져오기
    return pd.DataFrame(data)

# 데이터를 가져옴
df = get_trading_data()

# 데이터에서 시간, 국내/해외 거래량 컬럼 추출
df["시간"] = pd.to_datetime(df["시간"])  # 시간 컬럼을 datetime으로 변환
df["국내 거래량"] = df["국내 거래량"].astype(float)
df["해외 거래량"] = df["해외 거래량"].astype(float)

# 날짜, 월, 연도별로 데이터를 그룹화
df["일"] = df["시간"].dt.date
df["월"] = df["시간"].dt.month
df["연도"] = df["시간"].dt.year

@app.get("/", response_class=HTMLResponse)
async def root():
    # 그래프 시각화 (시간별 거래량)
    plt.figure(figsize=(10, 6))
    plt.plot(df["시간"], df["국내 거래량"], marker="o", linestyle="-", color="b", label="국내 거래량")
    plt.plot(df["시간"], df["해외 거래량"], marker="x", linestyle="--", color="r", label="해외 거래량")
    plt.title("시간별 국내/해외 거래량")
    plt.xlabel("시간")
    plt.ylabel("거래량")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()

    # 그래프를 이미지로 변환
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    graph_url = base64.b64encode(buf.read()).decode("utf-8")
    
    html_content = f"""
    <html>
        <head>
            <title>거래량 시각화</title>
        </head>
        <body>
            <h1>시간별 거래량 시각화 (국내/해외 비교)</h1>
            <p>시간대별 국내와 해외의 거래량을 비교한 그래프입니다.</p>
            <img src="data:image/png;base64,{graph_url}" alt="시간별 거래량 그래프">
            <h2>국내/해외 거래량 비교</h2>
            <p>이 그래프는 각 시간대에 대한 국내와 해외의 거래량을 비교합니다. 각 선은 거래량을 시각적으로 나타냅니다.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

