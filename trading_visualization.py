
import requests
import pandas as pd
import matplotlib.pyplot as plt

# 제공된 실제 API URL로 수정
api_url = 'https://api.kedn.com/trading-data'  # 실제 API URL로 수정
api_key = '/lo3zD/sg1U2J708WaSyo9Sto0LMRBm9oCQvJ2S08RVy3vGKAdxNgpGuTyltQGJI4i+sqc7oSjRw20wgKoqG9w=='  # 제공된 인증키

# API 호출을 위한 요청 헤더 설정
headers = {
    'Authorization': f'Bearer {api_key}'
}

# 데이터를 가져오는 함수
def get_trading_data():
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()  # 에러가 발생하면 예외 발생
    data = response.json()  # API 응답을 JSON으로 변환
    return data

# 데이터를 DataFrame으로 변환하고 날짜 처리
def process_data(data):
    df = pd.DataFrame(data['results'])  # 예시 데이터 구조, 실제 응답에 맞게 수정 필요
    df['date'] = pd.to_datetime(df['date'])  # 날짜 형식 변환
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    return df

# 데이터를 시각화하는 함수
def plot_data(df):
    # 연도별 거래량
    df_yearly = df.groupby('year')['trade_amount'].sum()
    df_yearly.plot(kind='bar', title='연도별 거래량', ylabel='거래량')
    plt.show()

    # 월별 거래량
    df_monthly = df.groupby('month')['trade_amount'].sum()
    df_monthly.plot(kind='bar', title='월별 거래량', ylabel='거래량')
    plt.show()

    # 일별 거래량
    df_daily = df.groupby('day')['trade_amount'].sum()
    df_daily.plot(kind='bar', title='일별 거래량', ylabel='거래량')
    plt.show()

# 메인 실행 흐름
if __name__ == '__main__':
    # API로 데이터 가져오기
    data = get_trading_data()
    
    # 데이터를 처리하여 DataFrame으로 변환
    df = process_data(data)
    
    # 데이터를 시각화
    plot_data(df)

