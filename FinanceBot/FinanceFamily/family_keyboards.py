from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from FinanceServer.family_finance_connection import family_finance_server


class FAccountCallback(CallbackData, prefix='F_account'):
    call_data: str
    call: str


class FAddConsumptionCallback(CallbackData, prefix='F_add'):
    call_data: str
    call_add: str


class FAddIncomeCallback(CallbackData, prefix='F_add_income'):
    call_data: str
    call_add: str


class FAnalysisExpensesCallback(CallbackData, prefix='F_analysis_expenses'):
    call_data: str
    call_analysis: str


class FAnalysisIncomeCallback(CallbackData, prefix='F_analysis_income'):
    call_data: str
    call_analysis: str


class FLimitsCallback(CallbackData, prefix='F_limits'):
    call_data: str
    call_limits: str


class FDelLimitsCallback(CallbackData, prefix='F_dellimits'):
    call_data: str
    call_dellimits: str


class FListDelLimitsCallback(CallbackData, prefix='F_listdellimits'):
    call_data: str
    call_listdellimits: str


# TODO Семейный Кошелек
def family_account_keyboard():
    personal_account_kb = InlineKeyboardBuilder()
    personal_account_kb.button(
        text="Счета 💰", callback_data="F_accounts")
    personal_account_kb.button(
        text="Добавить ✏", callback_data="F_add")
    personal_account_kb.button(
        text="Аналитика 📊", callback_data="F_analytics")
    personal_account_kb.button(
        text="Лимиты 🔒", callback_data="F_limits")
    personal_account_kb.button(
        text="Настройки ⚙", callback_data="F_settings")
    personal_account_kb.button(
        text="Главное меню", callback_data="F_main_menu")
    personal_account_kb.adjust(1)
    return personal_account_kb.as_markup()


def family_wallet_entry():
    account_kb = InlineKeyboardBuilder()
    account_kb.button(
        text="Создать семейный кошелек", callback_data="F_create_wallet")
    account_kb.button(
        text="Войти по коду", callback_data="F_input")
    account_kb.button(
        text="Назад в Меню", callback_data="F_main_menu")
    account_kb.adjust(1)
    return account_kb.as_markup()


def account_keyboard():
    account_kb = InlineKeyboardBuilder()
    account_kb.button(
        text="Создать ➕", callback_data="F_create")
    account_kb.button(
        text="Удалить ➖", callback_data="F_delete")
    account_kb.button(
        text="Назад в кошелёк", callback_data="F_back_to_wallet")
    account_kb.adjust(1)
    return account_kb.as_markup()


# # TODO Выбор валюты
currency = ['BYN', 'RUB', 'USD', 'EUR']


def list_of_currencies_keyboard():
    list_of_currencies_kb = InlineKeyboardBuilder()
    for list_of_currencies in currency:
        list_of_currencies_kb.button(text=list_of_currencies, callback_data=list_of_currencies)
        list_of_currencies_kb.adjust(1)
    return list_of_currencies_kb.as_markup()


# TODO Создать ещё (Счет)
def create_another_account_keyboard():
    create_another_account_kb = InlineKeyboardBuilder()
    create_another_account_kb.button(
        text="Создать ещё ➕", callback_data="F_create")
    create_another_account_kb.button(
        text="Вернуться в кошелёк", callback_data="F_back_to_wallet")
    create_another_account_kb.adjust(1)
    return create_another_account_kb.as_markup()


# TODO Выбор счета
def choose_an_account_keyboard(user_id):
    choose_an_account_kb = InlineKeyboardBuilder()
    connection = family_finance_server.show_list_of_accounts(user_id=user_id)
    for list_account in connection:
        choose_an_account_kb.button(
            text=list_account.split('.')[1],
            callback_data=FAccountCallback(call_data=list_account, call='F_call').pack())
    choose_an_account_kb.button(text="Назад", callback_data="F_back_to_wallet")
    choose_an_account_kb.adjust(1)
    return choose_an_account_kb.as_markup()


