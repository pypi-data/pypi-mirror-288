import aiohttp
import asyncio
import json
import logging
import re

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}/"
        self.running = False

        # Настройка логирования
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        # Инициализация диспетчера
        self.dispatcher = Dispatcher()

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
                    await self.dispatcher.process_update(session, update)
                await asyncio.sleep(1)  # Small sleep to avoid hitting the rate limits

    async def _get_updates(self, session, offset):
        url = f"{self.base_url}getUpdates?timeout=100&offset={offset}"
        async with session.get(url) as response:
            if response.status != 200:
                self.logger.error(f"Failed to get updates: {response.status}")
                return []
            result = await response.json()
            return result.get("result", [])

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

class Dispatcher:
    def __init__(self):
        self.handlers = {}

    def register_handler(self, command, callback):
        self.handlers[command] = callback

    async def process_update(self, session, update):
        message = update.get("message")
        if not message:
            return

        chat_id = message["chat"]["id"]
        text = message.get("text")

        if not text:
            return

        response_text = None
        for command, callback in self.handlers.items():
            if text.startswith(command):
                # Extract arguments if present
                args = re.split(r'\s+', text[len(command):].strip())
                if asyncio.iscoroutinefunction(callback):
                    response_text = await callback(*args)
                else:
                    response_text = callback(*args)
                break

        if response_text:
            await self._send_message(session, chat_id, response_text)
