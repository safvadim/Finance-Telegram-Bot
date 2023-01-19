from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from FinanceFamily.family_keyboards import *
from aiogram import F
from FinanceFamily.family_states import *
from FinanceServer.family_finance_connection import family_finance_server
from FinanceServer.family_finance_connection import FamilyFinanceServerConfig as FFsc

router = Router()


@router.callback_query(lambda limits_call: limits_call.data == "F_limits")
async def limit(query: CallbackQuery):
    await query.message.edit_text("Выберите:")
    await query.message.edit_reply_markup(limits_keyboard())


# TODO FSM
@router.callback_query(lambda limits_call: limits_call.data == "F_add_limit")
async def add_limit(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    connection = family_finance_server.show_list_of_accounts(user_id=user_id)
    if not FFsc.show_list:
        await query.answer("Для начала создайте счёт!")
    else:
        await query.message.edit_text("Выберите счёт:\n\n"
                                      "Если хотите выйти нажмите /Cancel\n"
                                      "Или введите 'Отмена'")
        await query.message.edit_reply_markup(withdrawal_of_invoice_for_limit())
        await state.set_state(AddLimits.account_id)


@router.message(Command(commands=["Cancel"]))
@router.message(Text(text="Отмена"))
async def cancellation(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=creating_or_exiting_limits())


@router.callback_query(LimitsCallback.filter(F.call_limits == 'F_call_limits'))
async def add_limit(query: CallbackQuery, state: FSMContext):
    data = query.data.split('.')[0]
    data = data.split(':')[1]
    await state.update_data(account_id=data)
    await state.set_state(AddLimits.name_category)
    await query.message.edit_text(
        text="Выберите категорию:")
    await query.message.edit_reply_markup(category_limits_keyboard())


@router.callback_query(AddLimits.name_category)
async def add_limit_category(query: CallbackQuery, state: FSMContext):
    await state.update_data(name_category=query.data)
    await state.set_state(AddLimits.amount_limit)
    await query.message.edit_text("Установите сумму лимита:")


@router.message(AddLimits.amount_limit)
async def add_limit_amount(message: Message, state: FSMContext):
    if len(message.text) > 10:
        await message.answer("Не корректное число")
    elif message.text.isdigit():
        amount_record_float = float(message.text.replace(',', '.'))
        amount_record = round(amount_record_float, 2)
        await state.update_data(amount_limit=amount_record)
        data = await state.get_data()
        account_id_data = data['account_id']
        name_category_data = data['name_category']
        amount_limit_data = data['amount_limit']
        user_data = dict(account_id=account_id_data,
                         name_category=name_category_data,
                         amount_limit=amount_limit_data)
        connection_adding_limits = family_finance_server.adding_limits(data_user=user_data)
        await message.answer("Лимит добавлен!", reply_markup=creating_or_exiting_limits())
    else:
        try:
            amount_record_float = float(message.text.replace(',', '.'))
            amount_record = round(amount_record_float, 2)
            await state.update_data(amount_limit=amount_record)
            data = await state.get_data()
            account_id_data = data['account_id']
            name_category_data = data['name_category']
            amount_limit_data = data['amount_limit']
            user_data = dict(account_id=account_id_data,
                             name_category=name_category_data,
                             amount_limit=amount_limit_data)
            connection_adding_limits = family_finance_server.adding_limits(data_user=user_data)
            await message.answer("Лимит добавлен!", reply_markup=creating_or_exiting_limits())
        except ValueError:
            await message.answer("Неверный формат, введите ещё раз:")


# TODO Удаление лимита
@router.callback_query(lambda remove_limit_call: remove_limit_call.data == "F_remove_limit")
async def remove_limit(query: CallbackQuery):
    user_id = query.from_user.id
    connection = family_finance_server.show_list_of_accounts(user_id=user_id)
    if not FFsc.show_list:
        await query.answer("Для начала создайте счёт!")
    else:
        await query.message.edit_text("Выберите счёт.")
        await query.message.edit_reply_markup(deleting_a_limit())


@router.callback_query(DelLimitsCallback.filter(F.call_dellimits == 'F_call_dellimits'))
async def add_limit(query: CallbackQuery):
    data = query.data.split('.')[0]
    data = data.split(':')[1]
    connection = family_finance_server.list_of_limits(account_id=data)
    if not FFsc.category_limit:
        await query.answer("Нет лимитов для удаления!")
    else:
        await query.message.edit_text("Выберите лимит для удаления")
        await query.message.edit_reply_markup(del_limit())


@router.callback_query(F.data.in_(FFsc.category_limit))
async def test1(query: CallbackQuery):
    data = query.data.split(',')[0]
    connection = family_finance_server.limit_deletion(limit_deletion=data)
    await query.answer(f"Лимит удален!")
    await remove_limit(query)