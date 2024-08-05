import aiohttp
import asyncio
from typing import Callable, Dict, Any

class TelegramBotFastMe:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}/"
        self.handlers: Dict[str, Callable] = {}
        self.session = None

    async def start(self):
        self.session = aiohttp.ClientSession()
        offset = 0
        while True:
            try:
                updates = await self._get_updates(offset)
                for update in updates:
                    offset = update['update_id'] + 1
                    await self._process_update(update)
            except Exception as e:
                print(f"Error: {e}")

    async def _get_updates(self, offset: int):
        async with self.session.get(f"{self.base_url}getUpdates", params={'offset': offset, 'timeout': 30}) as response:
            return (await response.json())['result']

    async def _process_update(self, update: Dict[str, Any]):
        if 'message' in update and 'text' in update['message']:
            text = update['message']['text']
            chat_id = update['message']['chat']['id']
            if text.startswith('/'):
                command = text.split()[0][1:]
                if command in self.handlers:
                    await self.handlers[command](self, chat_id, text)

    async def send_message(self, chat_id: int, text: str):
        await self.session.post(f"{self.base_url}sendMessage", json={'chat_id': chat_id, 'text': text})

    def command(self, name: str):
        def decorator(func):
            self.handlers[name] = func
            return func
        return decorator

    async def stop(self):
        if self.session:
            await self.session.close()