from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from utils.logger import *
import time


class TwitchSearchPage(BasePage):
    
    # 元素定位
    # 搜尋框
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search'], input[data-a-target='tw-input']")
    SEARCH_INPUT_2 = (By.XPATH, "//*[@id='twilight-sticky-header-root']/div/div/div/div/input")
    
    # Channels tab
    CHANNELS_TAB = (By.CSS_SELECTOR, "a[href*=channels], a[data-index='1']")
    CHANNELS_TAB_2 = (By.XPATH, "//div[text()='Channels']")

    
    def __init__(self, driver):
        super().__init__(driver)
    
    def enter_search_keyword(self, keyword):
        """輸入搜尋關鍵字"""
        log_info(f"Enter keyword: {keyword}")
        
        search_input = None
        try:
            self.wait_for_visible(self.SEARCH_INPUT, timeout=10)
            self.input_text(self.SEARCH_INPUT, keyword)
            search_input = self.find_element(self.SEARCH_INPUT)
        except:
            log_info("Use the 2nd search input locator")
            self.wait_for_visible(self.SEARCH_INPUT_2, timeout=10)
            self.input_text(self.SEARCH_INPUT_2, keyword)
            search_input = self.find_element(self.SEARCH_INPUT_2)
        
        search_input.send_keys(Keys.RETURN)
        log_info("Execute search")
        
        self.wait_for_url_contains("search", timeout=10)
        self.wait_for_page_load(timeout=10)
        log_info("Search results have loaded")

    def click_channels_tab(self):
        """點擊 Channels Tab"""
        log_info("Click Channels Tab")
        try:
            self.wait_for_visible(self.CHANNELS_TAB, timeout=10)
            self.wait_for_clickable(self.CHANNELS_TAB, timeout=10)
            self.click(self.CHANNELS_TAB, timeout=5)
            log_info("Switched to Channels Tab")
        except Exception as e:
            log_debug(f"Main locator failed: {e}")
            log_info(f"Use the 2nd locator")
            try:
                self.wait_for_clickable(self.CHANNELS_TAB_2, timeout=10)
                self.click(self.CHANNELS_TAB_2, timeout=5)
                log_info("Switched to Channels Tab (2nd locator)")
            except Exception as e2:
                log_error(f"Click Channels Tab failed: {e2}")
                raise
        
        self.wait_for_page_load(timeout=10)
        
        time.sleep(2)
        log_info("Channels content has loaded")

