import aiohttp
import asyncio
import os
import json
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from whitelist import whitelist
from utils import validate_imei, format_response
from redis_client import get_redis_client
from dotenv import load_dotenv

load_dotenv()

API_TOKEN: str= os.getenv('TELEGRAM_BOT_TOKEN')
BACKEND_URL: str = os.getenv('BACKEND_URL')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

@router.message(Command(commands=['start']))
async def send_welcome(message: types.Message) -> None:
    """
    Отправка приветственного сообщения
    """
    await message.reply("Отправьте мне IMEI для проверки.")

@router.message(lambda message: message.text and validate_imei(message.text))
async def check_imei(message: types.Message) -> None:
    """
    Проверка IMEI и отправка результата пользователю
    """
    user_id: int = message.from_user.id
    if user_id not in whitelist:
        await message.reply('У вас нет доступа к этому боту.')
        return
    
    imei: str = message.text
    redis = await get_redis_client()

    # Проверка кэша
    cached_response = await redis.get(imei)
    if cached_response:
        await message.reply(cached_response.decode('utf-8'))
        return
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://{BACKEND_URL}:8000/api/check-imei', json={'imei': imei}) as response:
            if response.status == 200:
                data = await response.json()
                str_data = format_response(data, imei)
                try:
                    await redis.set(imei, str_data)
                except Exception as e:
                    print(f"Error connecting to Redis: {e}")
                await message.reply(str_data)
            else:
                await message.reply('Ошибка при проверке IMEI.')

@router.message(lambda message: message.text and not validate_imei(message.text))
async def invalid_imei(message: types.Message) -> None:
    """
    Отправка сообщения об ошибке при неверном формате IMEI
    """
    await message.reply('Неверный формат IMEI.')

async def main() -> None:
    """
    Запуск бота
    """
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())