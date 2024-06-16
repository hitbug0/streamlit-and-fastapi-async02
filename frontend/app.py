# awaitは、async関数の実行結果が確定するまで待つためのキーワード
# 複数タスクを投げっぱなしにする→最後だけ揃えるというデザインパターンをすると、簡単に並列化っぽいことができる

import asyncio
import time

import streamlit as st
from streamlit import session_state as stss
from views.contents import content1, content2, content3, settings


# セッション状態の初期化関数
def initialize_session_state():
    print("initialize_session_state")

    # 更新ボタンが押されたかどうかをセッションステートで管理
    if "is_update_needed" not in stss:
        # Trueならばページを開くだけで（ボタンを押さなくても）レンダリングを一度実行する
        stss.is_update_needed = False

    if "calc_progress_rate" not in stss:
        stss.calc_progress_rate = 1  # 計算完了状態


# 初期ロード時のみ走る関数
# いかなる状況でも内容が変わらないコンテンツはここで定義しておく
@st.cache_data(ttl=60)
def initialize_static_contents():
    print("=============== initialize static contents ===============")

    st.subheader("UIレンダリングにおける同期/非同期")
    st.write(
        """
        - 以下の要素より現実的なものとし、非同期でUIレンダリングをする場合の動作確認を行う.
            - ソースコードのファイル構成
            - バックエンドとの接続
            - ページのデザイン
        - UI要素$E_i$ごとの表示には$t_i$ [s]かかる設定とする.
        """
    )


# 実質的なメイン処理
async def main():
    initialize_session_state()  # キャッシュは持たない。たまにキャッシュがあるのにセッション状態がないケースが起こるため
    initialize_static_contents()
    tabs = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
    t1, t2, t3, rerun_button = settings(st.sidebar)
    # 更新ボタンを押さなくても回すべき処理はこの上に書く

    # 更新ボタンが押されていたら「更新が必要」の状態にする
    if rerun_button:
        stss.is_update_needed = True

    # 更新不要の場合は処理終了
    if not stss.is_update_needed:
        return True

    # 更新が必要な場合は以下を実行する
    print("load data: start")
    start = time.time()  # 時間計測用
    tasks = []  # 「これやっといて～」みたいな感じで割り振ったタスクリスト
    with tabs[0]:
        task = asyncio.create_task(content1(f"time: {t1} s", t1, st))  # タスクその1
        tasks.append(task)
    with tabs[1]:
        task = asyncio.create_task(content2(f"time: {t2} s", t2, st))  # タスクその2
        tasks.append(task)
    with tabs[2]:
        task = asyncio.create_task(content3(f"time: {t3} s", t3, st))  # タスクその3
        tasks.append(task)

    await asyncio.gather(*tasks)  # すべてのタスクが終わるまで待つ

    t_total = time.time() - start
    st.write(f"所要時間: {t_total:.2f} s")
    stss.is_update_needed = False  # 更新後は「更新不要」状態にする
    print("load data: end")


if __name__ == "__main__":
    asyncio.run(main())
