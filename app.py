import os
from dotenv import load_dotenv
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
from HTMLParser import HTMLParser

load_dotenv()
CHAT_BOT_TOKEN = os.getenv("CHAT_BOT_TOKEN")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot_token = CHAT_BOT_TOKEN
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# URL to monitor
url = "https://www.smartsheet.com/careers-list?location=Bellevue%2C+WA%2C+USA&department=Engineering+-+Developers&position="

# Dictionary to store chat IDs and their associated URLs
chat_ids_urls = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Get the chat ID
    chat_id = message.chat.id

    # Add the chat ID to the dictionary with the URL to monitor
    chat_ids_urls[chat_id] = url

    await message.reply("Monitoring has started!")


async def check_website():
    while True:
        try: 
            for chat_id, data in chat_ids_urls.items():
                    url = data['url']
                    previous_data = data.get('previous_data')

                    # Fetch the HTML content and parse the dictionary
                    parser = HTMLParser(url)
                    current_data = parser.parse_html()

                    # Check for changes in the parsed dictionary
                    if previous_data is not None:
                        added_titles = [job['Job Title'] for job in current_data if job not in previous_data]
                        if added_titles:
                            image_url = 'https://resourseas.com/wp-content/uploads/2021/01/Job-Openings-we-are-hiring-1.jpg'
                            added_titles_str = "\n".join(added_titles)
                            message = f"Website has been updated!\n\nAdded titles:\n{added_titles_str}"
                            # Changes detected, send a message to the chat ID
                            await bot.send_message(chat_id=chat_id, photo=image_url, caption=message)

                    # Update the parsed dictionary for the chat ID and position
                    data['previous_data'] = current_data
                    chat_ids_urls[chat_id] = data

                    await asyncio.sleep(300)

        except Exception as e:
                logging.error(f"An error occurred while checking the website: {str(e)}")

                await asyncio.sleep(100)

@dp.message_handler(commands=['send_image'])
async def send_image(message: types.Message):
    image_url = 'https://motivationaldiaries.com/wp-content/uploads/2016/05/dontgiveup.jpg'
    
    # Send the image to the user
    await bot.send_photo(chat_id=message.chat.id, photo=image_url, caption='You will succeed 💎')

@dp.message_handler(commands=['getdata'])
async def get_data_command(message: types.Message):
    # Create a custom keyboard with two options: Smartsheet and Remitly
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('🟦 Smartsheet', '🤝 Remitly')

    # Send the menu message with the custom keyboard
    await message.answer("Choose a company:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ['🟦 Smartsheet', '🤝 Remitly'])
async def handle_company_selection(message: types.Message):
    company = message.text.lower()

    if company == '🟦 smartsheet':
        url = "https://www.smartsheet.com/careers-list?location=Bellevue%2C+WA%2C+USA&department=Engineering+-+Developers&position="
    elif company == '🤝 remitly':
        url = "https://careers.remitly.com/all-open-jobs/?team=engineering"
    else:
        return  # Invalid company, do nothing

    parser = HTMLParser(url)
    data = parser.parse_html()

    if len(data) > 0:
        message_text = ""
        number_in_order = 1
        for item in data:
            job_title = item['Job Title']
            department = item['Department']
            location = item['Location']
            job_link = item['Job Link']
            item_text = f"*🟦 {number_in_order}. Job Title: {job_title}\n*" \
                        f"Department: {department}\n" \
                        f"Location: {location}\n" \
                        f"Job Link: {job_link}\n\n"
            message_text += item_text
            number_in_order += 1

        # Check if message_text exceeds 4096 characters
        if len(message_text) <= 4096:
            await message.answer(message_text, parse_mode=types.ParseMode.MARKDOWN)
        else:
            # Divide message_text into multiple messages
            while message_text:
                await message.answer(message_text[:4096], parse_mode=types.ParseMode.MARKDOWN)
                message_text = message_text[4096:]
    else:
        await message.answer("Sorry, no available positions for now.")


# @dp.message_handler(commands=['getdata'])
# async def get_data_command(message: types.Message):

#     parser = HTMLParser(url)
#     data = parser.parse_html()

#     if len(data) > 0:
#         message_text = ""
#         number_in_order = 1
#         for item in data:
#             job_title = item['Job Title']
#             department = item['Department']
#             location = item['Location']
#             job_link = item['Job Link']
#             item_text = f"*🟦 {number_in_order}. Job Title: {job_title}\n*" \
#                         f"Department: {department}\n" \
#                         f"Location: {location}\n" \
#                         f"Job Link: {job_link}\n\n"
#             message_text += item_text
#             number_in_order += 1

#         # Check if message_text exceeds 4096 characters
#         if len(message_text) <= 4096:
#             await message.answer(message_text, parse_mode=types.ParseMode.MARKDOWN)
#         else:
#             # Divide message_text into multiple messages
#             while message_text:
#                 await message.answer(message_text[:4096], parse_mode=types.ParseMode.MARKDOWN)
#                 message_text = message_text[4096:]
#     else:
#         await message.answer("Sorry, no available positions for now.")


async def start_bot():
    try:
        await dp.start_polling()
        asyncio.create_task(check_website())
        await asyncio.Event().wait()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start_bot())
