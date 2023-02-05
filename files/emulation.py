from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

min_for_lenght_password = 8
min_for_lenght_email = 8
max_for_lenght_password = 16
max_for_lenght_email = 12
chars_all = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
chars_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
path_logs = 'files\documents\logs.txt'
path_all_logs = 'files\\documents\\all_logs.txt'

token = "5692335647:AAH32tS7q8g03A4Ia37wFX1zz5yNov8lG_I"

template_sticker_id = 'CAACAgIAAxkBAAMlY6RPx5-MocCkLSCbTa12CTWiRXEAAmYAA6JJHjIv90aQvKOfxCwE'


href = "https://id.rambler.ru/login-20/registration"
href_enter = "https://mail.rambler.ru/"

def logs_write_to_file(message, path= path_logs):
    f = open(path, 'a')
    f.write(message)
    f.close()

def random_email(min, max):
    lenght = random.randint(min, max)
    email = ''

    for i in range(lenght):
        email += random.choice(chars_all)
    
    logs_write_to_file('[@]:'+ email + '@rambler.com' + '\n')
    logs_write_to_file('[@]:'+ email + '@rambler.com' + '\n', path=path_all_logs)
    return email + '@rambler.com'

def random_password(max,min = 8):
    lenght = random.randint(min, max)
    passwrod = ''
    
    for i in range(lenght - 3):
        passwrod += random.choice(chars_all)
    passwrod += random.choice(chars_upper)
    for i in range(2):
        passwrod += str(random.randint(0, 9))

    logs_write_to_file(message='[#]:' + passwrod + '\n', )
    logs_write_to_file(message='[#]:' + passwrod + '\n', path=path_all_logs)
    return passwrod

def read_file(path = path_logs):
    list_acc = []
    f = open(path, 'r')
    for line in f:
        list_acc.append(line.replace('[#]:', '').replace('[@]:', '').replace('\n', ''))
    return list_acc

def verefication(login, password, trg = True):
    driver = webdriver.Firefox()
    driver.get(href_enter)   

    time.sleep(1)

    elem_email = driver.find_element(By.ID, "login")
    elem_email.send_keys(login)
    elem_password = driver.find_element(By.ID, "password")
    elem_password.send_keys(password)
    elem_next = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div/div/div/div[1]/form/button/span") 
    elem_next.click()

    if(trg == False):
        time.sleep(5)  
    driver.close()

def main(href = href, trg = True):
    driver = webdriver.Firefox()
    driver.get(href)    

    time.sleep(1)  

    elem_email = driver.find_element(By.ID, "login")
    elem_email.send_keys(random_email(min=min_for_lenght_email,
                            max=max_for_lenght_password))
    elem_password = driver.find_element(By.ID, "password")
    elem_password.send_keys(random_password(min=min_for_lenght_password,
                                max=max_for_lenght_password))
    elem_next = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div/div/div/div[1]/form/button/span") 
    elem_next.click()
    if(trg == False):
        time.sleep(5)  
    driver.close()

if __name__ == "__main__":
    pass