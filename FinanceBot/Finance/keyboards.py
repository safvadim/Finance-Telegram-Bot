from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from FinanceServer.finance_connection import FinanceServerConfig


class AccountCallback(CallbackData, prefix='account'):
    call_data: str
    call: str


class AddConsumptionCallback(CallbackData, prefix='add'):
    call_data: str
    call_add: str


class AddIncomeCallback(CallbackData, prefix='add_income'):
    call_data: str
    call_add: str


class AnalysisIncomeCallback(CallbackData, prefix='analysis_income'):
    call_data: str
    call_analysis: str


class AnalysisExpensesCallback(CallbackData, prefix='analysis_expenses'):
    call_data: str
    call_analysis: str


class LimitsCallback(CallbackData, prefix='limits'):
    call_data: str
    call_limits: str


class DelLimitsCallback(CallbackData, prefix='dellimits'):
    call_data: str
    call_dellimits: str


# TODO Старт
def start_keyboard():
    start_kb = InlineKeyboardBuilder()
    start_kb.button(
        text="Личный кошелек", callback_data="personal_account")
    start_kb.button(
        text="Семейный кошелек", callback_data="family_account")
    start_kb.button(
        text="Портфель", callback_data="portfolio")
    start_kb.adjust(1)
    return start_kb.as_markup()


# TODO Личный Кошелек
def personal_account_keyboard():
    personal_account_kb = InlineKeyboardBuilder()
    personal_account_kb.button(
        text="Счета 💰", callback_data="accounts")
    personal_account_kb.button(
        text="Добавить ✏", callback_data="add")
    personal_account_kb.button(
        text="Аналитика 📊", callback_data="analytics")
    personal_account_kb.button(
        text="Лимиты 🔒", callback_data="limits")
    personal_account_kb.button(
        text="Настройки ⚙", callback_data="settings")
    personal_account_kb.button(
        text="Главное меню", callback_data="main_menu")
    personal_account_kb.adjust(1)
    return personal_account_kb.as_markup()


# TODO Счет
def account_keyboard():
    account_kb = InlineKeyboardBuilder()
    account_kb.button(
        text="Создать ➕", callback_data="create")
    account_kb.button(
        text="Удалить ➖", callback_data="delete")
    account_kb.button(
        text="Назад в кошелёк", callback_data="back_to_wallet")
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
        text="Создать ещё ➕", callback_data="create")
    create_another_account_kb.button(
        text="Вернуться в кошелёк", callback_data="back_to_wallet")
    create_another_account_kb.adjust(1)
    return create_another_account_kb.as_markup()


# TODO Создать ещё (Расходы)
def create_more_expenses_keyboard():
    create_more_expenses_kb = InlineKeyboardBuilder()
    create_more_expenses_kb.button(
        text="Добавить ещё ➕", callback_data="consumption")
    create_more_expenses_kb.button(
        text="Вернуться в кошелёк", callback_data="back_to_wallet")
    create_more_expenses_kb.adjust(1)
    return create_more_expenses_kb.as_markup()


# TODO Создать ещё (Доходы)
def create_more_income_keyboard():
    create_more_expenses_kb = InlineKeyboardBuilder()
    create_more_expenses_kb.button(
        text="Добавить ещё ➕", callback_data="income")
    create_more_expenses_kb.button(
        text="Вернуться в кошелёк", callback_data="back_to_wallet")
    create_more_expenses_kb.adjust(1)
    return create_more_expenses_kb.as_markup()


# TODO Выбор счета
def choose_an_account_keyboard():
    choose_an_account_kb = InlineKeyboardBuilder()
    for list_account in FinanceServerConfig.show_list:
        choose_an_account_kb.button(
            text=list_account.split('.')[1],
            callback_data=AccountCallback(call_data=list_account, call='call').pack())
    choose_an_account_kb.adjust(1)
    return choose_an_account_kb.as_markup()


def select_account_for_expenses():
    select_account_for_expenses_kb = InlineKeyboardBuilder()
    for list_account in FinanceServerConfig.show_list:
        select_account_for_expenses_kb.button(
            text=list_account.split('.')[1],
            callback_data=AddConsumptionCallback(call_data=list_account, call_add='call_add').pack())
    select_account_for_expenses_kb.adjust(1)
    return select_account_for_expenses_kb.as_markup()


def income_account_selection():
    income_account_selection_kb = InlineKeyboardBuilder()
    for list_account in FinanceServerConfig.show_list:
        income_account_selection_kb.button(
            text=list_account.split('.')[1],
            callback_data=AddIncomeCallback(call_data=list_account, call_add='call_add').pack())
    income_account_selection_kb.adjust(1)
    return income_account_selection_kb.as_markup()


def income_analysis_account():
    account_selection_for_analysis_kb = InlineKeyboardBuilder()
    for list_account in FinanceServerConfig.show_list:
        account_selection_for_analysis_kb.button(
            text=list_account.split('.')[1],
            callback_data=AnalysisIncomeCallback(call_data=list_account, call_analysis='call_analysis').pack())
    account_selection_for_analysis_kb.button(
        text="Назад",
        callback_data="back_to_wallet")
    account_selection_for_analysis_kb.adjust(1)
    return account_selection_for_analysis_kb.as_markup()


def expense_analysis_account():
    account_selection_for_analysis_kb = InlineKeyboardBuilder()
    for list_account in FinanceServerConfig.show_list:
        account_selection_for_analysis_kb.button(
            text=list_account.split('.')[1],
            callback_data=AnalysisExpensesCallback(call_data=list_account, call_analysis='call_analysis').pack())
    account_selection_for_analysis_kb.button(
        text="Назад",
        callback_data="back_to_wallet")
    account_selection_for_analysis_kb.adjust(1)
    return account_selection_for_analysis_kb.as_markup()


