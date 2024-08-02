from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

import os
import requests
import mimetypes

from fastrpa.exceptions import ElementNotFound
from fastrpa.types import BrowserOptions, BrowserOptionsClass, WebDriver


VISIBILITY_TIMEOUT = 10
HIDDEN_TIMEOUT = 60


def get_browser_options(
    options: list[str], options_class: BrowserOptionsClass = ChromeOptions
) -> BrowserOptions:
    instance = options_class()
    for opt in options:
        instance.add_argument(opt)
    return instance


def get_element(
    webdriver_or_parent_node: WebDriver | WebElement,
    xpath: str,
    timeout: int = VISIBILITY_TIMEOUT,
) -> WebElement:
    try:
        return WebDriverWait(webdriver_or_parent_node, timeout).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )

    except ElementNotInteractableException:
        return WebDriverWait(webdriver_or_parent_node, timeout).until(
            expected_conditions.element_to_be_clickable((By.XPATH, xpath))
        )

    except TimeoutException:
        raise ElementNotFound(xpath, timeout)


def wait_until_element_is_hidden(
    webdriver_or_parent_node: WebDriver | WebElement,
    xpath: str,
    timeout: int = HIDDEN_TIMEOUT,
):
    WebDriverWait(webdriver_or_parent_node, timeout).until_not(
        expected_conditions.element_to_be_clickable((By.XPATH, xpath))
    )


def wait_until_element_is_present(
    webdriver_or_parent_node: WebDriver | WebElement,
    xpath: str,
    timeout: int = HIDDEN_TIMEOUT,
):
    WebDriverWait(webdriver_or_parent_node, timeout).until(
        expected_conditions.presence_of_element_located((By.XPATH, xpath))
    )


def get_select_element(
    webdriver_or_parent_node: WebDriver | WebElement,
    xpath: str,
    timeout: int = VISIBILITY_TIMEOUT,
) -> Select:
    return Select(get_element(webdriver_or_parent_node, xpath, timeout))


def get_element_text(
    webdriver_or_parent_node: WebDriver | WebElement,
    xpath: str,
    timeout: int = VISIBILITY_TIMEOUT,
) -> str | None:
    element = get_element(webdriver_or_parent_node, xpath, timeout)
    if element.text:
        return element.text
    elif value := element.get_attribute("value"):
        return value
    return None


def get_file_path(path: str) -> str:
    if os.path.isfile(path):
        return path

    file_response = requests.get(path)
    file_extension = mimetypes.guess_extension(file_response.headers["Content-Type"])
    file_hash = abs(hash(file_response.content))
    download_path = f"/tmp/{file_hash}{file_extension}"

    with open(download_path, "wb") as file:
        file.write(file_response.content)

    return download_path
