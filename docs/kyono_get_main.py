from importselenium import selenium_running
from kyobo_scrapping_sky import Mongo_connect
from kyobo_intopage_yohan import into_screen,move_page,quitBrowser


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



# main('https://www.kyobobook.co.kr/')


if __name__ == "__main__":
    try:
        address = 'https://www.kyobobook.co.kr/'
        main(address)    # 업무 코드
    except:
        pass    # 업무 코드 문제 발생 시 대처 코드
    finally :
        pass    # try나 except이 끝난 후 무조건 실행 코드

