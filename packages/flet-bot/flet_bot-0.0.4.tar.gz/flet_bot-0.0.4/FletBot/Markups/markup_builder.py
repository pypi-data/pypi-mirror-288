from telebot.types import InlineKeyboardButton, KeyboardButton
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from typing import List, Optional, Any

class MarkupBuilder:
    def __init__(self):
        self.__reply_markup : ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None
        self.__keyboard = []
        
        self.params = {}
    
    def set_resize_keyboard(self, flag = True):
        self.params['resize_keyboard'] = flag
        return self
    
    def set_one_time_keyboard(self, flag=True):
        self.params['one_time_keyboard'] = flag
        return self
    
    def set_selective(self, flag = True):
        self.params['selective'] = flag
        return self
    
    def set_row_width(self, width=3):
        self.params['row_width'] = width
        return self
    
    def set_input_field_placeholder(self, placeholder = "test"):
        self.params["input_field_placeholder"] = placeholder
        return self
    
    def set_is_persistent(self, flag=True):
        self.params["is_persistent"] = flag
        return self
    
    def reply(self):
        self.__reply_markup = ReplyKeyboardMarkup
        return self

    def inline(self):    
        self.__reply_markup = InlineKeyboardMarkup
        return self
    
    
    def add_row(self, row: InlineKeyboardButton | KeyboardButton | List[KeyboardButton|InlineKeyboardButton]):
        self.__reply_markup.row(row)
        return self
    
    def add(self, buttons: InlineKeyboardButton | KeyboardButton | List[KeyboardButton|InlineKeyboardButton]):
        self.__reply_markup.row(buttons)
        return self

    def build(self):
        if issubclass(self.__reply_markup, InlineKeyboardMarkup):
            self.__reply_markup = InlineKeyboardMarkup(**self.params)
            return self.__reply_markup
    
        self.__reply_markup = ReplyKeyboardMarkup(**self.params)
        return self.__reply_markup
        