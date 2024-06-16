import asyncio

from .models import calculation_context


async def long_computation(calc_id: str, t: float):
    calculation = calculation_context.calculations[calc_id]
    calculation.progress_rate = 0.0
    N = 28
    dt = t / N
    for i in range(N):
        calculation.progress_rate += 1 / N
        print(f"計算関数の中のprogress_rate: {calculation.progress_rate:.2f}")
        await asyncio.sleep(dt)

    calculation.progress_rate = 1.0
    calculation.result = t**2