def withdrawal_of_invoice_for_limit():
    withdrawal_of_invoice_for_limit_kb = InlineKeyboardBuilder()
    for list_account in FinanceServerConfig.show_list:
        withdrawal_of_invoice_for_limit_kb.button(
            text=list_account.split('.')[1],
            callback_data=LimitsCallback(call_data=list_account, call_limits='call_limits').pack())
    withdrawal_of_invoice_for_limit_kb.adjust(1)
    return withdrawal_of_invoice_for_limit_kb.as_markup()


def deleting_a_limit():
    deleting_a_limit_kb = InlineKeyboardBuilder()
    for list_limit in FinanceServerConfig.show_list:
        deleting_a_limit_kb.button(
            text=list_limit.split('.')[1],
            callback_data=DelLimitsCallback(call_data=list_limit, call_dellimits='call_dellimits').pack())

    deleting_a_limit_kb.button(
        text="Назад",
        callback_data="back_to_wallet")

    deleting_a_limit_kb.adjust(1)
    return deleting_a_limit_kb.as_markup()


# TODO Добавить Доход/Расход
# Доход
def add_keyboard():
    add_kb = InlineKeyboardBuilder()
    add_kb.button(
        text="Расход", callback_data="consumption")
    add_kb.button(
        text="Доход", callback_data="income")
    add_kb.button(
        text="Вернуться в кошелёк", callback_data="back_to_wallet")
    add_kb.adjust(1)
    return add_kb.as_markup()


# Расход
category_list = ['Продукты', 'Транспорт', 'Платежи', 'Развлечения', 'Другое']


def consumption_keyboard():
    consumption_kb = InlineKeyboardBuilder()
    for category_list_kb in category_list:
        consumption_kb.button(text=category_list_kb, callback_data=category_list_kb)
        consumption_kb.adjust(1)
    return consumption_kb.as_markup()

# Расход
category_list_limits = ['Продукты', 'Транспорт', 'Платежи', 'Развлечения', 'Другое']


def category_limits_keyboard():
    category_limits_kb = InlineKeyboardBuilder()
    for category_list_kb in category_list_limits:
        category_limits_kb.button(text=category_list_kb, callback_data=category_list_kb)
        category_limits_kb.adjust(1)
    return category_limits_kb.as_markup()


# TODO Аналитика
def choice_of_analytics_keyboard():
    choice_of_analytics_kb = InlineKeyboardBuilder()
    choice_of_analytics_kb.button(
        text="По доходам", callback_data='by_income')
    choice_of_analytics_kb.button(
        text="По расходам", callback_data="on_expenses")
    choice_of_analytics_kb.button(
        text="Вернуться в кошелёк", callback_data="back_to_wallet")
    choice_of_analytics_kb.adjust(1)
    return choice_of_analytics_kb.as_markup()


def expenses_keyboard():
    expenses_kb = InlineKeyboardBuilder()
    expenses_kb.button(
        text="➡", callback_data="expenseforward_5")
    expenses_kb.button(
        text="Вернуться в кошелёк", callback_data="back_to_wallet")
    expenses_kb.adjust(1)
    return expenses_kb.as_markup()


def incomes_keyboard():
    income_kb = InlineKeyboardBuilder()
    income_kb.button(
        text="➡", callback_data="incomeforward_5")
    income_kb.button(
        text="Вернуться в кошелёк", callback_data="back_to_wallet")
    income_kb.adjust(1)
    return income_kb.as_markup()


# TODO Лимиты
def limits_keyboard():
    limits_kb = InlineKeyboardBuilder()
    limits_kb.button(
        text="Добавить лимит на категорию", callback_data='add_limit')
    limits_kb.button(
        text="Удалить лимит", callback_data="remove_limit")
    limits_kb.button(
        text="Вернуться в кошелёк", callback_data="back_to_wallet")
    limits_kb.adjust(1)
    return limits_kb.as_markup()


def creating_or_exiting_limits():
    creating_or_exiting_limits_kb = InlineKeyboardBuilder()
    creating_or_exiting_limits_kb.button(
        text="Добавить ещё ➕", callback_data="add_limit")
    creating_or_exiting_limits_kb.button(
        text="Вернуться в кошелёк", callback_data="back_to_wallet")
    creating_or_exiting_limits_kb.adjust(1)
    return creating_or_exiting_limits_kb.as_markup()


def del_limit():
    del_limit_kb = InlineKeyboardBuilder()
    for category_limit in FinanceServerConfig.category_limit:
        del_limit_kb.button(text=category_limit.split(',')[1], callback_data=category_limit)
        del_limit_kb.adjust(1)
    return del_limit_kb.as_markup()


# TODO Настройки
def settings_keyboard():
    settings_kb = InlineKeyboardBuilder()
    settings_kb.button(
        text="Получить Премиум", callback_data='get_premium')
    settings_kb.button(
        text="Добавить новую категорию", callback_data="add_new_category")
    settings_kb.button(
        text="Добавить новую валюту", callback_data="add_new_currency")
    settings_kb.button(
        text="Стереть все данные", callback_data="erase_all_data")
    settings_kb.button(
        text="Вернуться в кошелёк", callback_data="back_to_wallet")
    settings_kb.adjust(1)
    return settings_kb.as_markup()

