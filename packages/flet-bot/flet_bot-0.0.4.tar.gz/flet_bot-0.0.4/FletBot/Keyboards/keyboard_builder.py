from telebot.types import WebAppInfo
from telebot.types import KeyboardButtonPollType, KeyboardButtonRequestUser, KeyboardButtonRequestChat, KeyboardButtonRequestUsers
from telebot.types import InlineKeyboardButton, KeyboardButton
from typing import List, Optional, Any

class ButtonBuilder:
    def __init__(self):
        self.__button_type: InlineKeyboardButton | KeyboardButton = KeyboardButton
        self.text: Any = "ChangeText"
        self.url: Any | None = None
        self.callback_data: Any | None = None
        self.web_app: Any | None = None
        self.switch_inline_query: Any | None = None
        self.switch_inline_query_current_chat: Any | None = None
        self.switch_inline_query_chosen_chat: Any | None = None
        self.callback_game: Any | None = None, 
        self.pay: Any | None = None
        self.login_url: Any | None = None
        self.kwargs: Any | None = None

        self.result_params = {}

        self.request_contact: bool | None = None
        self.request_location: bool | None = None
        self.request_poll: KeyboardButtonPollType | None = None        
        self.request_user: KeyboardButtonRequestUser | None = None
        self.request_chat: KeyboardButtonRequestChat | None = None
        self.request_users: KeyboardButtonRequestUsers | None = None

    def inline(self):
        self.__button_type = InlineKeyboardButton
        return self
    
    def set_text(self, text):
        self.text = text
        self.result_params['text'] = self.text
        return self

    def set_url(self, url):
        if not(issubclass(self.__button_type, InlineKeyboardButton)):
            raise RuntimeError("Property\"url\" only for inline button")
        self.url = url
        self.result_params['url'] = self.url
        return self
    
    def set_callback_data(self, callback_data):
        if not(issubclass(self.__button_type, InlineKeyboardButton)):
            raise RuntimeError("Property\"callback_data\" only for inline button")
        self.callback_data = callback_data
        self.result_params['callback_data'] = self.callback_data
        return self
    

    def set_web_app(self, web_app_url):
        self.web_app = WebAppInfo(url=web_app_url)
        self.result_params['web_app'] = self.web_app
        return self
    
    def set_switch_inline_query(self, switch_inline_query):
        self.switch_inline_query = switch_inline_query
        self.result_params['switch_inline_query'] = self.switch_inline_query
        return self
    
    def set_pay(self, pay):
        if not(issubclass(self.__button_type, InlineKeyboardButton)):
            raise RuntimeError("Property\"callback_data\" only for inline button")
        self.pay = pay 
        self.result_params['pay'] = self.pay
        return self
    
    def set_game_callback(self, game_callback):
        if not(issubclass(self.__button_type, InlineKeyboardButton)):
            raise RuntimeError("Property\"callback_data\" only for inline button")
        self.callback_game = game_callback
        self.result_params['callback_game'] = self.callback_game
        return self
    
    def set_login_url(self, login_url):
        if not(issubclass(self.__button_type, InlineKeyboardButton)):
            raise RuntimeError("Property\"callback_data\" only for inline button")
        self.login_url = login_url
        self.result_params['login_url'] = self.login_url
        return self
    
    def add_kwargs(self, **kwargs):
        self.kwargs = kwargs
        self.result_params['kwargs'] = self.kwargs
        return self
    
    def request_contact(self):
        if not(issubclass(self.__button_type, KeyboardButton)):
            raise RuntimeError("Property\"request_*\" only for keyboard button")
        self.request_contact = True
        self.result_params['request_contact'] = self.request_contact
        return self
    
    def set_request_location(self):
        if not(issubclass(self.__button_type, KeyboardButton)):
            raise RuntimeError("Property\"request_*\" only for keyboard button")
        self.request_location = True
        self.result_params['request_location'] = self.request_location
        return self
    
    def build(self):
        if issubclass(self.__button_type, InlineKeyboardButton):
            return self.__build_inline_button()
        return self.__build_keyboard_button()
    

    def __build_keyboard_button(self):
        return KeyboardButton(**self.result_params)
    
    def __build_inline_button(self):
        if self.kwargs is None:
            return InlineKeyboardButton(**self.result_params)
        else:
            return InlineKeyboardButton(**self.result_params)