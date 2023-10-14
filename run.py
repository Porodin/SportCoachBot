import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

Token_API = "6645247048:AAFYx8UJ9A8oDyFnBVHbJ8uVntpBTyBYNEE"
bot = Bot(Token_API)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        f'Приветствую тебя, {message.from_user.first_name}! Я бот, который позволит тебе выбрать товар, по интересующей тебя категории в таких интернет-магазинах как:<b> <a href="https://www.sportmaster.ru"> Спортмастер</a></b>, <b> <a href="https://www.ozon.ru">Ozon</a></b>, <b> <a href="https://www.wildberries.ru">Wildberries</a></b>',
        parse_mode="HTML", disable_web_page_preview=True)

    firstb = types.InlineKeyboardButton(text='🙂да', callback_data='yes')
    secondb = types.InlineKeyboardButton(text='😔нет', callback_data='no')
    ikb = types.InlineKeyboardMarkup(inline_keyboard=[[firstb], [secondb]], row_width=2)

    await bot.send_message(chat_id=message.from_user.id, text='Открыть список категорий?', reply_markup=ikb)


@dp.callback_query(F.data == 'yes')
async def process_button_1_press(callback_query: types.CallbackQuery):
    if callback_query.message.text != 'yes':
        kb = [
            [
                types.KeyboardButton(text="гантели"),
                types.KeyboardButton(text="гири"),
                types.KeyboardButton(text="грифы")

            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Выберите категорию интересующего вас товара"
        )
        await callback_query.message.answer('Список всех категорий...', reply_markup=keyboard)

@dp.callback_query(F.data == 'no')
async def process_button_2_press(callback_query: CallbackQuery):
    if callback_query.message.text != 'no':
        await callback_query.message.answer(
            text='Значит в другой раз')


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls

    # And the run events dispatching
    await dp.start_polling(bot, skipe_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
