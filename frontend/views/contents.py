# awaitは、async関数の実行結果が確定するまで待つためのキーワード
# 複数タスクを投げっぱなしにする→最後だけ揃えるというデザインパターンをすると、簡単に並列化っぽいことができる

import asyncio

from api.api import calculate
from modules.utils import processing
from streamlit import session_state as stss


async def content1(e, t, div):
    tasks = [
        # プログレスバーの表示
        asyncio.create_task(disp_bar(div)),
        # バックエンドとのやりとり
        asyncio.create_task(calculate(e, t)),
    ]
    results = await asyncio.gather(*tasks)  # すべてのタスクが終わるまで待つ

    div.write(results[1])


async def disp_bar(div):
    stss.calc_progress_rate = 0
    bar = div.progress(0.0, text="Now loading...")
    while stss.calc_progress_rate < 1:
        bar.progress(stss.calc_progress_rate)
        await asyncio.sleep(0.5)

    bar.empty()


async def content2(e, t, div):
    e_ = await processing(e, t)
    div.write(e_)


async def content3(e, t, div):
    e_ = await processing(e, t)
    div.write(e_)


def settings(div):
    div.write("### 設定")
    t1 = div.slider("$t_1$ [s]", min_value=0.0, max_value=10.0, value=4.0, step=0.5)
    t2 = div.slider("$t_2$ [s]", min_value=0.0, max_value=10.0, value=5.0, step=0.5)
    t3 = div.slider("$t_3$ [s]", min_value=0.0, max_value=10.0, value=0.5, step=0.5)
    button = div.button("データ更新")
    return t1, t2, t3, button
