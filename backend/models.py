from pydantic import BaseModel


class CalcData(BaseModel):
    number: float
    message: str


class Calculation:
    def __init__(self):
        self.progress_rate = 0.0
        self.result = None


class CalculationContext:
    def __init__(self):
        self.calculations = {}

    def add_calculation(self, calc_id: str):
        self.calculations[calc_id] = Calculation()


calculation_context = CalculationContext()
# この変数はutils.long_computationで読み書きを、main.get_statusで読み込みのみを行う
# todo キャンセル処理、タイムアウト処理
