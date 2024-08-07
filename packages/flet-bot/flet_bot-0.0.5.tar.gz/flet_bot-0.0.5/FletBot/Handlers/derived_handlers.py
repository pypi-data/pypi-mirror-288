from telebot.asyncio_handler_backends import State
from FletBot.Handlers.base_handler import Handler
from typing import Any, Awaitable, Callable, List, Optional, Union

class MessageHandler(Handler):    
    def __init__(self, 
                 callback: Callable[[Any], Awaitable], 
                 content_types: Optional[List[str]]=None, 
                 commands: Optional[List[str]]=None,
                 regexp: Optional[str]=None,
                 func: Optional[Callable]=None,
                 chat_types: Optional[List[str]]=None,
                 pass_bot: Optional[bool]=False, 
                 **kwargs):

        super().__init__(callback, content_types,commands,
                 regexp, func, chat_types, pass_bot, **kwargs)
        
    def set_state(self, state: Union[State | str | int] | None = None):
        return super().set_state(state)
        
    def register(self):
        return super().register()
    
class DocumentHandler(Handler):    
    def __init__(self, 
                 callback: Callable[[Any], Awaitable], 
                 content_types: Optional[List[str]]=None, 
                 commands: Optional[List[str]]=None,
                 regexp: Optional[str]=None,
                 func: Optional[Callable]=None,
                 chat_types: Optional[List[str]]=None,
                 pass_bot: Optional[bool]=False, 
                 **kwargs):
        
        super().__init__(callback, content_types,commands,
                 regexp, func, chat_types, pass_bot, **kwargs)
        
    def register(self):
        return super().register()

class PhotoHandler(Handler):    
    def __init__(self, 
                 callback: Callable[[Any], Awaitable], 
                 content_types: Optional[List[str]]=None, 
                 commands: Optional[List[str]]=None,
                 regexp: Optional[str]=None,
                 func: Optional[Callable]=None,
                 chat_types: Optional[List[str]]=None,
                 pass_bot: Optional[bool]=False, 
                 **kwargs):
        
        super().__init__(callback, content_types,commands,
                 regexp, func, chat_types, pass_bot, **kwargs)
        
    def register(self):
        return super().register()
    
class CallbackHandler(Handler):    
    def __init__(self, 
                 callback: Callable[[Any], Awaitable], 
                 content_types: Optional[List[str]]=None, 
                 commands: Optional[List[str]]=None,
                 regexp: Optional[str]=None,
                 func: Optional[Callable]=None,
                 chat_types: Optional[List[str]]=None,
                 pass_bot: Optional[bool]=False, 
                 **kwargs):
        
        super().__init__(callback, content_types,commands,
                 regexp, func, chat_types, pass_bot, **kwargs)
        
    def register(self):
        return super().register()
