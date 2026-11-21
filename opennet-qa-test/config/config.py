from pathlib import Path


BASE_DIR = Path(__file__).parent.parent

# URL
TWITCH_URL = "https://www.twitch.tv"

# browser settings
BROWSER = "chrome"
HEADLESS = False
IMPLICIT_WAIT = 1
PAGE_LOAD_TIMEOUT = 30

# 模擬手機設定
MOBILE_EMULATION = {
    "deviceName": "iPhone 14 Pro Max",
}

# screenshot settings
SCREENSHOT_DIR = BASE_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True) # 如果不存在就建立screenshots目錄

# 測試參數設定
SEARCH_KEYWORD = "StarCraft II"
SCROLL_COUNT = 2
# SCROLL_PAUSE_TIME = 1  # 每次捲動後的暫停時間
