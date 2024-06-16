# awaitは、async関数の実行結果が確定するまで待つためのキーワード
# 複数タスクを投げっぱなしにする→最後だけ揃えるというデザインパターンをすると、簡単に並列化っぽいことができる

import asyncio

import requests
from pydantic import BaseModel, ValidationError
from streamlit import session_state as stss

SERVER_URL = "http://127.0.0.1:8000"


class CalcData(BaseModel):
    number: float
    message: str


async def calculate(message, t):
    # データのバリデーション (このケースではなくてもよい)
    try:
        data = CalcData(number=t, message=message)
    except ValidationError as e:
        print(f"Data validation error: {e}")
        return False

    responce = requests.post(f"{SERVER_URL}/calc", json=data.model_dump())
    if not responce.status_code == 200:
        return "failed to calc request"
    stss.calc_progress_rate = 0

    print(responce.json()["message"])
    calc_id = responce.json()["calc_id"]

    while stss.calc_progress_rate < 1:
        responce = requests.get(f"{SERVER_URL}/get_status/{calc_id}")

        if not responce.status_code == 200:
            print("35: ", responce.status_code)

        stss.calc_progress_rate = responce.json()["progress_rate"]
        print(
            f"""{responce.json()["message"]}, progress: {responce.json()["progress_rate"]:.2f}"""
        )
        await asyncio.sleep(t / 10)

    return responce.json()["calc_result"]
