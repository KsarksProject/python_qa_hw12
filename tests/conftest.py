import os
import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import allure_attach

def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='100.0',
        help='Версия браузера для запуска тестов (например, 112.0)'
    )
    parser.addoption(
        '--browser_type',
        default='chrome',
        help='Тип браузера для запуска тестов (например, chrome)'
    )

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture(scope="function")
def browser_management(request):
    # Используем значения по умолчанию, если параметры не переданы
    browser_version = request.config.getoption('--browser_version') or '100.0'
    browser_type = request.config.getoption('--browser_type') or 'chrome'
    options = Options()

    selenoid_capabilities = {
        "browserName": browser_type,
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True,
            "screenResolution": "1280x1024"  # Передаем разрешение в виде строки
        }
    }

    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    if not login or not password:
        raise Exception("Переменные окружения LOGIN и PASSWORD должны быть установлены!")

    options.page_load_strategy = 'eager'
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub",
        options=options
    )

    browser.config.driver = driver

    yield browser

    # Добавляем вложения для отчета Allure
    allure_attach.add_screenshot(browser)
    allure_attach.add_logs(browser)
    allure_attach.add_html(browser)
    allure_attach.add_video(browser)

    browser.quit()
