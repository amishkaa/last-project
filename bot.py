import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile

TOKEN = '6993062188:AAFPh2dmpWWSPodhgXFiR8Sxz8W1cY0MsHI'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message(Command('start'))
async def start(message: Message):
    user_name = message.from_user.first_name
    nl = '\n'
    await message.answer(f'Привет, {user_name}!{nl}'
                         f'Наш бот много чего умеет:{nl}'
                         f'/url - ссылка на наш сайт!{nl}'
                         f'/play - сыграй в игру{nl}'
                         f'/mem - увидь мем!(к сожалению, на данный момент был придуман лишь один)')


@dp.message(Command('play'))
async def game(message: Message):
    await message.answer(f'Считай, что у нас тут казино.'
                         f'Сейчас будем играть в баскетбол. Мяч попал в кольцо - ты выйграл. Нет - значит нет.')
    x = await message.answer_dice(DiceEmoji.BASKETBALL)
    if x.dice.value == 5 or x.dice.value == 4:
        await message.answer(f'Ты выйграл!')
    else:
        await message.answer(f'Упс')


@dp.message(Command('url'))
async def url(message: Message):
    url = ...
    await message.answer(f'Вот ссылка на наш прекрасный сайт! {url}')


@dp.message(Command('mem'))
async def upload_photo(message: Message):
    file_ids = []
    with open("photo.png", "rb") as image_from_buffer:
        result = await message.answer_photo(
            BufferedInputFile(
                image_from_buffer.read(),
                filename="image.jpg"
            ),
            caption="Единственный мем, который мы придумали"
        )
        file_ids.append(result.photo[-1].file_id)


@dp.message()
async def eho(message: Message):
    await message.answer('Пиши что сказано')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())