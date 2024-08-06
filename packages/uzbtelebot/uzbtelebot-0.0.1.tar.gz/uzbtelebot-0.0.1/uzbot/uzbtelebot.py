import telebot

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

    def message(self, user_id, message):
        self.bot.send_message(user_id, message)

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



    def run(self):
        self.bot.polling()

# Foydalanish uchun misol
if __name__ == "__main__":
    bot = UzBot.from_token('your_token_here')

    @bot.command('start')
    def start_command(message):
        bot.message(message.from_user.id, 'Salom!')

    bot.run()
