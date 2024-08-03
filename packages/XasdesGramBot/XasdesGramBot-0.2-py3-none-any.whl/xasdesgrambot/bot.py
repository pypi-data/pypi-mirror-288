import aiohttp
import asyncio
import json
import logging

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}/"
        self.commands = {}
        self.running = False

        # Настройка логирования
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def add_command(self, command, callback):
        self.commands[command] = callback

    async def start_polling(self):
        self.running = True
        self.logger.info("Bot started polling")
        await self._polling()

    def stop_polling(self):
        self.running = False
        self.logger.info("Bot stopped polling")

    async def _polling(self):
        offset = 0
        async with aiohttp.ClientSession() as session:
            while self.running:
                updates = await self._get_updates(session, offset)
                for update in updates:
                    offset = update["update_id"] + 1
                    await self._handle_update(session, update)

    async def _get_updates(self, session, offset):
        url = f"{self.base_url}getUpdates?timeout=100&offset={offset}"
        async with session.get(url) as response:
            if response.status != 200:
                self.logger.error(f"Failed to get updates: {response.status}")
                return []
            result = await response.json()
            return result.get("result", [])

    async def _handle_update(self, session, update):
        message = update.get("message")
        if not message:
            return

        chat_id = message["chat"]["id"]
        text = message.get("text")

        if not text:
            return

        for command, callback in self.commands.items():
            if text.startswith(command):
                response_text = callback(text)
                await self._send_message(session, chat_id, response_text)

    async def _send_message(self, session, chat_id, text):
        url = f"{self.base_url}sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        headers = {
            "Content-Type": "application/json"
        }
        async with session.post(url, data=json.dumps(payload), headers=headers) as response:
            if response.status != 200:
                self.logger.error(f"Failed to send message: {response.status}")

# Пример использования
if __name__ == "__main__":
    import os

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = TelegramBot(token)

    def start_command(text):
        return "Welcome to the bot!"

    bot.add_command("/start", start_command)

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start_polling())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        bot.stop_polling()
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        loop.close()
