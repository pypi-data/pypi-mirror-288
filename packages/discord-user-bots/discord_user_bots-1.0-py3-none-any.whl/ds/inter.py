import aiohttp
import asyncio
import re

from cachetools import TTLCache
from .type.message import Message

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru,en-US;q=0.9',
    'Priority': 'u=1, i',
    'Referer': 'https://discord.com/channels/@me',
    'Sec-Ch-Ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9153 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36',
    'X-Debug-Options': 'bugReporterEnabled',
    'X-Discord-Locale': 'ru',
    'X-Discord-Timezone': 'Europe/Moscow',
}

last_message = None
last_message_id_sendes = 0

class Interaction:
    def __init__(self, token: str, user_id: int, user_info: dict) -> Message:
        global last_message
        self.token: str = token
        self.user_id: int = user_id
        self.user_info: dict = user_info
        self.cache: TTLCache = TTLCache(maxsize=1, ttl=600)
        if last_message:
            self.message = Message(token=self.token, user_info=self.user_info, **last_message)
    
    async def send_message(self, content) -> Message:
        global last_message_id_sendes, headers
        url: str = f'https://discord.com/api/v9/channels/{self.user_id["info"]}/messages'
        headers['Authorization'] = self.token
        headers['Content-Type'] = 'application/json'
        payload: dict = {
            'content': content,
            'flags': 0,
            'mobile_network_type': 'unknown',
            'tts': False
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                response_json: dict = await response.json()
                last_message_id_sendes = response_json['id']
        return Message(token=self.token, user_info=self.user_info, **response_json)

    async def get_all_message(self, user_id: dict, functions: callable, Tr: bool = False) -> None:

        global last_message, last_message_id_sendes, headers

        headers['Authorization'] = self.token
        headers['Content-Type'] = 'application/json'

        url = f"https://discord.com/api/v9/channels/{user_id['info']}/messages?limit=50"
        async with aiohttp.ClientSession() as session:

            last_message_id = self.cache['last_message_id'] if self.cache else 0
            params = {'limit': 50}
            if last_message_id:

                params['after'] = last_message_id
            async with session.get(url, headers=headers, params=params) as response:

                if response.status == 200:

                    messages = await response.json()
                    if messages:

                        messages.reverse()

                        for message in messages:

                            self.cache['last_message_id'] = message['id']
                            content_lower = message['content']
                            
                            if "commands" in user_id:
                                com = user_id['commands']
                                commands = user_id['command']

                                if not Tr and int(last_message_id_sendes) < int(message['id']):

                                    match = com.match(content_lower)
                                    if match:

                                        kwargs = {k: self._convert_arg(v, match.group(k)) for k, v in com.groupindex.items()}
                                        self.message = Message(token=self.token, user_info=self.user_info, **message)

                                        await functions(inter=self, **kwargs)
                                        break

                                    else:

                                        print(f"No match found for content: {content_lower}")

                            if not Tr and "event" in user_id and int(last_message_id_sendes) < int(message['id']):

                                if user_id["event"] == "message_new":

                                    self.message = Message(token=self.token, user_info=self.user_info, **message)
                                    await functions(inter=self)
                                    break

    async def get_messages(self, functions: callable) -> None:

        await self.get_all_message(self.user_id, functions, True)
        await asyncio.sleep(2)

        while True:
            await self.get_all_message(self.user_id, functions)

    def _convert_arg(self, arg_type: str, value: str):

        if arg_type == 'int':
            return int(value)
        
        return value
