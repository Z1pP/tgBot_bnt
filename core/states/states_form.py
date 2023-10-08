from aiogram.fsm.state import State, StatesGroup

class ReportState(StatesGroup):
    manager = State()
    orders = State()
    invoices = State()
    paid = State()
    margin = State()
    revenue = State()
    nds = State()
    is_correct = State()
