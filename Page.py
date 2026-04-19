import allure
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
from typing import List, Optional


@allure.epic("Тестирование главной страницы интернет-магазина")
class Main_page:
    
    @allure.step("Иницилизировать браузер")
    def __init__(self, driver: Optional[WebDriver] = None) -> None:
        """Инициализация страницы магазина"""
        if driver is None:
            self.driver: WebDriver = webdriver.Chrome()
            self.driver.implicitly_wait(10)
            self.driver.maximize_window()
            self._own_driver: bool = True
        else:
            self.driver: WebDriver = driver
            self._own_driver: bool = False
        self.wait: WebDriverWait = WebDriverWait(self.driver, 20)

    @allure.step("Открытие страницы магазина {URL}")
    def open(self, URL: Optional[str] = None) -> None:
        """Открывает страницу по URL. Если URL не указан, использует BASE_URL из config"""
        if URL is None:
            URL = Config.BASE_URL
        self.driver.get(URL)

    @allure.step("Кликнуть по элементу {locator}")
    def click(self, locator: str) -> None:
        """нажимает на кнопку с указанным локатором"""
        element: WebElement = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
        try:
            element.click()
        except:
            try:
                self.driver.execute_script("arguments[0].click();", element)
            except:
                try:
                    from selenium.webdriver.common.action_chains import ActionChains
                    ActionChains(self.driver).move_to_element(element).click().perform()
                except Exception as e:
                    raise AssertionError(f"Не удалось кликнуть по {locator}: {e}")

    @allure.step("найти элемент по локатору {locator}, для дальнейшей с ним работой")
    def find(self, locator: str) -> List[WebElement]:
        """находит элемент с указанным локатором"""
        return self.driver.find_elements(By.CSS_SELECTOR, locator)

    @allure.step("Закрыть всплывающие окна")
    def close_popups(self) -> None:
        """Закрывает различные всплывающие окна на странице"""
        popup_selectors: List[str] = [
            '.popmechanic-close',
            '.popmechanic__close',
            '.close-button',
            '[data-testid="close-popup"]',
            '.modal-close',
            '.popup-close'
        ]
        for selector in popup_selectors:
            popups: List[WebElement] = self.find(selector)
            if popups:
                try:
                    popups[0].click()
                    self.waiting_load()
                except Exception as e:
                    print(f"Не удалось закрыть {selector}: {e}")

    @allure.step("Ожидание загрузки страницы")
    def waiting_load(self) -> None:
        """Ожидает полной загрузки страницы (readyState = complete)"""
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.loader, .spinner, .loading')))
        except Exception as e:
            print(f"Загрузчики не исчезли или не найдены: {e}")

    @allure.step("Прокрутка страницы до элемента {element}")
    def roll_for_element(self, element: str) -> None:
        """Прокручивает страницу до указанного элемента"""
        elements: WebElement = self.driver.find_element(By.CSS_SELECTOR, element)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", elements)

    @allure.step("Ожидание изменения URL")
    def waiting_load_cart(self) -> None:
        """Ожидает изменение URL при переходе в корзину"""
        self.wait.until(EC.url_contains("/cart"))
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.cart, .cart-page, .basket-page, [data-testid="cart-page"]')))

    @allure.step("Получить количество товаров в корзине")
    def get_cart_items_count(self) -> int:
        """Возвращает количество товаров в корзине"""
        items: List[WebElement] = self.find('[data-testid="cart-item"], .cart-item, .basket-item')
        return len(items)

    @allure.step("Проверить, что корзина не пуста")
    def assert_cart_not_empty(self) -> None:
        """Проверяет, что в корзине есть товары"""
        items_count: int = self.get_cart_items_count()
        assert items_count > 0, f"Корзина пуста, но должна содержать товары. Найдено: {items_count}"

    @allure.step("Проверить, что корзина пуста")
    def assert_cart_empty(self) -> None:
        """Проверяет, что корзина пуста"""
        items_count: int = self.get_cart_items_count()
        assert items_count == 0, f"Корзина должна быть пуста, но найдено товаров: {items_count}"

    @allure.step("Получить количество товара в корзине")
    def get_quantity(self) -> int:
        """Возвращает текущее количество товара"""
        quantity_inputs: List[WebElement] = self.find('.chg-app-input.chg-app-input--size-s')
        if len(quantity_inputs) == 0:
            quantity_inputs = self.find('#v-0-1')
        assert len(quantity_inputs) > 0, "Поле количества не найдено"
        value: Optional[str] = quantity_inputs[0].get_attribute('value')
        return int(value) if value else 0

    @allure.step("Закрытие браузера")
    def close(self) -> None:
        """Окончание ссесии"""
        if self._own_driver:
            self.driver.quit()