import allure
import pytest
from Page import Main_page


@allure.suite("Product page")
@allure.story("Просмотр товара")
@allure.title("Проверка, что товар можно добавить в корзину")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_product_in_cart(product_page):
    """Тест использует предусловие - находимся на странице товара"""
    product_page.waiting_load()
    product_page.close_popups()
    product_page.click('.product-buttons.product-offer__buttons')
    product_page.waiting_load()
    counter_elements = product_page.find('.header-controls__indicator')
    counter_value = int(counter_elements[0].text)
    assert counter_value >= 1
