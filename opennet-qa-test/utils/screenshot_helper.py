"""截圖工具"""
from pathlib import Path
from datetime import datetime
from utils.logger import log_info, log_debug


class ScreenshotHelper:
    
    def __init__(self, screenshot_dir: Path):
        self.screenshot_dir = screenshot_dir
        self.screenshots = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def take_screenshot(self, driver, step_name: str) -> str:
        filename = f"{self.timestamp}_{step_name}.png"
        filepath = self.screenshot_dir / filename
        
        # 截圖
        driver.save_screenshot(str(filepath))
        self.screenshots.append(str(filepath))
        
        log_info(f"Screenshot saved: {filename}")
        log_debug(f"Screenshot path: {filepath}")
        return str(filepath)
