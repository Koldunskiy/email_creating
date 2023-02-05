import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
import time
import os
import datetime
import files.emulation
import _class.constants


def is_open():
    import psutil
    for proc in psutil.process_iter():
        name = proc.name()  
        print(name)      
        if name == "firefox.exe":
            return True

def logs_write_to_file_about_user(message, path= _class.constants.path_users + _class.constants.path_name_users):
    f = open(path, 'a')
    f.write(message)
    f.close()

def file_cleaning(path =  _class.constants.path_logs + _class.constants.path_name_logs):
    try:
        with open(path, 'r+') as f:
            f.truncate()
    except IOError:
        print('Failure')

kb_start = [
    [
        types.KeyboardButton(text="Создать email")
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
    await bot.send_message(message.from_user.id ,'Остановка, ' + message.from_user.full_name, reply_markup=hide_markup)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_start)
    await bot.send_sticker(message.from_user.id,  _class.constants.template_sticker_id, reply_markup=keyboard)   
    text_combo = str(message.from_user.full_name) + ": " + str(datetime.datetime.now()) + "\n" + str(message) + "\n"
    print(str(text_combo))
    logs_write_to_file_about_user(message = str(text_combo))


@dp.message_handler(content_types='text', state=None)
async def text_handler(message: types.Message):
    if message.text == "Создать email":     
        if(is_open() == True):
            await bot.send_message(message.from_user.id, 'В данный момент я занят, попробуйте позже')   
            return
        hide_markup = reply_markup=types.ReplyKeyboardRemove()
        await bot.send_sticker(message.from_user.id,  _class.constants.template_sticker_id)              
        await bot.send_message(message.from_user.id, 'Введите количество аккаунтов', reply_markup=hide_markup)
        await Form.count.set()         
         
    elif message.text == "Вывод преведущий сесии":        
        all_files_in_directory = os.listdir( _class.constants.path_logs)    

        for filess in all_files_in_directory:           
            document = open( _class.constants.path_logs + '/' + filess, 'rb')            
            await message.reply_document(document)
            document.close()
    
    elif message.text == "Проверка текущих аккаунтов": 
        trg = 2
        for line in files.emulation.read_file():
            if(trg == 2):
                first = line
                trg = 0
                print(line)
            first = line
            trg+= 1
          
           
    elif message.text=='Регестрация началась, подождите...':
        time.sleep(4)
        bot.delete_message(message.chat.id, message.message_id)

@dp.message_handler(state=Form.count)
async def count_handler(message: types.Message, state:FSMContext):
    try:
        if(0 < int(message.text) < 20):
            count = int(message.text)
            await bot.send_message(message.from_user.id, "Регестрация началась, подождите...")
            file_cleaning()
            for i in range(count):
                files.emulation.main()       
        else:
            await bot.send_message(message.from_user.id, "Ошибка, чтобы вернуться к началу введуте /stop")
            return

        all_files_in_directory = os.listdir(_class.constants.path_logs)    

        for filess in all_files_in_directory:           
            if(filess == 'all_logs.txt'):
                continue
            document = open( _class.constants.path_logs + '/' + filess, 'rb')            
            await message.reply_document(document)
            document.close()
        
        await state.finish()
    except:
        await bot.send_message(message.from_user.id, "Ошибка, введите валидное значение, или чтобы вернуться к началу введуте /stop")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)