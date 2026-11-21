from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
from utils.logger import *
import random
import time
import traceback


class TwitchSearchChannelsTabPage(BasePage):
    
    # 元素定位
    # Channel
    CHANNEL_BUTTONS = (By.CSS_SELECTOR, "button.ScCoreLink-sc-16kq0mq-0, button.tw-link")  # 頻道按鈕
    CHANNEL_TITLES = (By.CSS_SELECTOR, "h2[title]")  # 頻道名稱標題
    ALL_BUTTONS = (By.TAG_NAME, "button")  # 備用：所有按鈕
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def scroll_down_page(self, times=2):
        """向下滑動頁面"""
        log_info(f"Try to scroll down {times} times")

        for i in range(times):
            try:
                log_info(f"Scroll down {i+1} times")
                
                # 向下滑動
                # HACK: 當滑動比例較大時, 會導致畫面來不及render, 而出現問題
                window_viewport_ratio = 0.5
                # TODO: 可優化等待策略, js react檢查, 或監控dom變化, 以確保在滑動幅度較大時, 畫面能正確render
                self.scroll_by(viewport_ratio=window_viewport_ratio)
                time.sleep(1)  # 等待畫面渲染
                log_debug(f"Scroll down {window_viewport_ratio * 100}% of window height")
                    
            except Exception as e:
                log_error(f"Failed on scroll {i+1} times: {e}")
    
    def get_channel_elements(self):
        """獲取頻道元素列表"""
        try:
            # 使用 CHANNEL_BUTTONS 定位
            elements = self.find_elements(self.CHANNEL_BUTTONS, timeout=3)
            log_debug(f"CHANNEL_BUTTONS found {len(elements)} elements")
            
            if not elements:
                log_debug("CHANNEL_BUTTONS locator not found, trying ALL_BUTTONS")
                elements = self.find_elements(self.ALL_BUTTONS, timeout=3)
                log_debug(f"ALL_BUTTONS found {len(elements)} elements")
            
            # 過濾有效的頻道按鈕
            valid_elements = []
            for elem in elements:
                try:
                    h2_elements = elem.find_elements(By.TAG_NAME, "h2")
                    if not h2_elements:
                        continue
                    # 從h2標題獲取頻道名稱
                    channel_name = h2_elements[0].get_attribute('title')
                    
                    if not channel_name:
                        continue

                    # 檢查元素是否可見
                    if elem.is_displayed():
                        valid_elements.append(elem) # 假如有直接append進list
                        log_debug(f"Found valid channel: {channel_name}")
                except:
                    continue

            log_debug(f"Found {len(valid_elements)} valid channel elements")
            return valid_elements
        except Exception as e:
            log_error(f"Error occurred while getting channel elements: {e}")
            return []   # 都未找到的狀況下回傳空list
    
    def select_random_channel(self):
        """隨機選擇一個頻道並點擊"""
        channels = self.get_channel_elements()
        
        if not channels:
            log_warning("Did not find any channels")
            return False

        log_info(f"Found {len(channels)} channels")
        # FIXME: 使用random選元素, 會導致多滑動一次
        selected_channel = random.choice(channels)
        
        try:
            # 獲取頻道名稱（從 h2 標題）
            h2_elements = selected_channel.find_elements(By.TAG_NAME, "h2")
            channel_name = h2_elements[0].get_attribute('title') if h2_elements else "Unknown"
            log_info(f"Random select a channel: {channel_name}")
            
            # 滾動到元素
            self.scroll_to_element(selected_channel)
            log_debug("Already scrolled to the selected channel element")

            # NOTE: 滾動後重新查找元素,避免 stale element 錯誤
            # 使用頻道名稱重新定位
            try:
                # 等待 DOM 穩定
                time.sleep(0.3)
                
                # 重新獲取所有頻道元素
                channels = self.get_channel_elements()
                
                # 從新元素中找到同名的頻道
                selected_channel = None
                for channel in channels:
                    try:
                        h2 = channel.find_elements(By.TAG_NAME, "h2")
                        if h2 and h2[0].get_attribute('title') == channel_name:
                            selected_channel = channel
                            log_debug(f"Re-found channel element: {channel_name}")
                            break
                    except:
                        continue
                
                if not selected_channel:
                    log_error(f"Can not find channel {channel_name} after scroll")
                    return False
                    
            except Exception as e:
                log_warning(f"Failed to find channel element: {e}, trying to click directly")
            
            self.wait_for_clickable((By.TAG_NAME, "button"), timeout=5)
            
            selected_channel.click()
            log_debug(f"Already clicked channel button: {channel_name}")
            
            self.wait_for_url_contains(channel_name.lower(), timeout=10)
            
            # 等待新頁面完全載入
            self.wait_for_page_load(timeout=10)
            log_info(f"Already in channel page: {channel_name}")            
            return True
        
        except Exception as e:
            log_error(f"Error occurred on select_random_channel: {e}")
            log_error(f"Detail error message: {traceback.format_exc()}")
            return False
    
