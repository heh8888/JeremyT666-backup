from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import *
import time

class TwitchStreamerPage(BasePage):

    
    # 元素定位
    VIDEO_PLAYER = (By.CSS_SELECTOR, "video, div[data-a-target='player-overlay-click-handler']")
    # 實況主名稱
    CHANNEL_HEADER = (By.CSS_SELECTOR, "div[data-a-target='channel-header-right']")
    CHAT_CONTAINER = (By.CSS_SELECTOR, "div[class*='chat'], div[data-a-target='chat-welcome-message']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def wait_for_streamer_page_load(self, timeout=15):
        
        # 1. 等待基本頁面載入完成
        self.wait_for_page_load(timeout)
        # log_debug("Streamer page load complete")
        
        # 2. 等待視頻播放器出現
        try:
            self.wait_for_visible(self.VIDEO_PLAYER, timeout=10)
            log_info("Video player is visible")
            time.sleep(5)  # 額外等待確保播放器穩定
        except:
            log_warning("Could not find video player, continuing...")
        
        get_streamer_info = self.get_streamer_info()
        log_info(f"Streamer info: Name='{get_streamer_info['name']}', URL='{get_streamer_info['url']}'")

        log_info("Streamer page fully loaded")
    
    def get_streamer_info(self):
        """獲取實況主資訊"""
        current_url = self.get_current_url()
        info = {
            "url": current_url,
            "name": None
        }
        
        # 從 URL 中取頻道名稱
        try:
            from urllib.parse import urlparse
            parsed = urlparse(current_url)
            path_parts = parsed.path.strip('/').split('/')
            if path_parts and path_parts[0]:
                info["name"] = path_parts[0]
                log_debug(f"Get streamer name: {info['name']}")
                return info
        except Exception as e:
            log_debug(f"Could not get channel name from URL: {e}")

        return info
