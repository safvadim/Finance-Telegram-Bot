import secrets

from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import F

from Finance.accounts import welcome
from Finance.keyboards import start_keyboard
from FinanceFamily.family_keyboards import *
from FinanceFamily.family_states import *
from FinanceServer.family_finance_connection import family_finance_server
from FinanceServer.family_finance_connection import FamilyFinanceServerConfig as Fsc
from Finance.analytics import ACCOUNT_ID

router = Router()


# TODO Верификация
@router.callback_query(lambda family_account_call: family_account_call.data == "family_account")
async def family_user_verification(query: CallbackQuery):
    user_id = query.from_user.id
    connection = family_finance_server.user_verification(user_id=user_id)
    if connection == 'Input':
        connection_input = family_finance_server.show_all_family_accounts(user_id=user_id)
        await query.message.edit_text(f"{connection_input}")
        await query.message.edit_reply_markup(family_account_keyboard())
    else:
        await query.message.edit_text("Выберите:")
        await query.message.edit_reply_markup(family_wallet_entry())


@router.callback_query(lambda F_create_wallet_call: F_create_wallet_call.data == "F_create_wallet")
async def family_user_create(query: CallbackQuery):
    token = secrets.token_hex(16)
    user_id = query.from_user.id
    full_name = query.from_user.full_name
    date = f"{query.message.date.day}.{query.message.date.month}.{query.message.date.year}"
    user_data = dict(user_id=f"F{user_id}", full_name=full_name, token=token, date=date)
    family_data = dict(family_user_id=f"F{user_id}", user_id=user_id, full_name=full_name)
    connection = family_finance_server.wallet_creation(user_data=user_data, family_data=family_data)
    await query.message.answer(f"{connection}\nВаш токен:\n{token}")
    await family_user_verification(query)


# TODO Вернуться в старт
@router.callback_query(lambda F_main_menu_call: F_main_menu_call.data == "F_main_menu")
async def return_to_start(query: CallbackQuery):
    hour = int(query.message.date.astimezone().hour)
    await query.message.edit_text(f"{welcome(hour)}<b>{query.from_user.full_name}!</b>")
    await query.message.edit_reply_markup(start_keyboard())


@router.callback_query(lambda F_input_call: F_input_call.data == "F_input")
async def input_user(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text("Введите код")
    await state.set_state(UserToken.token)


@router.message(UserToken.token)
async def user_token(message: Message, state: FSMContext):
    if len(message.text) > 32 or len(message.text) < 32:
        await message.answer("Неверный формат:")
    else:
        await state.update_data(token=message.text)
        user_id = message.from_user.id
        full_name = message.from_user.full_name
        data = await state.get_data()
        token = data['token']
        family_data = dict(user_id=user_id, full_name=full_name)
        connection = family_finance_server.search_by_token(token=token, family_data=family_data)
        await message.answer(f"{connection}")


# TODO Функции счета
@router.callback_query(lambda account_call: account_call.data == "F_accounts")
async def counting_functions(query: CallbackQuery):
    await query.message.edit_text(f"Выберите действие:")
    await query.message.edit_reply_markup(account_keyboard())


# TODO FSM Создание счета
@router.callback_query(lambda family_create_call: family_create_call.data == "F_create")
async def creating_an_account(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text("Пожалуйста, выберите валюту:\n\n"
                                  "Если хотите выйти нажмите /Cancel\n"
                                  "Или введите 'Отмена'")
    await query.message.edit_reply_markup(list_of_currencies_keyboard())
    await state.set_state(FCreatingAnAccount.currency)


# TODO Отмена
@router.message(Command(commands=["Cancel"]))
@router.message(Text(text="Отмена"))
async def cancellation(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=create_another_account_keyboard())


@router.callback_query(FCreatingAnAccount.currency, F.data.as_(str(currency)))
async def account_entry(query: CallbackQuery, state: FSMContext):
    await state.update_data(currency=query.data)
    await state.set_state(FCreatingAnAccount.name_currency)
    await query.message.edit_text(
        text="Введите название счёта:")


@router.message(FCreatingAnAccount.name_currency)
async def account_name_entry(message: Message, state: FSMContext):
    if len(message.text) > 10:
        await message.answer("Слишком длинное название, введите другое:")
    else:
        await state.update_data(name_currency=message.text)
        await state.set_state(FCreatingAnAccount.balance)
        await message.answer(text="Спасибо. Теперь введите сумму средств на счёте:")


@router.message(FCreatingAnAccount.balance)
async def amount_entry(message: Message, state: FSMContext):
    if len(message.text) > 10:
        await message.answer("Не корректное число")
    elif message.text.isdigit():
        amount_record_float = float(message.text.replace(',', '.'))
        amount_record = round(amount_record_float, 2)
        await state.update_data(balance=amount_record)
        data = await state.get_data()
        user_id = message.from_user.id
        currency_data = data['currency']
        name_currency_data = data['name_currency']
        balance_data = data['balance']
        user_data = dict(
                         currency=currency_data,
                         account_name=name_currency_data,
                         amount_check=balance_data)
        connection = family_finance_server.creating_an_account(user_id=user_id, user_data=user_data)
        await message.answer(text=f"Поздравляем, ваш счёт создан!", reply_markup=create_another_account_keyboard())
    else:
        try:
            amount_record_float = float(message.text.replace(',', '.'))
            amount_record = round(amount_record_float, 2)
            await state.update_data(balance=amount_record)
            data = await state.get_data()
            user_id = message.from_user.id
            currency_data = data['currency']
            name_currency_data = data['name_currency']
            balance_data = data['balance']
            user_data = dict(
                             currency=currency_data,
                             account_name=name_currency_data,
                             amount_check=balance_data)
            connection = family_finance_server.creating_an_account(user_id=user_id, user_data=user_data)
            await message.answer(text=f"Поздравляем, ваш счёт создан!", reply_markup=create_another_account_keyboard())
        except ValueError:
            await message.answer("Неверный формат, введите ещё раз:")


@router.callback_query(lambda back: back.data == "F_back_to_wallet")
async def back_to_wallet(query: CallbackQuery):
    user_id = query.from_user.id
    connection = family_finance_server.show_all_family_accounts(user_id=user_id)
    await query.message.edit_text(f"{connection}")
    await query.message.edit_reply_markup(family_account_keyboard())


# TODO Удаление счета
@router.callback_query(lambda family_delete_call: family_delete_call.data == "F_delete")
async def account_selection(query: CallbackQuery):
    user_id = query.from_user.id
    connection = family_finance_server.show_list_of_accounts(user_id=user_id)
    if not connection:
        await query.answer("Нет счёта для удаления!")
        await family_user_verification(query)
    else:
        await query.message.edit_text("Выберите счёт для удаления:")
        await query.message.edit_reply_markup(choose_an_account_keyboard(user_id))


@router.callback_query(lambda back_to_wallet_call: back_to_wallet_call.data == "F_back_to_wallet")
async def back_to_account(query: CallbackQuery):
    ACCOUNT_ID.clear()
    await family_user_verification(query)


@router.callback_query(FAccountCallback.filter(F.call == 'F_call'))
async def delete_accounts(query: CallbackQuery):
    get_id = query.data.split('.')[0]
    get_id = get_id.split(':')[1]
    connection = family_finance_server.account_deletion(account_deletion=get_id)
    await query.answer("Счёт удален!")
    await account_selection(query)




