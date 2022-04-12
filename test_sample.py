from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from Pages.locators import Locator


def test_sample_todo_app():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # launch the browser
    driver.get("https://aspireapp.odoo.com/web/login")
    driver.maximize_window()

    # login into the application
    driver.find_element(by=By.XPATH, value="//*[@name='login']").send_keys('user@aspireapp.com')
    driver.find_element(by=By.XPATH, value="//*[@name='password']").send_keys('@sp1r3app')
    driver.find_element(by=By.XPATH, value="//*[@type='submit']").click()
    driver.implicitly_wait(10)
    
    # go to inventory page
    driver.find_element(by=By.XPATH, value="//a[.='Inventory']").click()
    driver.find_element(by=By.XPATH, value="//span[.='Products']").click()
    driver.find_element(by=By.XPATH, value="//a[.='Products']").click()
    driver.find_element(by=By.XPATH, value="//*[contains(@title,'Create record')]").click()
    driver.implicitly_wait(10)

    pro_name = 'qwerty24'
    pro_quantity = 12

    # create a new product
    driver.find_element(by=By.XPATH, value="//input[@placeholder='e.g. Cheese Burger']").send_keys(pro_name)

    # update the quantity of the product created
    driver.find_element(by=By.XPATH, value="//*[contains(text(),'Update Quantity')]").click()

    try:
        element_clickable = EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Create')]"))
        WebDriverWait(driver, 10).until(element_clickable).click()
    except StaleElementReferenceException:
        print("Timed out waiting for page to load")

    driver.find_element(by=By.XPATH, value="//input[@name='inventory_quantity']").send_keys(Keys.CONTROL + 'a')
    driver.find_element(by=By.XPATH, value="//input[@name='inventory_quantity']").send_keys(Keys.BACKSPACE * 4)
    driver.find_element(by=By.XPATH, value="//input[@name='inventory_quantity']").send_keys(pro_quantity)
    driver.find_element(by=By.XPATH, value="//*[contains(text(),'Save')]").click()
    driver.find_element(by=By.XPATH, value="//a[.='Products']").click()
    driver.implicitly_wait(10)
    driver.find_element(by=By.XPATH, value="//input[contains(@placeholder,'Search...')]").send_keys(pro_name + '\n')
    driver.implicitly_wait(10)
    new_product = driver.find_elements(by=By.XPATH, value="//strong/span[contains(text(), " + pro_name + ")]")
    
    # validate that the product has been created successfully
    if new_product:
        print('product created successfully')
    else:
        pass

    # go to manufacturing page
    driver.find_element(by=By.XPATH, value="//a[@title='Home menu']").click()
    driver.find_element(by=By.XPATH, value="//div[.='Manufacturing']").click()
    
    # create new manufacturing order
    driver.find_element(by=By.XPATH, value="//*[contains(text(),'Create')]").click()

    driver.find_element(by=By.XPATH,
                        value="//div[@name='product_id']/div/div/input[starts-with(@id,'o_field_input')]").send_keys(
        pro_name + '\n')
    sleep(3)
    driver.find_element(by=By.XPATH,
                        value="//input[contains(@class,'o_required_modifier oe_inline text-left')]").send_keys(
        Keys.CONTROL + 'a')
    driver.find_element(by=By.XPATH,
                        value="//input[contains(@class,'o_required_modifier oe_inline text-left')]").send_keys(
        Keys.BACK_SPACE * 4)
    driver.find_element(by=By.XPATH,
                        value="//input[contains(@class,'o_required_modifier oe_inline text-left')]").send_keys(
        pro_quantity)
    driver.find_element(by=By.XPATH, value="//*[contains(text(),'Save')]").click()
    driver.implicitly_wait(5)
    manufacturing_order = driver.find_element(by=By.XPATH, value="//span[@placeholder='Manufacturing Reference']").text
    driver.implicitly_wait(10)

    driver.find_element(by=By.XPATH, value="//span[.='Confirm']").click()
    driver.implicitly_wait(10)
    
    # mark the state of the order as done
    driver.find_element(by=By.XPATH, value="//button[@confirm]/span[.='Mark as Done']").click()

    driver.implicitly_wait(10)
    try:
        element_present = EC.element_to_be_clickable((By.XPATH, "//span[.='Ok']"))
        WebDriverWait(driver, 10).until(element_present).click()
    except NoSuchElementException:
        print("Timed out waiting for page to load")
    driver.find_element(by=By.XPATH, value="//button[@name='process']/span['Apply']").click()

    driver.find_element(by=By.XPATH, value="// a[.='Manufacturing Orders']").click()
    sleep(2)
    
    # search for the manufacturing order
    driver.find_element(by=By.XPATH, value="//input[contains(@placeholder,'Search...')]").send_keys(Keys.BACK_SPACE * 2)
    driver.find_element(by=By.XPATH, value="//input[contains(@placeholder,'Search...')]").send_keys(
        manufacturing_order + '\n')

    quantity = float(driver.find_element(by=By.XPATH, value="//td[@name='product_qty']").text)
    state = driver.find_element(by=By.XPATH, value="//span[@name='state']").text

    # check if the order has been created with correct data (here quantity and state of the order)
    if quantity > 10 and state == 'Done':
        print('manufacturing order is correctly placed')


test_sample_todo_app()

