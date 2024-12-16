from aiogram.fsm.state import State, StatesGroup


class ReportState(StatesGroup):
    manager = State()
    orders = State()
    invoices = State()
    paid = State()
    margin = State()
    revenue = State()
    nds = State()


class Registration(StatesGroup):
    name = State()


class ChangeName(StatesGroup):
    name = State()


class Period(StatesGroup):
    period = State()