def income_account_selection(user_id):
    income_account_selection_kb = InlineKeyboardBuilder()
    connection = family_finance_server.show_list_of_accounts(user_id=user_id)
    for list_account in connection:
        income_account_selection_kb.button(
            text=list_account.split('.')[1],
            callback_data=FAddIncomeCallback(call_data=list_account, call_add='F_call_add').pack())
    income_account_selection_kb.adjust(1)
    return income_account_selection_kb.as_markup()


def income_analysis_account(user_id):
    account_selection_for_analysis_kb = InlineKeyboardBuilder()
    connection = family_finance_server.show_list_of_accounts(user_id=user_id)
    for list_account in connection:
        account_selection_for_analysis_kb.button(
            text=list_account.split('.')[1],
            callback_data=FAnalysisIncomeCallback(call_data=list_account, call_analysis='F_call_analysis').pack())
    account_selection_for_analysis_kb.button(
        text="Назад",
        callback_data="F_back_to_wallet")
    account_selection_for_analysis_kb.adjust(1)
    return account_selection_for_analysis_kb.as_markup()


# TODO Добавить Доход/Расход
# Доход
def add_keyboard():
    add_kb = InlineKeyboardBuilder()
    add_kb.button(
        text="Расход", callback_data="F_consumption")
    add_kb.button(
        text="Доход", callback_data="F_income")
    add_kb.button(
        text="Вернуться в кошелёк", callback_data="F_back_to_wallet")
    add_kb.adjust(1)
    return add_kb.as_markup()


def select_account_for_expenses(user_id):
    select_account_for_expenses_kb = InlineKeyboardBuilder()
    connection = family_finance_server.show_list_of_accounts(user_id=user_id)
    for list_account in connection:
        select_account_for_expenses_kb.button(
            text=list_account.split('.')[1],
            callback_data=FAddConsumptionCallback(call_data=list_account, call_add='F_call_add').pack())
    select_account_for_expenses_kb.adjust(1)
    return select_account_for_expenses_kb.as_markup()


# TODO Создать ещё (Расходы)
def create_more_expenses_keyboard():
    create_more_expenses_kb = InlineKeyboardBuilder()
    create_more_expenses_kb.button(
        text="Добавить ещё ➕", callback_data="F_consumption")
    create_more_expenses_kb.button(
        text="Вернуться в кошелёк", callback_data="F_back_to_wallet")
    create_more_expenses_kb.adjust(1)
    return create_more_expenses_kb.as_markup()


# Расход
category_list = ['Продукты', 'Транспорт', 'Платежи', 'Развлечения', 'Другое']


def consumption_keyboard():
    consumption_kb = InlineKeyboardBuilder()
    for category_list_kb in category_list:
        consumption_kb.button(text=category_list_kb, callback_data=category_list_kb)
        consumption_kb.adjust(1)
    return consumption_kb.as_markup()


# TODO Создать ещё (Доходы)
def create_more_income_keyboard():
    create_more_expenses_kb = InlineKeyboardBuilder()
    create_more_expenses_kb.button(
        text="Добавить ещё ➕", callback_data="F_income")
    create_more_expenses_kb.button(
        text="Вернуться в кошелёк", callback_data="F_back_to_wallet")
    create_more_expenses_kb.adjust(1)
    return create_more_expenses_kb.as_markup()


# TODO Аналитика
def choice_of_analytics_keyboard():
    choice_of_analytics_kb = InlineKeyboardBuilder()
    choice_of_analytics_kb.button(
        text="По доходам", callback_data='F_by_income')
    choice_of_analytics_kb.button(
        text="По расходам", callback_data="F_on_expenses")
    choice_of_analytics_kb.button(
        text="Вернуться в кошелёк", callback_data="F_back_to_wallet")
    choice_of_analytics_kb.adjust(1)
    return choice_of_analytics_kb.as_markup()


