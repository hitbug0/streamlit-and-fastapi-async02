import uuid

import uvicorn
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .models import CalcData, calculation_context
from .utils import long_computation

app = FastAPI()


@app.post("/calc")
async def calculate(data: CalcData, background_tasks: BackgroundTasks):
    # print(data)
    calc_id = str(uuid.uuid4())
    print(calc_id)
    calculation_context.add_calculation(calc_id)  # 計算コンテキストに新しい計算を追加
    background_tasks.add_task(long_computation, calc_id, data.number)
    return JSONResponse(content={"message": "calculation started", "calc_id": calc_id})


@app.get("/get_status/{calc_id}")
async def get_status(calc_id: str):
    if calc_id not in calculation_context.calculations:
        raise HTTPException(status_code=404, detail="Calculation ID not found")

    progress_rate = calculation_context.calculations[calc_id].progress_rate
    # print(f"計算関数の中のprogress_rate: {progress_rate:.2f}")

    if progress_rate < 1:
        msg = "calculating now"
        calc_result = None
    else:
        msg = "calculated"
        calc_result = calculation_context.calculations[calc_id].result

    return JSONResponse(
        content={
            "message": msg,
            "calc_result": calc_result,
            "progress_rate": progress_rate,
        }
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
