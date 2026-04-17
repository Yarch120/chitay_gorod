import allure
import pytest
from Page import Main_page
from config import Config

@allure.suite("Main page")
@allure.epic("Открытие сайта")
@allure.title("Проверка открытия главной страницы")
@allure.severity(allure.severity_level.BLOCKER)
def test_open(main_page):
    main_page.open(Config.BASE_URL)
    main_page.close()


@allure.suite("Main page")
@allure.epic("Переход в корзину")
@allure.title("Переход в корзину по кнопке 'Корзина'")
@allure.severity(allure.severity_level.CRITICAL)
def test_go_cart_page(main_page):
    main_page.open(Config.BASE_URL)
    main_page.waiting_load()
    main_page.click('[data-testid-button-header="cart"]')
    main_page.waiting_load_cart()
    main_page.waiting_load()
    expected_url = f"{Config.BASE_URL}/cart"
    actual_url = main_page.driver.current_url
    assert actual_url == expected_url
    main_page.close()


@allure.suite("Main page")
@allure.epic("Карточка товара")
@allure.title("Переход на карточку товара при нажатии на изображение")
@allure.severity(allure.severity_level.CRITICAL)
def test_go_product_page(main_page):
    main_page.open(Config.BASE_URL)
    main_page.waiting_load()
    old_url = main_page.driver.current_url
    main_page.close_popups()
    main_page.roll_for_element('.product-carousel__slide')
    products = main_page.find('.product-carousel__slide')
    assert len(products) > 0, "Товары не найдены"
    main_page.waiting_load()
    products[0].click()
    main_page.waiting_load()
    new_url = main_page.driver.current_url
    assert new_url != old_url
    main_page.close()
