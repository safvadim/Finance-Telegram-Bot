from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from FinanceFamily.family_keyboards import *
from FinanceFamily.family_states import *
from aiogram import F
from FinanceServer.family_finance_connection import family_finance_server

router = Router()


# TODO Добавить
@router.callback_query(lambda F_add_call: F_add_call.data == "F_add")
async def family_add(query: CallbackQuery):
    await query.message.edit_text("Выберите действие:")
    await query.message.edit_reply_markup(add_keyboard())


# TODO FSM Добавление расходов
@router.callback_query(lambda F_consumption_call: F_consumption_call.data == "F_consumption")
async def adding_costs(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    connection = family_finance_server.show_list_of_accounts(user_id=user_id)
    if not connection:
        await query.answer("Для начала создайте счёт!")
    else:
        await query.message.edit_text("Пожалуйста, выберите счёт:\n\n"
                                      "Если хотите выйти нажмите /Cancel\n"
                                      "Или введите 'Отмена'")
        await query.message.edit_reply_markup(select_account_for_expenses(user_id))
        await state.set_state(FAddExpenses.account_id)


@router.message(Command(commands=["Cancel"]))
@router.message(Text(text="Отмена"))
async def cancellation(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=create_more_expenses_keyboard())


@router.callback_query(FAddConsumptionCallback.filter(F.call_add == 'F_call_add'))
async def account_id_entry(query: CallbackQuery, state: FSMContext):
    data = query.data.split('.')[0]
    data = data.split(':')[1]
    await state.update_data(account_id=int(data))
    await state.set_state(FAddExpenses.category)
    await query.message.edit_text(
        text="Выберите категорию:")
    await query.message.edit_reply_markup(consumption_keyboard())


@router.callback_query(FAddExpenses.category, F.data.as_(str(category_list)))
async def category_entry(query: CallbackQuery, state: FSMContext):
    await state.update_data(category=query.data)
    await state.set_state(FAddExpenses.title)
    await query.message.answer("Введите название покупки:")


@router.message(FAddExpenses.title)
async def title_entry(message: Message, state: FSMContext):
    if len(message.text) > 50:
        await message.answer("Слишком длинное название, попробуйте ещё раз:")
    else:
        await state.update_data(title=message.text)
        await state.set_state(FAddExpenses.amount_expenses)
        await message.answer("Спасибо. Введите сумму:")


@router.message(FAddExpenses.amount_expenses)
async def amount_entry(message: Message, state: FSMContext):
    if len(message.text) > 10:
        await message.answer("Не корректное число")
    elif message.text.isdigit():
        amount_record_float = float(message.text.replace(',', '.'))
        amount_record = round(amount_record_float, 2)
        await state.update_data(amount_expenses=amount_record)
        data = await state.get_data()
        category_data = data['category']
        title_data = data['title']
        amount_expenses_data = data['amount_expenses']
        account_id_data = data['account_id']
        date = f"{message.date.day}.{message.date.month}.{message.date.year}"
        user_data = dict(category=category_data,
                         title=title_data,
                         amount_expenses=amount_expenses_data,
                         account_id=account_id_data,
                         date=date)
        connection_limit_expenses = family_finance_server.category_amount(account_id=data['account_id'],
                                                                          category=data['category'])
        connection_limit = family_finance_server.amount_category_limit(account_id=data['account_id'],
                                                                       name_category=data['category'])
        if connection_limit is None:
            connection = family_finance_server.adding_an_expense(data_user=user_data)
            await message.answer(text=f"{connection}", reply_markup=create_more_expenses_keyboard())
        else:
            res_sum = connection_limit_expenses + data['amount_expenses']
            if res_sum > connection_limit:
                await message.answer("Превышен лимит!")
                connection = family_finance_server.adding_an_expense(data_user=user_data)
                await message.answer(text=f"{connection}", reply_markup=create_more_expenses_keyboard())
            else:
                connection = family_finance_server.adding_an_expense(data_user=user_data)
                await message.answer(text=f"{connection}", reply_markup=create_more_expenses_keyboard())
    else:
        try:
            amount_record_float = float(message.text.replace(',', '.'))
            amount_record = round(amount_record_float, 2)
            await state.update_data(amount_expenses=amount_record)
            data = await state.get_data()
            category_data = data['category']
            title_data = data['title']
            amount_expenses_data = data['amount_expenses']
            account_id_data = data['account_id']
            date = f"{message.date.day}.{message.date.month}.{message.date.year}"
            user_data = dict(category=category_data,
                             title=title_data,
                             amount_expenses=amount_expenses_data,
                             account_id=account_id_data,
                             date=date)
            connection_limit_expenses = family_finance_server.category_amount(account_id=data['account_id'],
                                                                              category=data['category'])
            connection_limit = family_finance_server.amount_category_limit(account_id=data['account_id'],
                                                                           name_category=data['category'])
            if connection_limit is None:
                connection = family_finance_server.adding_an_expense(data_user=user_data)
                await message.answer(text=f"{connection}", reply_markup=create_more_expenses_keyboard())
            else:
                res_sum = connection_limit_expenses + data['amount_expenses']
                if res_sum > connection_limit:
                    await message.answer("Превышен лимит!")
                    connection = family_finance_server.adding_an_expense(data_user=user_data)
                    await message.answer(text=f"{connection}", reply_markup=create_more_expenses_keyboard())
                else:
                    connection = family_finance_server.adding_an_expense(data_user=user_data)
                    await message.answer(text=f"{connection}", reply_markup=create_more_expenses_keyboard())
        except ValueError:
            await message.answer("Неверный формат, введите еще раз:")


# TODO FSM Доход
@router.callback_query(lambda income_call: income_call.data == "F_income")
async def add_income(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    connection = family_finance_server.show_list_of_accounts(user_id=user_id)
    if not connection:
        await query.answer("Для начала создайте счёт!")
    else:
        await query.message.edit_text("Пожалуйста, выберите счёт:")
        await query.message.edit_reply_markup(income_account_selection(user_id))
        await state.set_state(FAddIncome.account_id)


@router.message(Command(commands=["Cancel"]))
@router.message(Text(text="Отмена"))
async def cancellation(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=create_more_income_keyboard())


@router.callback_query(FAddIncome.account_id, FAddIncomeCallback.filter(F.call_add == 'F_call_add'))
async def account_id_record(query: CallbackQuery, state: FSMContext):
    data = query.data.split('.')[0]
    data = data.split(':')[1]
    await state.update_data(account_id=int(data))
    await state.set_state(FAddIncome.source_of_income)
    await query.message.edit_text(
        text="Введите источник дохода:")


@router.message(FAddIncome.source_of_income)
async def source_of_income_record(message: Message, state: FSMContext):
    if len(message.text) > 10:
        await message.answer("Недопустимая длинна текста, введите ещё раз:")
    else:
        await state.update_data(source_of_income=message.text)
        await state.set_state(FAddIncome.amount_income)
        await message.answer("Спасибо. Введите сумму:")


@router.message(FAddIncome.amount_income)
async def source_of_income(message: Message, state: FSMContext):
    if len(message.text) > 10:
        await message.answer("Не корректное число, введите ещё раз:")
    elif message.text.isdigit():
        amount_record_float = float(message.text.replace(',', '.'))
        amount_record = round(amount_record_float, 2)
        await state.update_data(amount_income=amount_record)
        data = await state.get_data()
        source_of_income_data = data['source_of_income']
        amount_income_data = data['amount_income']
        account_id_data = data['account_id']
        date = f"{message.date.day}.{message.date.month}.{message.date.year}"
        user_data = dict(source_of_income=source_of_income_data,
                         amount_income=amount_income_data,
                         account_id=account_id_data,
                         date=date)
        connection = family_finance_server.adding_income(data_user=user_data)
        await message.answer(text=f"Ваш доход добавлен!", reply_markup=create_more_income_keyboard())
    else:
        try:
            amount_record_float = float(message.text.replace(',', '.'))
            amount_record = round(amount_record_float, 2)
            await state.update_data(amount_income=amount_record)
            data = await state.get_data()
            source_of_income_data = data['source_of_income']
            amount_income_data = data['amount_income']
            account_id_data = data['account_id']
            date = f"{message.date.day}.{message.date.month}.{message.date.year}"
            user_data = dict(source_of_income=source_of_income_data,
                             amount_income=amount_income_data,
                             account_id=account_id_data,
                             date=date)
            connection = family_finance_server.adding_income(data_user=user_data)
            await message.answer(text=f"Ваш доход добавлен!", reply_markup=create_more_income_keyboard())
        except ValueError:
            await message.answer("Неверный формат, введите ещё раз:")