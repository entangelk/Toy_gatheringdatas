from importselenium import selenium_running
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from kyobo_intopage_yohan import into_screen,count_page,move_page,quitBrowser


def main(address) :
    try:
        browser = selenium_running(address)
        into_screen(browser)
        move_page(browser)
    except:
        pass    # 업무 코드 문제 발생 시 대처 코드
    finally :
        quitBrowser(browser)    # try나 except이 끝난 후 무조건 실행 코드
    return 0

if __name__ == "__main__":
    try:
        main('https://www.kyobobook.co.kr/')    # 업무 코드
    except:
        pass    # 업무 코드 문제 발생 시 대처 코드
    finally :
        address = 'https://www.kyobobook.co.kr/'
        browser = selenium_running(address)
        quitBrowser(browser)
        pass    # try나 except이 끝난 후 무조건 실행 코드
