import aiohttp

from pydantic import BaseModel
from typing import List, Optional

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


class Author(BaseModel):
    id: str
    username: str
    avatar: Optional[str]
    discriminator: str
    public_flags: int
    flags: int
    banner: Optional[str]
    accent_color: Optional[int]
    global_name: str
    banner_color: Optional[str]

class Message(BaseModel):
    type: int
    content: str
    mentions: List
    mention_roles: List
    attachments: List
    embeds: List
    timestamp: str
    edited_timestamp: Optional[str]
    flags: int
    components: List
    id: str
    channel_id: str
    author: Author
    pinned: bool
    mention_everyone: bool
    tts: bool

    token: Optional[str] = None
    user_info: dict

    async def edit(self, new_content: str) -> 'Message':

        global headers

        if self.author.id != self.user_info['id']:
            return None

        url: str = f'https://discord.com/api/v9/channels/{self.channel_id}/messages/{self.id}'

        headers['Authorization'] = self.token
        headers['Content-Type'] ='application/json'

        payload: dict = {
            'content': new_content,
            'flags': self.flags,
            'tts': self.tts
        }

        async with aiohttp.ClientSession() as session:

            async with session.patch(url, json=payload, headers=headers) as response:
                response_json: dict = await response.json()

        return Message(**response_json, token=self.token)

    async def delete(self) -> None:
        global headers

        if self.author.id != self.user_info['id']:
            return None
        
        url: str = f'https://discord.com/api/v9/channels/{self.channel_id}/messages/{self.id}'

        headers['Authorization'] = self.token
        headers['Content-Type'] ='application/json'

        payload: dict = {
            'flags': self.flags,
            'tts': self.tts
        }

        async with aiohttp.ClientSession() as session:
            
            async with session.delete(url, json=payload, headers=headers) as response:
                return None
