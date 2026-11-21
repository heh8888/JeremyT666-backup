import pytest
from pages.twitch_home_page import TwitchHomePage
from pages.twitch_search_page import TwitchSearchPage
from pages.twitch_search_channels_tab_page import TwitchSearchChannelsTabPage
from pages.twitch_streamer_page import TwitchStreamerPage
from config.config import SEARCH_KEYWORD, SCROLL_COUNT
from utils.logger import *


@pytest.mark.smoke
class TestTwitchSearch:
    
    def test_search_and_select_streamer(self, driver, screenshot_helper):
        """
        測試搜尋關鍵字並隨機選擇實況主
        
        測試流程:
        1. 進入 Twitch 首頁
        2. 點擊搜尋圖示
        3. 輸入關鍵字 "StarCraft II"
        4. 點擊 Channels 頁籤
        5. 向下捲動兩次
        6. 隨機選擇一位實況主
        7. 進入實況主頁面並截圖
        """
        try:
            # Initialize page objects
            home_page = TwitchHomePage(driver)
            search_page = TwitchSearchPage(driver)
            channels_page = TwitchSearchChannelsTabPage(driver)
            streamer_page = TwitchStreamerPage(driver)
            
            # Step 1. 進入 Twitch 首頁
            home_page.open()

            # Step 2. 點擊搜尋圖示
            home_page.click_browse_icon()

            # Step 3. 輸入搜尋關鍵字
            search_page.enter_search_keyword(SEARCH_KEYWORD)

            # Step 4. 點擊 Channels 頁籤
            search_page.click_channels_tab()
            
            # Step 5. 向下捲動頁面
            channels_page.scroll_down_page(times=SCROLL_COUNT)
            
            # Step 6. 隨機選擇一個頻道
            success = channels_page.select_random_channel()
            assert success, "Failed to select a channel"

            # Step 7. 等待實況主頁面載入
            streamer_page.wait_for_streamer_page_load()
            streamer_info = streamer_page.get_streamer_info()
            log_info(f"streamer_info: {streamer_info}")
            
            # Result Verification
            assert streamer_info, "Failed to navigate to streamer page"
            log_info("Test completed successfully!")
            
            # 最終截圖（成功）
            screenshot_helper.take_screenshot(driver, "final_success")
            
        except Exception as e:
            # 測試失敗時也截圖
            log_error(f"Test failed: {e}")
            screenshot_helper.take_screenshot(driver, "final_failure")
            raise

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
