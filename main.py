import ptbot
import os
from pytimeparse import parse
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')
BOT = ptbot.Bot(TG_TOKEN)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, chat_id, message_id, message):
    BOT.update_message(
        chat_id, message_id,
        f'Осталось {secs_left} секун\n{render_progressbar(
            parse(message),
            parse(message) - secs_left
        )}')


def reply(chat_id, message):
    message_id = BOT.send_message(
        chat_id,
        'Запускаю таймер'
    )
    BOT.create_timer(
        parse(message),
        choose,
        chat_id=chat_id,
        message=message
    )
    BOT.create_countdown(
        parse(message),
        notify_progress,
        message_id=message_id,
        chat_id=chat_id,
        message=message
    )


def choose(chat_id, message):
    message = 'Время вышло'
    BOT.send_message(
        chat_id,
        message
    )


def main():
    BOT.reply_on_message(reply)
    BOT.run_bot()


if __name__ == "__main__":
    main()
