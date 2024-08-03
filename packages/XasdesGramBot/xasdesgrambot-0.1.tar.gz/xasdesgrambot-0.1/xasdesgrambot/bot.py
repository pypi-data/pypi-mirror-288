import requests
import json
import threading

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}/"
        self.commands = {}
        self.running = False

    def add_command(self, command, callback):
        self.commands[command] = callback

    def start_polling(self):
        self.running = True
        threading.Thread(target=self._polling).start()

    def stop_polling(self):
        self.running = False

    def _polling(self):
        offset = 0
        while self.running:
            updates = self._get_updates(offset)
            for update in updates:
                offset = update["update_id"] + 1
                self._handle_update(update)

    def _get_updates(self, offset):
        url = f"{self.base_url}getUpdates?timeout=100&offset={offset}"
        response = requests.get(url)
        return response.json().get("result", [])

    def _handle_update(self, update):
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
                self._send_message(chat_id, response_text)

    def _send_message(self, chat_id, text):
        url = f"{self.base_url}sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        headers = {
            "Content-Type": "application/json"
        }
        requests.post(url, data=json.dumps(payload), headers=headers)
