from aiogram.fsm.state import StatesGroup, State


class CreatingAnAccount(StatesGroup):
    currency = State()
    name_currency = State()
    balance = State()


class AddExpenses(StatesGroup):
    category = State()
    title = State()
    amount_expenses = State()
    account_id = State()


class AddIncome(StatesGroup):
    source_of_income = State()
    amount_income = State()
    account_id = State()


class AddLimits(StatesGroup):
    account_id = State()
    name_category = State()
    amount_limit = State()
