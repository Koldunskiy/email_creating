import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
import os
import datetime
import files.emulation
import _class.constants

def file_cleaning(path =  _class.constants.path_logs + "logs.txt"):
    try:
        with open(path, 'r+') as f:
            f.truncate()
    except IOError:
        print('Failure')

kb_start = [
    [
        types.KeyboardButton(text="Email")
    ],
    [
        types.KeyboardButton(text="Вывод преведущий сесии",)
    ]
]

class Form(StatesGroup):
    count = State() 
  
bot = Bot(token= _class.constants.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(state='*', commands=['stop'])
@dp.message_handler(Text(equals='стоп', ignore_case=True), state='*')
async def cmd_stop(message: types.Message,  state: FSMContext):
    hide_markup = reply_markup=types.ReplyKeyboardRemove()
    await state.finish()
    await bot.send_message(message.from_user.id ,'Стоп', reply_markup=hide_markup)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_start)
    await bot.send_sticker(message.from_user.id,  _class.constants.template_sticker_id, reply_markup=keyboard)


@dp.message_handler(content_types='text', state=None)
async def text_handler(message: types.Message):
    if message.text == "Email":        
        hide_markup = reply_markup=types.ReplyKeyboardRemove()
        await bot.send_sticker(message.from_user.id,  _class.constants.template_sticker_id)              
        await bot.send_message(message.from_user.id, 'Введите количество аккаунтов', reply_markup=hide_markup)
        await Form.count.set()         
         
    elif message.text == "Вывод преведущий сесии":        
        all_files_in_directory = os.listdir( _class.constants.path_logs)    

        for files in all_files_in_directory:           
            document = open( _class.constants.path_logs + '/' + files, 'rb')            
            await message.reply_document(document)
            document.close()
    
@dp.message_handler(state=Form.count)
async def count_handler(message: types.Message, state:FSMContext):
    
    if(0 < int(message.text) < 20):
        count = int(message.text)
        await bot.send_message(message.from_user.id, "Регестрация началась")
        file_cleaning()
        for i in range(count):
            files.emulation.main()       
    else:
        await bot.send_message(message.from_user.id, "Error")
        return

    all_files_in_directory = os.listdir(_class.constants.path_logs)    

    for filess in all_files_in_directory:           
        document = open( _class.constants.path_logs + '/' + filess, 'rb')            
        await message.reply_document(document)
        document.close()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)