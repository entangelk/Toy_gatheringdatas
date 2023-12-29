# from importselenium import selenium_running
import time
from selenium.webdriver.common.by import By
pass
from kyobo_scrapping_sky import Mongo_connect,kyobo_scrapping,kyobo_comment_scrapping,connectingwebsite
pass



def into_screen(browser):  # 상품 리스트 페이지 진입

    time.sleep(3)
    element_click = browser.find_element(by=By.CSS_SELECTOR,value='#welcome_header_wrap > div.header_inner > nav > ul.gnb_list > li:nth-child(3) > a')
    element_click.click()
    time.sleep(1)
    return

def count_page(browser):   # 리스트 페이지에 있는 아이템 갯수 카운팅
    element_bundle = browser.find_elements(by=By.CSS_SELECTOR,value='#tabRoot > div.view_type_list.switch_prod_wrap>ol>li.prod_item')   # 아이템 전체 호출
    item_count = 0  # 카운트 초기화
    for i in element_bundle:
        item_count+=1   # 아이템 갯수만큼 카운팅
    return item_count

def move_page(browser):
    for j in range(10):  # 10개의 페이지 수집할 예정
        for i in range(count_page(browser)):   # 1개 페이지에서 아이템 갯수만큼 반복
            browser.get(browser.current_url)
            try : 
                element_click = browser.find_element(by=By.CSS_SELECTOR, value='body > div.burst_banner_wrap > button').click() # 화면을 가리는 하단 베너 닫기
                time.sleep(1)
                element_click = browser.find_element(by=By.CSS_SELECTOR, value='#ui-id-30 > div.dialog_footer > button.btn_md.btn_primary').click() # 베너 닫기 확인창 닫기
            except:
                pass
            time.sleep(1)

            try:
                element_click = browser.find_element(by=By.XPATH, value=f'/html/body/div[3]/main/section[2]/div/section/div[2]/div[2]/div[7]/div[4]/ol[1]/li[{i+1}]/div[2]/div[1]/a').click()   # 화면 내 2개의 상품 저장 리스트 존재 (첫번째 리스트 클릭)
            except:
                try:
                    element_click = browser.find_element(by=By.XPATH, value=f'/html/body/div[3]/main/section[2]/div/section/div[2]/div[2]/div[7]/div[4]/ol[2]/li[{i-9}]/div[2]/div[1]/a').click()   # 첫번째 리스트가 종료되어 없다면 두번째 리스트 클릭
                except:
                    quitBrowser()   # 화면 내 아이템이 없다면 종료
                    pass
            browser.get(browser.current_url)

            # 하늘님 펑션 들어가는 곳
            coll_book, coll_book_comment = Mongo_connect("kyobo_best_book", "kyobo_best_book_comment")
            book_id, book_name= kyobo_scrapping(browser, coll_book)
            kyobo_comment_scrapping(browser, coll_book_comment, book_name, book_id)
            
            browser.back()  # DB 전송 후 뒤로가기
            time.sleep(3)
            pass
        browser.get(browser.current_url)
        try:
            element_click = browser.find_element(by=By.CSS_SELECTOR,value='#tabRoot > div.view_type_list.switch_prod_wrap > div.pagination > button.btn_page.next') # 다음 페이지로 이동
            element_click.click()
        except:
            quitBrowser()   # 다음 페이지가 없다면 종료

        time.sleep(3)
        pass
    return

def quitBrowser(browser):
    # 브라우저 종료
    browser.quit()
    return 0


if __name__ == "__main__":
    address = 'https://www.kyobobook.co.kr/'
    browser = connectingwebsite(address)
    pass

into_screen(browser)
pass
move_page(browser)

