import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Page import Main_page


@pytest.fixture
def driver():
    """Фикстура для создания драйвера"""
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def main_page(driver):
    """Фикстура для главной страницы"""
    return Main_page(driver)  # Передаем driver в Page


@pytest.fixture
def product_page(main_page):
    """
    ПРЕДУСЛОВИЕ: переход на страницу товара
    """
    main_page.driver.get("https://www.chitai-gorod.ru/product/python-polnoe-rukovodstvo-2893579")
    main_page.waiting_load()
    return main_page


@pytest.fixture
def empty_cart_page(driver):
    """ПРЕДУСЛОВИЕ: открытая пустая корзина"""
    page = Main_page(driver)
    page.driver.get("https://www.chitai-gorod.ru/cart")
    page.waiting_load()
    return page


@pytest.fixture
def cart_page_with_specific_product(main_page):
    """
    ПРЕДУСЛОВИЕ: корзина с конкретным товаром, товар выбирается при вводе прямого URL на страницу товара
    """
    main_page.driver.get("https://www.chitai-gorod.ru/product/python-polnoe-rukovodstvo-2893579")
    main_page.waiting_load()
    try:
        add_button = main_page.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.product-buttons.product-offer__buttons'))
        )
        add_button.click()
        main_page.waiting_load()
    except Exception as e:
        print(f"⚠️ Не удалось добавить товар: {e}")
    main_page.click('[data-testid-button-header="cart"]')
    main_page.waiting_load()
    main_page.wait.until(EC.url_contains("/cart"))
    return main_page


@pytest.fixture
def cart_page_with_twice_items(main_page):
    """
    ПРЕДУСЛОВИЕ: корзина с товаром в количестве 2 штуки
    """
    main_page.driver.get("https://www.chitai-gorod.ru/product/python-polnoe-rukovodstvo-2893579")
    main_page.waiting_load()
    try:
        add_button = main_page.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.product-buttons.product-offer__buttons'))
        )
        add_button.click()
        main_page.waiting_load()
    except Exception as e:
        print(f"⚠️ Не удалось добавить товар: {e}")
    main_page.click('[data-testid-button-header="cart"]')
    main_page.waiting_load()
    main_page.wait.until(EC.url_contains("/cart"))
    quantity_input = main_page.find('#v-0-1')
    if quantity_input:
        current_value = quantity_input[0].get_attribute('value')
        if int(current_value) < 2:
            increase_button = main_page.find('.chg-ui-input-number__input-control--increment')
            if increase_button:
                increase_button[0].click()
                main_page.waiting_load()
    final_quantity = main_page.find('#v-0-1')[0].get_attribute('value')
    assert int(final_quantity) == 2, f"Количество товара = {final_quantity}, ожидалось 2"
    return main_page
