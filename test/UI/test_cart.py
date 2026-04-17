import allure
import pytest
from Page import Main_page


@allure.suite("Cart page")
@allure.epic("Открытие сайта")
@allure.title("Проверка открытия корзины")
@allure.severity(allure.severity_level.BLOCKER)
def test_open_cart(main_page):
    """сайт открывается при переходе по ссылке https://www.chitai-gorod.ru/cart"""
    main_page.open('https://www.chitai-gorod.ru/cart')
    main_page.close()


@allure.suite("Cart page")
@allure.story("Просмотр корзины")
@allure.title("Проверка, что в корзине есть добавленный товар")
@allure.severity(allure.severity_level.CRITICAL)
def test_cart_has_product(cart_page_with_specific_product):
    """Тест использует предусловие - корзина уже с товаром"""
    assert "/cart" in cart_page_with_specific_product.driver.current_url
    cart_page_with_specific_product.assert_cart_not_empty()


@allure.suite("Cart page")
@allure.story("Увеличение количества")
@allure.title("Проверка, что в корзине можно увеличить количество существующего товара")
@allure.severity(allure.severity_level.CRITICAL)
def test_increase_cart_has_product(cart_page_with_specific_product):
    """Тест использует предусловие - корзина уже с товаром"""
    cart_page_with_specific_product.waiting_load()
    old_quantity_inputs = cart_page_with_specific_product.find('#v-0-1')
    old_value = old_quantity_inputs[0].get_attribute('value')
    cart_page_with_specific_product.click('.chg-ui-input-number__input-control.chg-ui-input-number__input-control--increment')
    cart_page_with_specific_product.waiting_load()
    new_quantity_inputs = cart_page_with_specific_product.find('#v-0-1')
    new_value = new_quantity_inputs[0].get_attribute('value')
    assert int(new_value) == int(old_value) + 1


@allure.suite("Cart page")
@allure.story("Уменьшение количества")
@allure.title("Проверка уменьшения количества товара")
@allure.severity(allure.severity_level.CRITICAL)
def test_decrease_cart_quantity(cart_page_with_twice_items):
    """Тест использует предусловие - корзина уже с товаром в количестве 2-ух штук"""
    quantity_input = cart_page_with_twice_items.find('#v-0-1')
    old_value = int(quantity_input[0].get_attribute('value'))
    cart_page_with_twice_items.click('.chg-ui-input-number__input-control.chg-ui-input-number__input-control--decrement')
    # Проверяем новое количество
    new_quantity_input = cart_page_with_twice_items.find('#v-0-1')
    new_value = int(new_quantity_input[0].get_attribute('value'))
    assert new_value == old_value - 1


@allure.suite("Cart page")
@allure.story("Очистка корзины")
@allure.title("Проверка, что в корзине можно удалить все товары")
@allure.severity(allure.severity_level.BLOCKER)
def test_delete_product_cart(cart_page_with_specific_product):
    """Тест использует предусловие - корзина уже с товаром"""
    cart_page_with_specific_product.waiting_load()
    cart_page_with_specific_product.click('.cart-item__delete-button')
    cart_page_with_specific_product.waiting_load()
    cart_page_with_specific_product.click('.cart-item-deleted__close')
    cart_page_with_specific_product.waiting_load()
    assert "/cart" in cart_page_with_specific_product.driver.current_url
    cart_page_with_specific_product.assert_cart_empty()
