def selenium_running(get_address):

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    

    webdriver_manager_directory = ChromeDriverManager().install()
    browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))
    # ChromeDriver 실행

    # Chrome WebDriver의 capabilities 속성 사용
    capabilities = browser.capabilities

    # - 주소  입력
    browser.get(get_address)

    # - 가능 여부에 대한 OK 받음
    pass
    # - html 파일 받음(and 확인)
    html = browser.page_source

    return browser