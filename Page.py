import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config


@allure.epic("Тестирование главной страницы интернет-магазина")
class Main_page:
    @allure.step("Иницилизировать браузер")
    def __init__(self, driver=None):
        """Инициализация страницы магазина"""
        if driver is None:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(10)
            self.driver.maximize_window()
            self._own_driver = True
        else:
            self.driver = driver
            self._own_driver = False
        self.wait = WebDriverWait(self.driver, 20)

    @allure.step("Открытие страницы магазина {URL}")
    def open(self, URL: str = None):
        """Открывает страницу по URL. Если URL не указан, использует BASE_URL из config"""
        if URL is None:
            URL = Config.BASE_URL
        self.driver.get(URL)

    @allure.step("Кликнуть по элементу {locator}")
    def click(self, locator: str):
        """нажимает на кнопку с указанным локатором"""
        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
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
    def find(self, locator: str):
        """находит элемент с указанным локатором"""
        return self.driver.find_elements(By.CSS_SELECTOR, locator)

    @allure.step("Закрыть всплывающие окна")
    def close_popups(self):
        """Закрывает различные всплывающие окна на странице"""
        popup_selectors = [
            '.popmechanic-close',
            '.popmechanic__close',
            '.close-button',
            '[data-testid="close-popup"]',
            '.modal-close',
            '.popup-close'
        ]
        for selector in popup_selectors:
            popups = self.find(selector)
            if popups:
                try:
                    popups[0].click()
                    self.waiting_load()
                except Exception as e:
                    print(f"Не удалось закрыть {selector}: {e}")

    @allure.step("Ожидание загрузки страницы")
    def waiting_load(self):
        """Ожидает полной загрузки страницы (readyState = complete)"""
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.loader, .spinner, .loading')))
        except Exception as e:
            print(f"Загрузчики не исчезли или не найдены: {e}")
        try:
            self.wait.until(lambda driver: driver.execute_script("return jQuery.active == 0"))
        except Exception as e:
            print(f"⚠️ jQuery не завершился или не используется: {e}")

    @allure.step("Прокрутка страницы до элемента{element}")
    def roll_for_element(self, element):
        elements = self.driver.find_element(By.CSS_SELECTOR, element)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", elements)

    @allure.step("Ожидание изменения URL")
    def waiting_load_cart(self):
        """Ожидает изменение URL при переходе в корзину"""
        self.wait.until(EC.url_contains("/cart"))
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.cart, .cart-page, .basket-page, [data-testid="cart-page"]')))

    @allure.step("Получить количество товаров в корзине")
    def get_cart_items_count(self):
        """Возвращает количество товаров в корзине"""
        items = self.find('[data-testid="cart-item"], .cart-item, .basket-item')
        return len(items)

    @allure.step("Проверить, что корзина не пуста")
    def assert_cart_not_empty(self):
        """Проверяет, что в корзине есть товары"""
        items_count = self.get_cart_items_count()
        assert items_count > 0, f"Корзина пуста, но должна содержать товары. Найдено: {items_count}"

    @allure.step("Проверить, что корзина пуста")
    def assert_cart_empty(self):
        """Проверяет, что корзина пуста"""
        items_count = self.get_cart_items_count()
        assert items_count == 0, f"Корзина должна быть пуста, но найдено товаров: {items_count}"

    @allure.step("Получить количество товара в корзине")
    def get_quantity(self) -> int:
        """Возвращает текущее количество товара"""
        quantity_inputs = self.find('.chg-app-input.chg-app-input--size-s')
        assert len(quantity_inputs) > 0, "Поле количества не найдено"
        value = quantity_inputs[0].get_attribute('value')
        return int(value) if value else 0

    @allure.step("Закрытие браузера")
    def close(self):
        """Окончание ссесии"""
        if self._own_driver:
            self.driver.quit()
