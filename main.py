import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from time import time
from psutil import process_iter
from datetime import datetime
import os
import files.emulation
import _class.constants

#   Проверка на открытие исполняемго браузера
def is_open():   
    for proc in process_iter():
        name = proc.name()  
        #print(name)      
        if name == "firefox.exe":
            return True

#   Запись о ходе работы бота - информация о пользователях
#   -message: Текст для записи в файл
#   -path: Путь к файлу
def logs_write_to_file_about_user(message, path= _class.constants.PATH_TO_USER + _class.constants.PATH_NAME_USER):
    f = open(path, 'r+')
    f.write(message)
    f.close()

#   Очистка файла от информации
#   -path: Путь до файла
def file_cleaning(path =  _class.constants.PATH_TO_USER):   
    try:
        with open(path, 'r+') as f:
            f.truncate()
    except IOError:
        print('Failure')

#   Клавиатура пользователя
kb_start = [
    [
        types.KeyboardButton(text="Создать email")
    ],
    [
        types.KeyboardButton(text="Вывод педыдущий сесии")
    ],
    [
        types.KeyboardButton(text="Очистить педыдущие сесии"),
        types.KeyboardButton(text="Проверка текущих аккаунтов")
    ]
]

#   Клавиатура администратора
kb_admin = [
    [
        types.KeyboardButton(text="Создать email")
    ],
    [
        types.KeyboardButton(text="Вывод педыдущий сесии")
    ],
    [
        types.KeyboardButton(text="Очистить педыдущие сесии"),
        types.KeyboardButton(text="Проверка текущих аккаунтов")
    ],
    [
        types.KeyboardButton(text="Просмотреть историю всех учётных записей"),
        types.KeyboardButton(text="Просмотреть логи пользователей")
    ],
    [
        types.KeyboardButton(text="Удалить историю всех учётных записей"),
        types.KeyboardButton(text="Удалить логи пользователей")
    ]
]

#   Класс для хранения потока
class Form(StatesGroup):
    count = State() 

#   Присваивание переменной значения aiogram.Bot
bot = Bot(token= _class.constants.TOKEN)
#   Узел хранилища данных
storage = MemoryStorage()
#   Иницилизация бота
dp = Dispatcher(bot, storage=storage)

#   Ответ на команду /stop
@dp.message_handler(state='*', commands=['stop'])
@dp.message_handler(Text(equals='стоп', ignore_case=True), state='*')
async def cmd_stop(message: types.Message,  state: FSMContext):
    hide_markup = reply_markup=types.ReplyKeyboardRemove()
    await state.finish()
    await bot.send_message(message.from_user.id ,'Остановка, ' + message.from_user.full_name, reply_markup=hide_markup)

#   Ответ на команду /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):   
    if(message.from_id == _class.constants.AD_ID):
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb_admin)
        await bot.send_sticker(message.from_user.id,  _class.constants.TEMPLATE_STICKER_ID, reply_markup=keyboard)   
        text_combo = str(message.from_user.full_name) + ": " + str(datetime.now()) + "\n" + str(message) + "\n"
        print(str(text_combo))
        logs_write_to_file_about_user(message = str(text_combo))
        return
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_start)
    await bot.send_sticker(message.from_user.id,  _class.constants.TEMPLATE_STICKER_ID, reply_markup=keyboard)   
    text_combo = str(message.from_user.full_name) + ": " + str(datetime.now()) + "\n" + str(message) + "\n"
    print(str(text_combo))
    logs_write_to_file_about_user(message = str(text_combo))

#   Ответ на текстовое сообщение
@dp.message_handler(content_types='text', state=None)
async def text_handler(message: types.Message):
    if message.text == "Создать email":     
        if(is_open() == True):
            await bot.send_message(message.from_user.id, 'В данный момент я занят, попробуйте позже')   
            return
        hide_markup = reply_markup=types.ReplyKeyboardRemove()
        await bot.send_sticker(message.from_user.id,  _class.constants.TEMPLATE_STICKER_ID)              
        await bot.send_message(message.from_user.id, 'Введите количество аккаунтов',  reply_markup=hide_markup)
        await Form.count.set()         
         
    elif message.text == "Вывод педыдущий сесии":      
        try:                
            if(os.stat(_class.constants.PATH_USER + str(message.from_user.id) + _class.constants.EXTENSION).st_size == 0):
                await bot.send_message(message.from_id, "Файл с предыдущими сесиями пуст") 
                return
            document = open( _class.constants.PATH_USER + str(message.from_user.id) + _class.constants.EXTENSION, 'rb')     
            await bot.send_message(message.from_id, "Ваши учётные записи:")     
            await message.reply_document(document)
            document.close()
        except IOError:
            await bot.send_message(message.from_user.id, "Ошибка, файл не cуществует.")
            print('Failure')

    elif message.text == "Очистить педыдущие сесии":
        try:
            files.emulation.trunclate_file(path= _class.constants.PATH_USER + '/' + str(message.from_user.id))
            await bot.send_message(message.from_user.id, "Файл пуст.")
        except IOError:
            await bot.send_message(message.from_user.id, "Ошибка, файл не существует или повреждён.")
            print('Failure')

    elif message.text == "Проверка текущих аккаунтов": 
        try:
            try:
                mail = []
                password = []
                trg = 2
                for line in files.emulation.read_file(user_id=message.from_user.id):
                    if(trg == 2):
                        mail.append(line)
                        trg = 1                  
                        continue                
                    password.append(line)
                    trg+= 1
            except Exception as e:
                await bot.send_message(message.from_user.id, "Файл с предыдущими сесиями пуст или не существует")        
                print(e)
            try:
                if(is_open() == True):
                    await bot.send_message(message.from_user.id, 'В данный момент я занят, попробуйте позже')   
                    return
                for i in range(len(mail)):           
                    files.emulation.verefication(login=mail[i], password=password[i], trg=False)
            except Exception as e:
                await bot.send_message(message.from_user.id, "Файл с предыдущими сесиями пуст")            
                print(e)
        except Exception as e:
            print(e)
            await bot.send_message(message.from_id, "Страница изменилась, нужно переделывать.")

#   Поток Form
@dp.message_handler(state=Form.count)
async def count_handler(message: types.Message, state:FSMContext):
    try:
        if(0 < int(message.text) < 20):
            count = int(message.text)
            await bot.send_message(message.from_user.id, "Регистрация началась, подождите...")     
            for i in range(count):
                files.emulation.main(self_message=message.from_user.id, trg=False)     
        else:
            await bot.send_message(message.from_user.id, "Ошибка, поробуйте другое число, или чтобы вернуться к началу введите: /stop")
            return

        document = open( _class.constants.PATH_USER + str(message.from_user.id) + _class.constants.EXTENSION, 'rb')       
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb_start)
        await bot.send_message(message.from_id, "Ваши учётные записи:", reply_markup=keyboard)     
        await message.reply_document(document)
        document.close()
    
        await state.finish()
        return
    except:
        await bot.send_message(message.from_user.id, "Ошибка, введите валидное значение, или чтобы вернуться к началу введуте /stop")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)