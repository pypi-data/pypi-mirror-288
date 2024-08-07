from FletBot.felt_bot import *
from FletBot import Handler
from FletBot import Markups
from FletBot import Keyboards

class CallbackQuery:
    def __init__(self, query) -> None:
        self.id : int = query.id
        self.callback_id : int = query.id
        self.callback_data : str = query.data

        self._message = query.message
        self.message_id = self._message.id
        self.text : str = self._message.text
        self.date : int = self._message.date
        self.chat_id : int = self._message.chat.id
        
        self._user = query.from_user
        self.user_id = self._user.id
        self.is_bot = self._user.is_bot
        self.first_name = self._user.first_name
        self.last_name = self._user.last_name
        self.username = self._user.username
        self.language_code = self._user.language_code
        self.is_premium = self._user.is_premium

class MessageQuery:
    def __init__(self, message) -> None:

        self._message = message
        self.id = message.id
        self.chat = message.chat

        self.message_id : int = self._message.id
        self.text : str = self._message.text
        self.date : int = self._message.date
        self.chat_id : int = self._message.chat.id
        self.from_user = self._message.from_user
        
        self._user = self._message.from_user
        self.user_id = self._user.id
        self.user_is_bot = self._user.is_bot
        self.user_first_name = self._user.first_name
        self.user_last_name = self._user.last_name
        self.username = self._user.username
        self.user_language_code = self._user.language_code
        self.user_is_premium = self._user.is_premium 

        self.contact = message.contact
        self.phone_number = None
        if (self.contact):
            self.phone_number = self.contact.phone_number

        self.location = message.location
        if (self.location):
            print(self.location)

    def __str__(self) -> str:
        return str(self.__dict__)

def msg(func):
    async def message_handler(message, bot):
        if type(message) == MessageQuery:
            msgQ=message
        else
            msgQ = MessageQuery(message)
        await func(msgQ, bot)
    return message_handler

def call(func):
    async def callback(query, bot):
        if type(query) == CallbackQuery:
            callQ = query
        else:
            callQ = CallbackQuery(query)
        await func(callQ, bot)
    return callback