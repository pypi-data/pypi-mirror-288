import re
from typing import Callable, List, Dict, Tuple

class BotLabeler:
    def __init__(self):
        self._message_funcs: List[Tuple[Dict, Callable]] = []
        self._event_funcs: List[Tuple[Dict, Callable]] = []

    def message(self, channel_id: int | str = None, commands: str | List[str] = None):
        def decorator(func):
            async def wrapper(inter, *args, **kwargs):
                result = await func(inter, *args, **kwargs)
                return result

            command_patterns = [self._build_command_pattern(cmd) for cmd in (commands if isinstance(commands, list) else [commands])]
            for pattern in command_patterns:
                self._message_funcs.append(({"info": channel_id, "commands": pattern}, wrapper))

            return wrapper
        return decorator

    def event(self, user_id: int | str, event: str):
        def decorator(func):
            async def wrapper(inter, *args, **kwargs):
                result = await func(inter, *args, **kwargs)
                return result

            self._event_funcs.append(({"info": user_id, "event": event}, wrapper))
            return wrapper
        return decorator

    def _build_command_pattern(self, command: str):
        command = command.lower()
        arg_pattern = r"<(\w+):(\w+)>"
        command_regex = re.sub(arg_pattern, r"(?P<\1>\2)", command)
        
        type_map = {"int": r"\d+", "str": r".+"}
        for type_name, pattern in type_map.items():
            command_regex = command_regex.replace(type_name, pattern)
        
        return re.compile(f"^{command_regex}$")

    async def process_message(self, inter, message_content):
        for conditions, func in self._message_funcs:
            pattern = conditions['commands']
            match = pattern.match(message_content.lower())
            if match:
                kwargs = {k: self._convert_arg(v, match.group(k)) for k, v in conditions['commands'].groupindex.items()}
                await func(inter, **kwargs)
                break

    async def process_event(self, inter, event_type):
        for conditions, func in self._event_funcs:
            if conditions['event'] == event_type:
                await func(inter)
                break

    def _convert_arg(self, arg_type: str, value: str):
        if arg_type == 'int':
            return int(value)
        return value