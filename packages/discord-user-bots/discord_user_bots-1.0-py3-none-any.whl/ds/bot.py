import asyncio
import requests

import re
import os

from .inter import Interaction
from .error.token import DiscordValidToken

from .labeler import BotLabeler

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru,en-US;q=0.9',
    'Priority': 'u=1, i',
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

class Bot:
    def __init__(self, token: str, prefix: str = "", note=True):
        self.token = token

        self.prefix = prefix
        self._message_funcs = []
        self._slash_message_funcs = []
        self.note = note
        self.token_verif: int | dict = self.token_verification()

    def message(self, channel_id: int|str|list = None, guild_id: int|str = None, commands: str | list = None):
        def decorator(func):
            async def wrapper(inter, *args, **kwargs):
                result = await func(inter, *args, **kwargs)
                return result

            if isinstance(commands, list):
                command_patterns = [self._build_command_pattern(command) for command in commands]
                command = [command.split('<')[0].strip() for command in commands]
            else:
                command_patterns = [self._build_command_pattern(commands)]
                command = [commands.split('<')[0].strip()]

            if guild_id:
                guilds = self.get_guild(guild_id)

                for channel in guilds:

                    if isinstance(commands, list):

                        for command1 in command:

                            self._message_funcs.append((
                                {"info": channel['id'], "commands": command_pattern, 
                                "user_info": self.token_verif, "command": command1
                            }, wrapper))
                        
                    else:
                            self._message_funcs.append((
                                {"info":  channel['id'], "commands": command_pattern, 
                                "user_info": self.token_verif, "command": command[0]
                            }, wrapper))

            elif channel_id:
                for command_pattern in command_patterns:

                    if isinstance(commands, list):

                        for command1 in command:

                            self._message_funcs.append((
                                {"info": channel_id, "commands": command_pattern, 
                                "user_info": self.token_verif, "command": command1
                            }, wrapper))
                        
                    else:
                            self._message_funcs.append((
                                {"info": channel_id, "commands": command_pattern, 
                                "user_info": self.token_verif, "command": command[0]
                            }, wrapper))


            return wrapper
        return decorator

    def _build_command_pattern(self, command: str):
        command = command.lower()
        arg_pattern = r"<(\w+):(\w+)>"
        command_regex = re.sub(arg_pattern, r"(?P<\1>\2)", command)
        
        type_map = {"int": r"\d+", "str": r".+"}
        for type_name, pattern in type_map.items():
            command_regex = command_regex.replace(type_name, pattern)
        
        return re.compile(f"^{command_regex}$", re.IGNORECASE)


    def register_bot(self, bot: BotLabeler):

        for conditions, func in bot._message_funcs:
            print(conditions)
            command = conditions['commands'].split('<')[0].strip()

            conditions = conditions
            conditions["command"] = command[0]
            conditions["user_info"] = self.token_verif

            self._message_funcs.append((conditions, func))
            
        
        for conditions, func in bot._event_funcs:

            conditions = conditions
            conditions["user_info"] = self.token_verif

            self._message_funcs.append((conditions, func))

    def event(self, user_id, event):

        def decorator(func):

            async def wrapper(inter, *args, **kwargs):

                result = await func(inter, *args, **kwargs)
                return result
            
            self._message_funcs.append(({"info": user_id, "event": event, "user_info": self.token_verif}, wrapper))
            return wrapper
        
        return decorator

    def __call__(self, func):

        async def wrapper(*args, **kwargs):

            result = await func(*args, **kwargs)
            return result
        return wrapper

    def token_verification(self, token:str = None):

        global headers
        if not token:
            token = self.token

        url: str = f'https://discord.com/api/v9/users/@me'

        headers['Authorization'] = self.token
        headers['Content-Type'] ='application/json'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:

            return response.json()
        else:
            return response.status_code

    def get_guild(self, id):

        global headers

        url = f"https://discord.com/api/v10/guilds/{id}/channels"

        headers['Authorization'] = self.token
        headers['Content-Type'] ='application/json'

        response = requests.get(url, headers=headers)
        return response.json()
    
    async def delete_friend_request(self, id):

        global headers

        url = f"https://discord.com/api/v9/users/@me/relationships/{id}"

        headers['Authorization'] = self.token

        response = requests.delete(url, headers=headers)
        return response.text

    def run(self):

        async def main():

            if self.note:
                print(
                    "https://support.discord.com/hc/en-us/articles/115002192352-Automated-User-Accounts-Self-Bots\n"
                    "We are not forcing you to use this library, but know that the use of user bots is punishable by bans in discord"
                )

            os.system("pyclean .")
            tasks = []
            for user_id, func in self._message_funcs:

                task = asyncio.create_task(Interaction(self.token, user_id, self.token_verif).get_messages(func))
                tasks.append(task)
                
            await asyncio.gather(*tasks)

        if type(self.token_verif) == dict:
            asyncio.run(main())

        else:
            raise DiscordValidToken(f"Invalid Token | Status code: {self.token_verif}")
