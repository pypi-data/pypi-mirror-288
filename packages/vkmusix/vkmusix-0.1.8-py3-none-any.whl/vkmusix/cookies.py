#  VKMusix — VK Music API Client Library for Python
#  Copyright (C) 2024—present to4no4sv <https://github.com/to4no4sv/VKMusix>
#
#  This file is part of VKMusix.
#
#  VKMusix is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  VKMusix is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with VKMusix. If not, see <http://www.gnu.org/licenses/>.

import os
import time
import pickle
from typing import Union

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from .errors import errorsDict, createErrorClass


def getCookies(login: Union[str, int], password: Union[str, int], cookieFilename: Union[str, int] = None) -> str:
    if not cookieFilename:
        cookieFilename = login

    if isinstance(cookieFilename, int):
        cookieFilename = str(cookieFilename)

    options = Options()
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")

    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://vk.com/")

    loginInput = driver.find_element(By.ID, "index_email")
    loginInput.send_keys(login)
    loginInput.send_keys(Keys.RETURN)
    time.sleep(2)  # Ждём редирект на следующую страницу

    # Проверяем, не появилась ли ошибка «Слишком много попыток»
    try:
        errorPopup = driver.find_element(By.ID, "auth-popup-description")
        if errorPopup and ("Слишком много попыток" in errorPopup.text or "Too many attempts" in errorPopup.text):
            driver.quit()
            errorType = "VKTooManyLoginAttempts"
            error = errorsDict.get(errorType)
            raise createErrorClass(errorType)("🇷🇺: " + error.ru + " 🇬🇧: " + error.en)

    except selenium.common.exceptions.WebDriverException:
        pass

    try:
        passwordInput = driver.find_element(By.NAME, "password")

    except selenium.common.exceptions.NoSuchElementException:
        # Нажимаем на кнопку "Подтвердить другим способом"
        otherMethodsButton = driver.find_element(By.XPATH, '//button[@data-test-id="other-verification-methods"]')
        otherMethodsButton.click()
        time.sleep(1)  # Ждём открытия окошка выбора

        # Выбираем метод подтверждения через пароль
        passwordMethodButton = driver.find_element(By.XPATH, '//div[@data-test-id="verificationMethod_password"]')
        passwordMethodButton.click()
        time.sleep(1)  # Ждём появления поля ввода пароля

        passwordInput = driver.find_element(By.NAME, "password")

    passwordInput.send_keys(password)
    passwordInput.send_keys(Keys.RETURN)

    time.sleep(2) # Ждём завершения входа

    # Проверяем успешность входа
    if "feed" not in driver.current_url:
        driver.quit()
        errorType = "VKUnsuccessfulLoginAttempt"
        error = errorsDict.get(errorType)
        raise createErrorClass(errorType)("🇷🇺: " + error.ru + " 🇬🇧: " + error.en)

    # Сохраняем куки в файл
    cookies = driver.get_cookies()
    with open(f"{cookieFilename}.VKCookie", "wb") as f:
        pickle.dump(cookies, f)

    driver.quit()
    return cookieFilename


def checkCookies(cookieFilename: Union[str, int]) -> list:
    with open(f"{cookieFilename}.VKCookie", "rb") as f:
        cookies = pickle.load(f)
    return cookies

    options = Options()
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")

    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://vk.com/")
    driver.delete_all_cookies()  # Удаляем все старые куки перед добавлением новых

    with open(f"{cookieFilename}.VKCookie", "rb") as f:
        cookies = pickle.load(f)

    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get("https://vk.com/")
    time.sleep(.25)
    if "feed" not in driver.current_url:  # Проверяем, произошёл ли редирект на страничку с новостями
        driver.quit()
        os.remove(f"{cookieFilename}.VKCookie")
        errorType = "VKInvalidCookie"
        error = errorsDict.get(errorType)
        raise createErrorClass(errorType)("🇷🇺: " + error.ru + " 🇬🇧: " + error.en)

    driver.quit()
    return cookies