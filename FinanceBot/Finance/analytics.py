from aiogram import Router, types
from aiogram.types import CallbackQuery
from Finance.keyboards import *
from aiogram import F
from FinanceServer.finance_connection import finance_server

router = Router()

ACCOUNT_ID = list()


@router.callback_query(lambda analytics_call: analytics_call.data == "analytics")
async def analytics(query: CallbackQuery):
    await query.message.edit_text("Выберите:")
    await query.message.edit_reply_markup(choice_of_analytics_keyboard())


@router.callback_query(lambda on_expenses_call: on_expenses_call.data == "on_expenses")
async def analyst_expense(query: CallbackQuery):
    user_id = query.from_user.id
    connection = finance_server.show_list_of_accounts(user_id=user_id)
    if not connection:
        await query.answer("Для начала создайте счёт!")
    else:
        await query.message.edit_text("Выберите счёт для анализа:")
        await query.message.edit_reply_markup(expense_analysis_account(user_id))


@router.callback_query(lambda by_income_call: by_income_call.data == "by_income")
async def revenue_analytics(query: CallbackQuery):
    user_id = query.from_user.id
    connection = finance_server.show_list_of_accounts(user_id=user_id)
    if not connection:
        await query.answer("Для начала создайте счёт!")
    else:
        await query.message.edit_text("Выберите счёт для анализа:")
        await query.message.edit_reply_markup(income_analysis_account(user_id))


@router.callback_query(AnalysisExpensesCallback.filter(F.call_analysis == 'call_analysis'))
async def withdrawal_from_expense(query: CallbackQuery):
    data = query.data.split('.')[0]
    data = data.split(':')[1]
    ACCOUNT_ID.append(int(data))
    connection = finance_server.cost_analytics(account_id=data)
    if not connection:
        await query.answer("У вас ещё нет расходов!")
    else:
        await query.message.edit_text(f"{connection}\n\nРасходы за месяц: /month"
                                      f"\nРасходы за квартал: /quarter\nРасходы за год: /year")
        await query.message.edit_reply_markup(expenses_keyboard())


@router.callback_query(F.data.startswith("expenseforward_"))
async def cost_pagination(query: CallbackQuery):
    global account_id
    page = int(query.data.split('_')[1])
    result = list()
    for account_id in ACCOUNT_ID:
        account_id = account_id
    connection = finance_server.cost_pagination(account_id=account_id, page=page)
    for json_list in connection['results']:
        category = json_list['category']
        title = json_list['title']
        date = '-'.join(json_list['date'].split('-')[::-1])
        amount_expenses = json_list['amount_expenses']
        conclusion = str(f"Категория: {category}\nНаименование: {title}\nЦена: {amount_expenses}\nДата: {date}")
        result.append(conclusion)
    list_of_expenses = '\n\n'.join(result)

    expenses_kb = InlineKeyboardBuilder()

    pagination_buttons = []

    if connection["previous"]:
        pagination_buttons.append(types.InlineKeyboardButton(text="⬅", callback_data=f"expenseforward_{page - 5}"))
    if connection["next"]:
        pagination_buttons.append(types.InlineKeyboardButton(text="➡", callback_data=f"expenseforward_{page + 5}"))

    expenses_kb.row(*pagination_buttons).row(types.InlineKeyboardButton
                                         (text="Вернуться в кошелёк", callback_data="back_to_wallet"))

    await query.message.edit_text(f"{list_of_expenses}\n\nРасходы за месяц: /month"
                                  f"\nРасходы за квартал: /quarter\nРасходы за год: /year")
    await query.message.edit_reply_markup(expenses_kb.as_markup())


@router.callback_query(AnalysisIncomeCallback.filter(F.call_analysis == 'call_analysis'))
async def withdrawal_from_income(query: CallbackQuery):
    data = query.data.split('.')[0]
    data = data.split(':')[1]
    ACCOUNT_ID.append(int(data))
    connection = finance_server.revenue_analytics(account_id=data)
    if not connection:
        await query.answer("У вас ещё нет доходов!")
    else:
        await query.message.edit_text(f"{connection}\n\nДоходы за месяц: /month"
                                      f"\nДоходы за квартал: /quarter\nДоходы за год: /year")
        await query.message.edit_reply_markup(incomes_keyboard())


@router.callback_query(F.data.startswith("incomeforward_"))
async def income_pagination(query: CallbackQuery):
    global account_id
    page = int(query.data.split('_')[1])
    result = list()
    for account_id in ACCOUNT_ID:
        account_id = account_id
    connection = finance_server.income_pagination(account_id=account_id, page=page)
    for json_list in connection['results']:
        source_of_income = json_list['source_of_income']
        amount_income = json_list['amount_income']
        date = '-'.join(json_list['date'].split('-')[::-1])
        conclusion = str(f"Источник дохода: {source_of_income}\nСумма: {amount_income}\nДата: {date}")
        result.append(conclusion)
    list_of_income = '\n\n'.join(result)

    incomes_kb = InlineKeyboardBuilder()

    pagination_buttons_income = []

    if connection["previous"]:
        pagination_buttons_income.append(
            types.InlineKeyboardButton(text="⬅", callback_data=f"incomeforward_{page - 5}"))
    if connection["next"]:
        pagination_buttons_income.append(
            types.InlineKeyboardButton(text="➡", callback_data=f"incomeforward_{page + 5}"))

    incomes_kb.row(*pagination_buttons_income).row(types.InlineKeyboardButton
                                         (text="Вернуться в кошелёк", callback_data="back_to_wallet"))

    await query.message.edit_text(f"{list_of_income}\n\nДоходы за месяц: /month"
                                  f"\nДоходы за квартал: /quarter\nДоходы за год: /year")
    await query.message.edit_reply_markup(incomes_kb.as_markup())







