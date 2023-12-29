from importselenium import selenium_running
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

address = 'https://www.kyobobook.co.kr/'
browser = selenium_running(address)

def into_screen():
    time.sleep(3)
    element_click = browser.find_element(by=By.CSS_SELECTOR,value='#welcome_header_wrap > div.header_inner > nav > ul.gnb_list > li:nth-child(3) > a')
    element_click.click()
    time.sleep(1)
    return

def count_page():
    element_bundle = browser.find_elements(by=By.CSS_SELECTOR,value='#tabRoot > div.view_type_list.switch_prod_wrap>ol>li.prod_item')
    item_count = 0
    for i in element_bundle:
        item_count+=1
    return item_count

def move_page():
    element_click = browser.find_element(by=By.CSS_SELECTOR,value='#tabRoot > div.view_type_list.switch_prod_wrap > ol:nth-child(1) > li > div.prod_area.horizontal > div.prod_info_box > div.auto_overflow_wrap.prod_name_group > div > div > a')
    element_click.click()    



def quitBrowser(browser):
    # 브라우저 종료
    browser.quit()
    return 0


if __name__ == "__main__":
    # find_element().click()
    address = 'https://www.kyobobook.co.kr/'