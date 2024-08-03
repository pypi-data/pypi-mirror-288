import unittest
from xasdesgrambot import TelegramBot

class TestTelegramBot(unittest.TestCase):
    def setUp(self):
        self.bot = TelegramBot("YOUR_TELEGRAM_BOT_TOKEN")

    def test_add_command(self):
        def hello_command(text):
            return "Hello, world!"

        self.bot.add_command("/hello", hello_command)
        self.assertIn("/hello", self.bot.commands)
        self.assertEqual(self.bot.commands["/hello"](""), "Hello, world!")

if __name__ == '__main__':
    unittest.main()
