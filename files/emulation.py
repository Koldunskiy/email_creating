from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import os.path
import files.constants_emulation

#   Очистка файла
def trunclate_file(path): 
    try:
        with open(path + files.constants_emulation.EXTENSION, 'r+') as f:
            f.truncate()
    except IOError:
        print('Failure')

#   Запись в файл
#   -message: Текст для записи
#   path: Путь к файлу
def logs_write_to_file(message, 
                        path= files.constants_emulation.PATH_ALL_LOGS):
    if(os.path.exists(path + files.constants_emulation.EXTENSION) == False):
        f = open(file=path + files.constants_emulation.EXTENSION, mode='w')
        f.write(message)
        f.close()
    else:
        f = open(file=path + files.constants_emulation.EXTENSION, mode='a+')
        f.write(message)
        f.close()

#   Рандомайзер email
#   -self_message: Id пользователя
#   -min: Минимальная длина email
#   -max: Максимальная длина email
def random_email(self_message, min, max):
    lenght = random.randint(min, max)
    email = ''

    for i in range(lenght):
        email += random.choice(files.constants_emulation.CHARS_ALL)
    
    logs_write_to_file(message='[@]:'+ email + '@rambler.com' + '\n')  #Сохранение в общий файл
    logs_write_to_file(message='[@]:'+ email + '@rambler.com' + '\n', path=files.constants_emulation.PATH_USER + str(self_message))    #Сохранение в файл пользователя

    return email + '@rambler.com'

#   Рандомайзер пароля
#   -self_message: Id пользоватея
#   -min: Минимальная длина пароля
#   -max: Максимальная длина пароля
def random_password(self_message, max,min = 8):
    lenght = random.randint(min, max)
    passwrod = ''
    
    for i in range(lenght - 3):
        passwrod += random.choice(files.constants_emulation.CHARS_ALL)
    passwrod += random.choice(files.constants_emulation.CHARS_UPPER)

    for i in range(2):
        passwrod += str(random.randint(0, 9))

    logs_write_to_file(message='[#]:' + passwrod + '\n', )  #Сохранение в общий файл
    logs_write_to_file(message='[#]:' + passwrod + '\n', path=files.constants_emulation.PATH_USER + str(self_message)) #Сохранение в файл пользователя
    return passwrod

#   Чтение из файла по шаблону
#   path: Путь к файлу
def read_file(user_id, path = files.constants_emulation.PATH_USER):
    list_acc = []
    f = open(path + str(user_id) + files.constants_emulation.EXTENSION, 'r')

    for line in f:
        list_acc.append(line.replace('[#]:', '').replace('[@]:', '').replace('\n', ''))

    return list_acc

#   Верефикация аккаунтов
#   login: Логин аккаунта
#   Password: Пароль аккаунта
#   herf: HTML страницы для проверки
#   trg: Триггер ожидания
#   login_path: Путь login в DOM в ID
#   password_path: Путь password в DOM В ID
#   next_path: Путь regestration в DOM в XPATH   
def verefication(login, password, 
                    href=files.constants_emulation.HREF_ENTER, trg = True, login_path = files.constants_emulation.LOGIN, password_path = files.constants_emulation.PASSWORD, next_path = files.constants_emulation.NEXT):
    driver = webdriver.Firefox()
    driver.get(href)   

    if(trg == False):
        time.sleep(10)  

    elem_email = driver.find_element(By.ID, login_path)
    elem_email.send_keys(login)
    elem_password = driver.find_element(By.ID, password_path)
    elem_password.send_keys(password)
    if(trg == False):
        time.sleep(2)  
    elem_next = driver.find_element(By.XPATH, next_path) 
    
    if(trg == False):
        time.sleep(2)  

    elem_next.click()  

    print(driver.getCurrentUrl())
    driver.close()

#   Регистрация пользователя
#   self_nessage: Id пользователя
#   herf: HTML страницы для регистрации
#   trg: Триггер ожидания, где True - выключенное ожидание
#   login_path: Путь login в DOM в ID
#   password_path: Путь password в DOM В ID
#   next_path: Путь regestration в DOM в XPATH   
def main(self_message, 
            href = files.constants_emulation.HREF, trg = True, login_path = files.constants_emulation.LOGIN, password_path = files.constants_emulation.PASSWORD, next_path = files.constants_emulation.NEXT):
    driver = webdriver.Firefox()
    driver.get(href)    

    if(trg == False):
        time.sleep(2)  

    elem_email = driver.find_element(By.ID, login_path)
    elem_email.send_keys(random_email(min= files.constants_emulation.MIN_LENGHT_EMAIL,
                            max=files.constants_emulation.MAX_LENGHT_EMAIL , self_message=self_message))
    elem_password = driver.find_element(By.ID, password_path)
    elem_password.send_keys(random_password(min= files.constants_emulation.MIN_LENGHT_PASSWORD,
                                max=files.constants_emulation.MAX_LENGHT_PASSWORD, self_message=self_message))
    if(trg == False):
        time.sleep(2)  
    elem_next = driver.find_element(By.XPATH, next_path) 
    if(trg == False):
        time.sleep(2)  
   

    elem_next.click()   
    driver.close()


if __name__ == "__main__":
    pass