# awaitは、async関数の実行結果が確定するまで待つためのキーワード
# 複数タスクを投げっぱなしにする→最後だけ揃えるというデザインパターンをすると、簡単に並列化っぽいことができる

import asyncio


async def processing(e, t):
    await asyncio.sleep(t)
    return e