def expense_analysis_account(user_id):
    account_selection_for_analysis_kb = InlineKeyboardBuilder()
    connection = family_finance_server.show_list_of_accounts(user_id=user_id)
    for list_account in connection:
        account_selection_for_analysis_kb.button(
            text=list_account.split('.')[1],
            callback_data=FAnalysisExpensesCallback(call_data=list_account, call_analysis='F_call_analysis').pack())
    account_selection_for_analysis_kb.button(
        text="Назад",
        callback_data="F_back_to_wallet")
    account_selection_for_analysis_kb.adjust(1)
    return account_selection_for_analysis_kb.as_markup()


def expenses_keyboard():
    expenses_kb = InlineKeyboardBuilder()
    expenses_kb.button(
        text="➡", callback_data="expenseforward_5")
    expenses_kb.button(
        text="Вернуться в кошелёк", callback_data="F_back_to_wallet")
    expenses_kb.adjust(1)
    return expenses_kb.as_markup()


def incomes_keyboard():
    income_kb = InlineKeyboardBuilder()
    income_kb.button(
        text="➡", callback_data="incomeforward_5")
    income_kb.button(
        text="Вернуться в кошелёк", callback_data="F_back_to_wallet")
    income_kb.adjust(1)
    return income_kb.as_markup()


# TODO Лимиты
def limits_keyboard():
    limits_kb = InlineKeyboardBuilder()
    limits_kb.button(
        text="Добавить лимит на категорию", callback_data='F_add_limit')
    limits_kb.button(
        text="Удалить лимит", callback_data="F_remove_limit")
    limits_kb.button(
        text="Вернуться в кошелёк", callback_data="F_back_to_wallet")
    limits_kb.adjust(1)
    return limits_kb.as_markup()


def withdrawal_of_invoice_for_limit(user_id):
    withdrawal_of_invoice_for_limit_kb = InlineKeyboardBuilder()
    connection = family_finance_server.show_list_of_accounts(user_id=user_id)
    for list_account in connection:
        withdrawal_of_invoice_for_limit_kb.button(
            text=list_account.split('.')[1],
            callback_data=FLimitsCallback(call_data=list_account, call_limits='F_call_limits').pack())
    withdrawal_of_invoice_for_limit_kb.adjust(1)
    return withdrawal_of_invoice_for_limit_kb.as_markup()


def creating_or_exiting_limits():
    creating_or_exiting_limits_kb = InlineKeyboardBuilder()
    creating_or_exiting_limits_kb.button(
        text="Добавить ещё ➕", callback_data="F_add_limit")
    creating_or_exiting_limits_kb.button(
        text="Вернуться в кошелёк", callback_data="F_back_to_wallet")
    creating_or_exiting_limits_kb.adjust(1)
    return creating_or_exiting_limits_kb.as_markup()


# Расход
category_list_limits = ['Продукты', 'Транспорт', 'Платежи', 'Развлечения', 'Другое']


def category_limits_keyboard():
    category_limits_kb = InlineKeyboardBuilder()
    for category_list_kb in category_list_limits:
        category_limits_kb.button(text=category_list_kb, callback_data=category_list_kb)
        category_limits_kb.adjust(1)
    return category_limits_kb.as_markup()


def deleting_a_limit(user_id):
    deleting_a_limit_kb = InlineKeyboardBuilder()
    connection = family_finance_server.show_list_of_accounts(user_id=user_id)
    for list_limit in connection:
        deleting_a_limit_kb.button(
            text=list_limit.split('.')[1],
            callback_data=FDelLimitsCallback(call_data=list_limit, call_dellimits='F_call_dellimits').pack())

    deleting_a_limit_kb.button(
        text="Назад",
        callback_data="F_back_to_wallet")

    deleting_a_limit_kb.adjust(1)
    return deleting_a_limit_kb.as_markup()


def del_limit(account_id):
    del_limit_kb = InlineKeyboardBuilder()
    connection = family_finance_server.list_of_limits(account_id=account_id)
    for category_limit in connection:
        del_limit_kb.button(text=category_limit.split(',')[1],
                            callback_data=FListDelLimitsCallback(call_data=category_limit,
                                                                 call_listdellimits='F_call_listdellimits').pack())
        del_limit_kb.adjust(1)
    return del_limit_kb.as_markup()
