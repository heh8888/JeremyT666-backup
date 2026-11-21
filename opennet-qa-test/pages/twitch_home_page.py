from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import TWITCH_URL
from utils.logger import *
import time


class TwitchHomePage(BasePage):
    
    # 元素定位
    BROWSE_ICON = (By.CSS_SELECTOR, "a[href='/directory'] div.CoreText-sc-1txzju1-0")
    BROWSE_ICON_2 = (By.XPATH, "//*[@id='root']/div[2]/a[2]/div/div[1]")
    
    def __init__(self, driver):
        super().__init__(driver)    # super init 直接繼承basepage init
        self.url = TWITCH_URL
    
    def open(self):
        """開啟 Twitch 首頁"""
        self.driver.get(self.url)
        log_info(f"Opening Twitch homepage: {self.url}")
        
        # 等待載入完成
        self.wait_for_page_load(timeout=15)

        # 等待browse icon出現
        try:
            self.wait_for_visible(self.BROWSE_ICON, timeout=15)
            log_debug("Browse icon appeared")
        except:
            # 如果icon沒出現,嘗試等待第2定位器
            self.wait_for_visible(self.BROWSE_ICON_2, timeout=15)
            log_debug("Browse icon 2 appeared")
        
        # 額外等待確保畫面渲染完成
        # TODO: 可優化使用其他方式, js react檢查, 或者監控dom變化
        time.sleep(0.5)
        log_info("Homepage loaded completely")
        log_debug("All key elements have been rendered")
    
    def click_browse_icon(self):
        """點擊browse button"""
        log_info("Click browse icon")
        try:
            # 等待元素可見並可點擊
            self.wait_for_clickable(self.BROWSE_ICON, timeout=10)
            self.click(self.BROWSE_ICON, timeout=5)
        except Exception as e:
            log_debug(f"Main locator failed: {e}")
            log_info(f"Use the 2nd locator")
            self.wait_for_clickable(self.BROWSE_ICON_2, timeout=10)
            self.click(self.BROWSE_ICON_2, timeout=5)

        # 等待URL改變, 確認導向正確頁面
        self.wait_for_url_contains("/directory", timeout=10)
        
        self.wait_for_page_load(timeout=10)
        log_info("Already redirected to search page")
        # 額外等待確保畫面渲染完成
        # TODO: 可優化使用其他方式, js react檢查, 或者監控dom變化
        time.sleep(1)