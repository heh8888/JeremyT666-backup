from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.logger import *
from config.config import (
    BROWSER, HEADLESS, IMPLICIT_WAIT, 
    PAGE_LOAD_TIMEOUT, MOBILE_EMULATION
)


class DriverFactory:
    
    @staticmethod
    def get_driver():
        if BROWSER.lower() == "chrome":
            return DriverFactory._create_chrome_driver()
        else:
            raise ValueError(f"Unsupported browser type: {BROWSER}")
    
    @staticmethod
    def _create_chrome_driver():
        chrome_options = Options()
        
        # 手機模擬設定
        chrome_options.add_experimental_option("mobileEmulation", MOBILE_EMULATION)
        
        if HEADLESS:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox") # 禁用沙盒
        chrome_options.add_argument("--disable-notifications")  # 禁用browser通知請求

        log_debug(f"Chrome driver setting: mobile_emulation={MOBILE_EMULATION.get('deviceName', 'custom')}, headless={HEADLESS}")

        service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        log_debug("Chrome WebDriver created")
        
        # 設定等待時間
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        log_debug(f"Chrome wait time setting: implicit_wait={IMPLICIT_WAIT}s, page_load_timeout={PAGE_LOAD_TIMEOUT}s")
        
        return driver
