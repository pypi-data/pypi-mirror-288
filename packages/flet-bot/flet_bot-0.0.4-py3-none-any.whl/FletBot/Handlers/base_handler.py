from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, List, Optional, Union
from telebot.asyncio_handler_backends import State

class Handler(ABC):
    def __init__(self, 
                 callback: Callable[[Any], Awaitable], 
                 content_types: Optional[List[str]]=None, 
                 commands: Optional[List[str]]=None,
                 regexp: Optional[str]=None,
                 func: Optional[Callable]=None,
                 chat_types: Optional[List[str]]=None,
                 pass_bot: Optional[bool]=False,
                 state: Union[State, str, int] | None = None,
                 **kwargs):
        
        self.callback = callback
        self.content_types = content_types
        self.commands = commands
        self.regexp = regexp
        self.func = func
        self.chat_types = chat_types
        self.pass_bot = pass_bot
        self.state = state
        self.kwargs = kwargs
    
    def set_state(self, state: Union[State, str, int] | None = None):
        self.state = state
        return self
    
    def register(self):
        return {"callback":self.callback,
                "chat_types":self.chat_types,
                "content_types":self.content_types,
                "commands":self.commands,
                "regexp":self.regexp,
                "func":self.func,
                "state": self.state,
                "pass_bot":self.pass_bot,
                **self.kwargs}