import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

class UzBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.commands = {}

    @classmethod
    def token(cls, token):
        return cls(token)

    def command(self, command):
        def decorator(func):
            self.commands[command] = func
            self.bot.message_handler(commands=[command])(func)
            return func
        return decorator

    def user_text(self, message):
        return message.text

    def user_id(self, message):
        return message.from_user.id

    def user_name(self, message):
        return message.from_user.first_name

    def username(self, message):
        return message.from_user.username

    def message(self, user_id, text):
        self.bot.send_message(user_id, text)

    def reply(self, message, reply_message):
        self.bot.reply_to(message, reply_message)

    def video(self, user_id, video):
        self.bot.send_video(user_id, video)

    def audio(self, user_id, audio):
        self.bot.send_audio(user_id, audio)

    def voice(self, user_id, voice):
        self.bot.send_voice(user_id, voice)

    def animation(self, user_id, animation):
        self.bot.send_animation(user_id, animation)

    def game(self, user_id, game):
        self.bot.send_game(user_id, game)

    def photo(self, user_id, photo):
        self.bot.send_photo(user_id, photo)

    def send_inline_buttons(self, user_id, text, buttons):
        markup = InlineKeyboardMarkup()
        for button in buttons:
            markup.add(InlineKeyboardButton(button['text'], callback_data=button['callback_data']))
        self.bot.send_message(user_id, text, reply_markup=markup)

    def send_keyboard_buttons(self, user_id, text, buttons):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for button in buttons:
            markup.add(KeyboardButton(button))
        self.bot.send_message(user_id, text, reply_markup=markup)

    def update_inline_buttons(self, chat_id, message_id, buttons):
        markup = InlineKeyboardMarkup()
        for button in buttons:
            markup.add(InlineKeyboardButton(button['text'], callback_data=button['callback_data']))
        self.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=markup)

    def update_keyboard_buttons(self, user_id, buttons):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for button in buttons:
            markup.add(KeyboardButton(button))
        self.bot.send_message(user_id, ' ', reply_markup=markup)  # Sending a message with space to update keyboard

    def add_button(self, buttons, new_button):
        buttons.append(new_button)

    def run(self):
        self.bot.polling()

# Foydalanish uchun misol
if __name__ == "__main__":
    bot = UzBot.token('your_token_here')

    bot.current_inline_buttons = [
        {'text': 'Option 1', 'callback_data': 'option1'},
        {'text': 'Option 2', 'callback_data': 'option2'},
        {'text': 'Option 3', 'callback_data': 'option3'}
    ]

    bot.current_keyboard_buttons = [
        'Option 1',
        'Option 2',
        'Option 3'
    ]

    @bot.command('start')
    def start_command(message):
        bot.send_inline_buttons(message.from_user.id, 'Salom! Qanday yordam bera olaman?', bot.current_inline_buttons)
        bot.send_keyboard_buttons(message.from_user.id, 'Iltimos, biror tugmani tanlang:', bot.current_keyboard_buttons)

    @bot.bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == 'option1':
            bot.add_button(bot.current_inline_buttons, {'text': 'New Option', 'callback_data': 'new_option'})
            bot.update_inline_buttons(call.message.chat.id, call.message.message_id, bot.current_inline_buttons)
            bot.add_button(bot.current_keyboard_buttons, 'New Option')
            bot.update_keyboard_buttons(call.from_user.id, bot.current_keyboard_buttons)
        elif call.data == 'option2':
            bot.add_button(bot.current_inline_buttons, {'text': 'Another Option', 'callback_data': 'another_option'})
            bot.update_inline_buttons(call.message.chat.id, call.message.message_id, bot.current_inline_buttons)
            bot.add_button(bot.current_keyboard_buttons, 'Another Option')
            bot.update_keyboard_buttons(call.from_user.id, bot.current_keyboard_buttons)
        elif call.data == 'option3':
            bot.add_button(bot.current_inline_buttons, {'text': 'Additional Option', 'callback_data': 'additional_option'})
            bot.update_inline_buttons(call.message.chat.id, call.message.message_id, bot.current_inline_buttons)
            bot.add_button(bot.current_keyboard_buttons, 'Additional Option')
            bot.update_keyboard_buttons(call.from_user.id, bot.current_keyboard_buttons)

    bot.run()
