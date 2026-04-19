import allure
import pytest
from Page import Main_page
from config import Config
pytestmark = pytest.mark.ui


@allure.suite("Cataloge page")
@allure.epic("Проверка поиска")
@allure.title("Проверка поиска по названию")
@allure.severity(allure.severity_level.BLOCKER)
def test_find_books_by_name(main_page):
    main_page.open(Config.BASE_URL)
    main_page.waiting_load()
    main_page.close_popups()
    search_inputs = main_page.find('#app-search')
    search_input = search_inputs[0]
    search_query = "Гарри"
    search_input.send_keys(search_query)
    main_page.waiting_load()
    main_page.click('.search-form__button-search')
    main_page.waiting_load()
    results = main_page.find('[data-testid="product-item"], .product-card')
    found = False
    for result in results[:5]:  # Проверяем первые 5 результатов
        title = result.text.lower()
        if search_query.lower() in title:
            found = True
            break
    assert found


@allure.suite("Cataloge page")
@allure.epic("Проверка поиска")
@allure.title("Проверка поиска по автору")
@allure.severity(allure.severity_level.BLOCKER)
def test_find_books_by_autor(main_page):
    main_page.open(Config.BASE_URL)
    main_page.waiting_load()
    main_page.close_popups()
    search_inputs = main_page.find('#app-search')
    search_input = search_inputs[0]
    search_query = "Булгаков"
    search_input.send_keys(search_query)
    main_page.waiting_load()
    main_page.click('.search-form__button-search')
    main_page.waiting_load()
    results = main_page.find('[data-testid="product-item"], .product-card')
    found = False
    for result in results[:5]:  # Проверяем первые 5 результатов
        title = result.text.lower()
        if search_query.lower() in title:
            found = True
            break
    assert found


@allure.suite("Cataloge page")
@allure.epic("Открытие каталога")
@allure.title("Проверка открытия каталога")
@allure.severity(allure.severity_level.BLOCKER)
def test_find_cataloge(main_page):
    main_page.open(Config.BASE_URL)
    main_page.waiting_load()
    main_page.close_popups()
    main_page.click('.header-sticky__catalog-menu')
    main_page.waiting_load()
    element = main_page.find('.categories-menu')
    assert element[0].is_displayed()
