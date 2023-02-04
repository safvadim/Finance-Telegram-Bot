from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import F
from Finance.keyboards import *
from Finance.states import CreatingAnAccount
from FinanceServer.finance_connection import finance_server
from Finance.analytics import ACCOUNT_ID

router = Router()


# TODO Приветствие
def welcome(hour: int):
    night = 0 <= hour <= 6
    morning = 6 <= hour <= 12
    day = 12 <= hour <= 18
    evening = 18 <= hour <= 24
    if night:
        return f"🌒Доброй ночи, "
    if morning:
        return f"☀Доброе утро, "
    if day:
        return f"☀Добрый день, "
    if evening:
        return f"🌖Добрый вечер, "
    else:
        return f"Привет, "


# TODO Старт
@router.message(Command(commands=["start"]))
async def command_start(message: Message):
    hour = str(message.date.astimezone().hour)
    if hour[0] == '0':
        hour = int(hour[1:])
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    date = f"{message.date.day}.{message.date.month}.{message.date.year}"
    user_data = dict(user_id=user_id, full_name=full_name, date=date)
    connection = finance_server.user_verification(user_id=user_id, user_data=user_data)
    await message.answer(f"{welcome(int(hour))}<b>{message.from_user.full_name}!</b>",
                         reply_markup=start_keyboard())


# TODO Счет
@router.callback_query(lambda personal_account_call: personal_account_call.data == "personal_account")
async def personal_account(query: CallbackQuery):
    user_id = query.from_user.id
    connection = finance_server.show_all_accounts(user_id=user_id)
    await query.message.edit_text(f"{connection}")
    await query.message.edit_reply_markup(personal_account_keyboard())


# TODO Вернуться в старт
@router.callback_query(lambda main_menu_call: main_menu_call.data == "main_menu")
async def return_to_start(query: CallbackQuery):
    hour = int(query.message.date.astimezone().hour)
    await query.message.edit_text(f"{welcome(hour)}<b>{query.from_user.full_name}!</b>")
    await query.message.edit_reply_markup(start_keyboard())


# TODO Функции счета
@router.callback_query(lambda account_call: account_call.data == "accounts")
async def counting_functions(query: CallbackQuery):
    await query.message.edit_text(f"Выберите действие:")
    await query.message.edit_reply_markup(account_keyboard())


# TODO FSM Создание счета
@router.callback_query(lambda create_call: create_call.data == "create")
async def creating_an_account(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text("Пожалуйста, выберите валюту:\n\n"
                                  "Если хотите выйти нажмите /Cancel\n"
                                  "Или введите 'Отмена'")
    await query.message.edit_reply_markup(list_of_currencies_keyboard())
    await state.set_state(CreatingAnAccount.currency)


# TODO Отмена
@router.message(Command(commands=["Cancel"]))
@router.message(Text(text="Отмена"))
async def cancellation(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=create_another_account_keyboard())


@router.callback_query(CreatingAnAccount.currency, F.data.as_(str(currency)))
async def account_entry(query: CallbackQuery, state: FSMContext):
    await state.update_data(currency=query.data)
    await state.set_state(CreatingAnAccount.name_currency)
    await query.message.edit_text(
        text="Введите название счёта:")


@router.message(CreatingAnAccount.name_currency)
async def account_name_entry(message: Message, state: FSMContext):
    if len(message.text) > 10:
        await message.answer("Слишком длинное название, введите другое:")
    else:
        await state.update_data(name_currency=message.text)
        await state.set_state(CreatingAnAccount.balance)
        await message.answer(text="Спасибо. Теперь введите сумму средств на счёте:")


@router.message(CreatingAnAccount.balance)
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
        user_data = dict(user=user_id,
                         currency=currency_data,
                         account_name=name_currency_data,
                         amount_check=balance_data)
        connection = finance_server.creating_an_account(user_data=user_data)
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
            user_data = dict(user=user_id,
                             currency=currency_data,
                             account_name=name_currency_data,
                             amount_check=balance_data)
            connection = finance_server.creating_an_account(user_data=user_data)
            await message.answer(text=f"Поздравляем, ваш счёт создан!", reply_markup=create_another_account_keyboard())
        except ValueError:
            await message.answer("Неверный формат, введите ещё раз:")


@router.callback_query(lambda back: back.data == "back_wallet")
async def back_to_wallet(query: CallbackQuery):
    user_id = query.from_user.id
    connection = finance_server.show_all_accounts(user_id=user_id)
    await query.message.edit_text(f"{connection}")
    await query.message.edit_reply_markup(personal_account_keyboard())


# TODO Удаление счета
@router.callback_query(lambda delete_call: delete_call.data == "delete")
async def account_selection(query: CallbackQuery):
    user_id = query.from_user.id
    connection = finance_server.show_list_of_accounts(user_id=user_id)
    if not connection:
        await query.answer("Нет счёта для удаления!")
        await personal_account(query)
    else:
        await query.message.edit_text("Выберите счёт для удаления:")
        await query.message.edit_reply_markup(choose_an_account_keyboard(user_id))


@router.callback_query(lambda back_to_wallet_call: back_to_wallet_call.data == "back_to_wallet")
async def back_to_account(query: CallbackQuery):
    ACCOUNT_ID.clear()
    await personal_account(query)


@router.callback_query(AccountCallback.filter(F.call == 'call'))
async def delete_accounts(query: CallbackQuery):
    get_id = query.data.split('.')[0]
    get_id = get_id.split(':')[1]
    connection = finance_server.account_deletion(account_deletion=get_id)
    await query.answer("Счёт удален!")
    await account_selection(query)
