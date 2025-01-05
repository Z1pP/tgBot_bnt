from aiogram.fsm.state import State, StatesGroup


class ReportState(StatesGroup):
    manager_tg_id = State()
    total_orders = State()
    total_invoices = State()
    paid_invoices = State()
    total_margin = State()
    total_revenue = State()
    nds = State()


class Registration(StatesGroup):
    name = State()


class ChangeName(StatesGroup):
    name = State()


class Period(StatesGroup):
    period = State()
