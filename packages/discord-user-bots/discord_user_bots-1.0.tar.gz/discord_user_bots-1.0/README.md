# discord_user_bot

Discord library that will allow you to send messages or make events on these messages

# Installation:
```pip
pip install discord_user_bot
```

# Usage example

```python
from ds import Bot, Interaction

bots = Bot("user-token")

@bots.event(user_id=1234567890, event="message_new")
async def hello_world(inter: Interaction):
    print(inter.message.content)

bots.run()
```