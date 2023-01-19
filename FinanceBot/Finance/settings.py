from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from Finance.keyboards import *
from aiogram import F
from Finance.states import AddLimits
from FinanceServer.finance_connection import finance_server
from FinanceServer.finance_connection import FinanceServerConfig as Fsc

router = Router()


@router.callback_query(lambda settings_call: settings_call.data == "settings")
async def settings(query: CallbackQuery):
    await query.message.edit_text("Выберите:")
    await query.message.edit_reply_markup(settings_keyboard())


# Премиум
@router.callback_query(lambda get_premium_call: get_premium_call.data == "get_premium")
async def get_premium(query: CallbackQuery):
    await query.answer("В Разработке.")


# Добавление новой категории
@router.callback_query(lambda add_new_category_call: add_new_category_call.data == "add_new_category")
async def add_new_category(query: CallbackQuery):
    await query.answer("В Разработке.")


# Добавление новой валюты
@router.callback_query(lambda add_new_currency_call: add_new_currency_call.data == "add_new_currency")
async def add_new_currency(query: CallbackQuery):
    await query.answer("В Разработке.")


# Стереть все данные
@router.callback_query(lambda erase_all_data_call: erase_all_data_call.data == "erase_all_data")
async def erase_all_data(query: CallbackQuery):
    await query.answer("В Разработке.")
