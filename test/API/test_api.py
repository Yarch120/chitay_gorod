import allure
import pytest
import requests
from config import Config
pytestmark = pytest.mark.api


@allure.suite("API тестирование Читай-город")
class TestChitaiGorodAPI:

    # Позитивные тесты

    @allure.feature("Корзина")
    @allure.story("Добавление книги")
    @allure.title("Добавление книги в корзину")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_book_to_cart(self):
        """Позитивный тест: добавление книги в корзину"""
        url = f"{Config.API_BASE_URL}/web/api/v1/cart/product"
        payload = {"id": Config.BOOK_ID}
        with allure.step(f"Отправить POST запрос на {url}"):
            response = requests.post(url, json=payload, headers=Config.HEADERS)
        with allure.step("Проверить статус ответа"):
            assert response.status_code in [200, 201]
        with allure.step("Проверить время ответа"):
            assert response.elapsed.total_seconds() < 3

    @allure.feature("Корзина")
    @allure.story("Изменение количества")
    @allure.title("Увеличение количества книги в корзине")
    @allure.severity(allure.severity_level.NORMAL)
    def test_increase_book_quantity(self):
        """Позитивный тест: увеличение количества книги до 2"""
        url = f"{Config.API_BASE_URL}/web/api/v1/cart"
        payload = {"id": Config.CART_ID, "quantity": 2}
        with allure.step(f"Отправить PUT запрос на {url}"):
            response = requests.put(url, json=payload, headers=Config.HEADERS)
        with allure.step("Проверить статус ответа"):
            assert response.status_code == 200

    @allure.feature("Корзина")
    @allure.story("Удаление")
    @allure.title("Удаление товара из корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_book_from_cart(self):
        """Позитивный тест: удаление книги из корзины"""
        url = f"{Config.API_BASE_URL}/web/api/v1/cart/product/{Config.CART_ID}"
        with allure.step(f"Отправить DELETE запрос на {url}"):
            response = requests.delete(url, headers=Config.HEADERS)
        with allure.step("Проверить статус ответа"):
            assert response.status_code in [200, 204]

    # Негативные тесты

    @allure.feature("Корзина")
    @allure.story("Негативные сценарии")
    @allure.title("Добавление несуществующего товара в корзину")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_nonexistent_book_to_cart(self):
        """Негативный тест: добавление несуществующей книги"""
        url = f"{Config.API_BASE_URL}/web/api/v1/cart/product"
        payload = {"id": 11234567}
        with allure.step(f"Отправить POST запрос с несуществующим ID"):
            response = requests.post(url, json=payload, headers=Config.HEADERS)
        with allure.step("Проверить статус ошибки"):
            assert response.status_code in [400, 404, 422]

    @allure.feature("Корзина")
    @allure.story("Негативные сценарии")
    @allure.title("Увеличение количества свыше 1000")
    @allure.severity(allure.severity_level.NORMAL)
    def test_increase_quantity_exceed_limit(self):
        """Негативный тест: увеличение количества свыше 1000"""
        url = f"{Config.API_BASE_URL}/web/api/v1/cart"
        payload = {"id": Config.CART_ID, "quantity": 1001}
        with allure.step(f"Отправить PUT запрос с quantity = 1001"):
            response = requests.put(url, json=payload, headers=Config.HEADERS)
        with allure.step("Проверить статус ошибки"):
            assert response.status_code in [400, 404, 422]

    @allure.feature("Безопасность")
    @allure.story("Негативные сценарии")
    @allure.title("Отправка запроса без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_request_without_auth(self):
        """Негативный тест: запрос без токена авторизации"""
        url = f"{Config.API_BASE_URL}/web/api/v1/cart/product"
        payload = {"id": Config.BOOK_ID}
        headers_without_auth = {"Content-Type": "application/json"}
        with allure.step("Отправить POST запрос без заголовка авторизации"):
            response = requests.post(url, json=payload, headers=headers_without_auth)
        with allure.step("Проверить статус ошибки"):
            assert response.status_code == 401
