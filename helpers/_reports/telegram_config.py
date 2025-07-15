import os
from datetime import datetime
# from telegram import Bot
from dotenv import load_dotenv
load_dotenv()

telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')


def format_dict(report_dict, has_errors):
    main_stat = report_dict["main"]
    data = report_dict["data"]

    # Main statistics
    message = f"📊 Main Stats:\n\n"
    message += f"Start: {main_stat['total_time']['start']}\n"
    message += f"Stop:  {main_stat['total_time']['stop']}\n" 
    message += f"Duration: {main_stat['total_time']['duration']}\n\n"
    message += f"Total products: {main_stat['count_of_products']}\n"
    message += f"New: {main_stat['stat']['counts']['new']}\n"
    message += f"Update: {main_stat['stat']['counts']['update']}\n\n"
    message += f"Has errors: {has_errors}\n\n\n"
    
    return message

    

async def send_message_to_telegram(report_dict, has_errors):
    message = format_dict(report_dict, has_errors)
    bot = Bot(token=telegram_bot_token)
    await bot.send_message(chat_id=telegram_chat_id, text=message)

    if has_errors:
        log_dir = os.path.join(os.getenv("LOGS_DIR"), "errors")
        today_date = datetime.now().strftime('%d_%m')
        log_filename = os.path.join(log_dir, f'log_{today_date}.log')
        
        with open(log_filename, 'rb') as file:
            await bot.send_document(chat_id=telegram_chat_id, document=file)