from aiogram.fsm.state import StatesGroup, State


class UserToken(StatesGroup):
    token = State()


class FCreatingAnAccount(StatesGroup):
    currency = State()
    name_currency = State()
    balance = State()


class FAddExpenses(StatesGroup):
    category = State()
    title = State()
    amount_expenses = State()
    account_id = State()


class FAddIncome(StatesGroup):
    source_of_income = State()
    amount_income = State()
    account_id = State()


class FAddLimits(StatesGroup):
    account_id = State()
    name_category = State()
    amount_limit = State()