import pytest
import pytest_html
from datetime import datetime
from pathlib import Path
from utils.driver_factory import DriverFactory
from utils.screenshot_helper import ScreenshotHelper
from utils.logger import *
from config.config import SCREENSHOT_DIR, BASE_DIR


def pytest_configure(config):
    """
    html report 設定
    """
    # 生成帶時間戳的 HTML report 檔名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = BASE_DIR / "reports"
    report_dir.mkdir(exist_ok=True)
    
    # 設定 HTML report 路徑
    html_report_path = report_dir / f"report_{timestamp}.html"
    config.option.htmlpath = str(html_report_path)
    
    log_debug(f"HTML Report will be saved to: {html_report_path}")


@pytest.fixture(scope="function")
def driver():
    """WebDriver Fixture"""
    log_info("Initializing WebDriver...")
    driver = DriverFactory.get_driver()
    log_debug(f"WebDriver initialized: {type(driver).__name__}")

    yield driver

    log_info("Closing WebDriver...")
    driver.quit()


@pytest.fixture(scope="function")
def screenshot_helper(request):

    helper = ScreenshotHelper(SCREENSHOT_DIR)
    log_debug(f"ScreenshotHelper initialized")

    yield helper
    
    # 測試結束後將截圖附加到 HTML report (使用 pytest-html hook)
    if helper.screenshots:
        log_debug(f"Preparing to attach {len(helper.screenshots)} screenshots to HTML report")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    pytest-html hook: 在測試報告的 Links 欄位添加截圖
    """
    outcome = yield
    report = outcome.get_result()
    
    # 只在測試執行階段（call）處理
    if report.when == 'call':
        # 獲取 screenshot_helper fixture
        if 'screenshot_helper' in item.funcargs:
            helper = item.funcargs['screenshot_helper']
            
            if helper.screenshots:
                log_debug(f"在 pytest_runtest_makereport 中處理 {len(helper.screenshots)} 張截圖")
                
                # 初始化 extra 列表（不覆蓋現有的 log）
                extra = getattr(report, 'extra', [])
                
                for idx, screenshot_path in enumerate(helper.screenshots, 1):
                    screenshot_file = Path(screenshot_path)
                    if screenshot_file.exists():
                        log_debug(f"Processing screenshot file: {screenshot_path}")
                        
                        # 計算相對路徑（相對於 reports 目錄）
                        from os.path import relpath
                        report_dir = Path(SCREENSHOT_DIR).parent / "reports"
                        rel_path = relpath(screenshot_path, report_dir)
                        
                        # 獲取截圖檔名（用於顯示）
                        screenshot_name = screenshot_file.name
                        
                        # 添加到 Links 欄位（使用 url extra）
                        extra.append(pytest_html.extras.url(
                            rel_path,
                            name=f'{screenshot_name}'
                        ))
                        
                        log_debug(f"Screenshot added to Links: {screenshot_name}")
                    else:
                        log_debug(f"Screenshot file does not exist: {screenshot_path}")
                
                report.extra = extra


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """測試環境設置(scope=session)"""
    log_info("Setting up test environment...")
    log_info("Log file: " + logger.get_log_file())

    yield

    log_info("Test execution completed")
    log_info("Test log has been saved to: " + logger.get_log_file())
