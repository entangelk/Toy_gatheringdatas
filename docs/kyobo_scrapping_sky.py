
if __name__ == "__main__":
    try :      
        pass
    except :
        pass



# mongodb 연결 함수
def Mongo_connect(coll1, coll2) :
    from pymongo import MongoClient
    mongoclient = MongoClient("mongodb://localhost:27017")
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
    book_name = browser.find_element(by=By.CSS_SELECTOR, value='div.prod_title_box.auto_overflow_wrap > div > div')
    book_image = browser.find_element(by=By.CSS_SELECTOR, value='div > div.portrait_img_box.portrait > img').get_attribute('src')
    book_price = browser.find_element(by=By.CSS_SELECTOR, value='div.prod_price_box > div > span.price')
    browser.find_element(by=By.CSS_SELECTOR, value='div.sps_inner > ul > li:nth-child(3) > a').click()
    result = coll_book.insert_one({"책 이름":book_name, "책 사진" : book_image, "가격" : book_price}) #몽고디비에 책 데이터 넣기
    book_id = result.inserted_id
    return book_id

# 리뷰 정보 스크래핑 함수
def kyobo_comment_scrapping(browser, coll_book_comment, book_id):
    from selenium.common.exceptions import NoSuchElementException
    while True : 
        try :
            comment_lists = browser.find_elements(by=By.CSS_SELECTOR, value='div.comment_list > div')
            for comment_list in comment_lists :
                comment_user = comment_list.find_element(by=By.CSS_SELECTOR, value='div.left_area > div > span:nth-child(2)')
                comment_content = comment_list.find_element(by=By.CSS_SELECTOR, value='div.comment_contents')
                coll_book_comment.insert_one({"책ID":book_id
                                              ,"댓글 아이디" :comment_user
                                              ,"댓글 내용" : comment_content})
            browser.find_element(by=By.CSS_SELECTOR, value='div.tab_content > div > div.pagination > button.btn_page.next').click()
        except NoSuchElementException :
            break
    

coll_book, coll_book_comment = Mongo_connect("kyobo_best_book", "kyobo_best_book_comment")
browser = connectingwebsite("https://product.kyobobook.co.kr/detail/S000208779631")
book_id = kyobo_scrapping(browser, coll_book)
kyobo_comment_scrapping(browser, coll_book_comment, book_id)

