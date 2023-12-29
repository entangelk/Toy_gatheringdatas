
if __name__ == "__main__":
    try :      
        pass
    except :
        pass



# mongodb 연결 함수. 변수 = 두 개의 collection 이름
def Mongo_connect(coll1, coll2) :
    from pymongo import MongoClient
    mongoclient = MongoClient("mongodb://192.168.0.145:27017")
    database = mongoclient["gatheringdatas"]
    coll_book = database[coll1]
    coll_book_comment = database[coll2]
    coll_book.delete_many({})
    coll_book_comment.delete_many({})
    return coll_book, coll_book_comment

# 사이트 연결 함수 sitename에 사이트 주소 삽입
def connectingwebsite(sitename):
    from selenium import webdriver
    browser = webdriver.Chrome()
    browser.get(sitename)
    return browser

# 책 정보 스크래핑 함수
def kyobo_scrapping(browser, coll_book): #책이름, 사진, 판매가, 리뷰 # coll_book은 책정보 입력하는 collection name
    from selenium.webdriver.common.by import By
    book_name = browser.find_element(by=By.CSS_SELECTOR, value='div.prod_title_box.auto_overflow_wrap > div > div').text # 책 이름
    book_writer = browser.find_element(by=By.CSS_SELECTOR, value='div.prod_author_box.auto_overflow_wrap > div.auto_overflow_contents > div > div').text # 책 저자
    book_image = browser.find_element(by=By.CSS_SELECTOR, value='div > div.portrait_img_box.portrait > img').get_attribute('src') # 책 이미지 링크
    book_price = browser.find_element(by=By.CSS_SELECTOR, value='div.prod_price_box > div > span.price').text # 책 가격
    book_grade = browser.find_element(by=By.CSS_SELECTOR, value='div.caption > span > span.val').text # 책 총 평점
    result = coll_book.insert_one({"책 이름":book_name, "저자" : book_writer ,"책 사진" : book_image, "가격" : book_price, "사용자 총점" : book_grade}) #몽고디비에 책 데이터 넣기
    book_id = result.inserted_id # 삽입된 책의 고유 ID
    return book_id, book_name

# 리뷰 정보 스크래핑 함수
def kyobo_comment_scrapping(browser, coll_book_comment, book_name, book_id):
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.by import By
    while True : 
        comment_lists = browser.find_elements(by=By.CSS_SELECTOR, value='div.comment_list > div')
        for comment_list in comment_lists :
            comment_user = comment_list.find_element(by=By.CSS_SELECTOR, value='div.left_area > div > span:nth-child(2)').text
            try :
                browser.execute_script('var extra_btn = document.querySelector(\'div.comment_footer > button > span.ico_arw\'); extra_btn.click();')
                time.sleep(1)
            except NoSuchElementException:
                pass
            comment_content = comment_list.find_element(by=By.CSS_SELECTOR, value='div.comment_contents').text
            coll_book_comment.insert_one({"책ID":book_id
                                            ,"책 이름" : book_name
                                            ,"댓글 아이디" :comment_user
                                            ,"댓글 내용" : comment_content}) 
            # 리뷰 다음 페이지로 넘어가기(JavaScript 사용)
            try :
                browser.execute_script ('var btn = document.querySelector(\'div.tab_content > div > div.pagination > button.btn_page.next\'); btn.click();')
                time.sleep(2)
            except:
                break

# 브라우저 종료 함수
def browser_quit(browser):
    browser.quit()
    return 0
    

# 요기 아래에 있는게 main 에 들어가야 하는 방식

import time
coll_book, coll_book_comment = Mongo_connect("kyobo_best_book", "kyobo_best_book_comment")
browser = connectingwebsite("https://product.kyobobook.co.kr/detail/S000208779631")
time.sleep(2)
book_id, book_name= kyobo_scrapping(browser, coll_book)
kyobo_comment_scrapping(browser, coll_book_comment, book_name, book_id)
browser_quit(browser)