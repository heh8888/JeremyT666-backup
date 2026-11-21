from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """定義所有動作的class"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator, timeout=10):
        """查找單一元素"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            raise NoSuchElementException(f"can't find element: {locator}, timeout={timeout}")
    
    def find_elements(self, locator, timeout=10):
        """查找多個元素"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            # 只要找到一個元素就return
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            return []   # 找不到時返回空list, 先不raise exception
    
    def click(self, locator, timeout=10):
        """點擊行為"""
        element = self.wait_for_clickable(locator, timeout)
        element.click()
    
    def input_text(self, locator, text, timeout=10):
        """輸入字串"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    def wait_for_clickable(self, locator, timeout=10):
        """等待元素可點擊"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_visible(self, locator, timeout=10):
        """等待元素可見"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def scroll_by(self, viewport_ratio=0.8):
        """向下滑動固定距離"""
        # 嘗試使用Selenium的ActionChains, 無法處理, 改用JS的方式處理
        # viewport_ratio: 視窗高度的比例, Ex: 0.8表示滑動視窗高度的80%
        self.driver.execute_script(
            f"window.scrollBy({{top: window.innerHeight * {viewport_ratio}, behavior: 'smooth'}});"
        )
        self.wait_for_scroll_stop()
    
    def scroll_to_element(self, element):
        """滑動到指定元素"""
        # 嘗試使用Selenium的ActionChains, 無法處理, 改用JS的方式處理
        # arguments[0] -> JS中接收Py傳入的第一個參數
        # scrollIntoView(...) -> JS內建方法, 將元素滑到可見範圍
        # behavior: 'smooth' scrollIntoView的對應參數, 平滑滑動
        # block: 'center' scrollIntoView的對應參數, 將元素滑到對其視窗中央
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
            element
        )
        self.wait_for_scroll_stop()
    
    def get_current_url(self):
        """取當前 URL"""
        return self.driver.current_url
    
    def wait_for_page_load(self, timeout=10):
        """等待頁面完全載入"""
        wait = WebDriverWait(self.driver, timeout)
        # Selenium官方建議方式, 會執行JS程式碼, 確保頁面完全載入
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    def wait_for_url_contains(self, text, timeout=10):
        """等待 URL 包含特定文字"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.url_contains(text))
        except TimeoutException:
            return False
    
    def wait_for_scroll_stop(self, timeout=5):
        """等待頁面停止捲動"""
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(lambda driver: driver.execute_script("""
                return new Promise(resolve => {                 // 建立非同步 Promise物件, Selenium會等待這個Promise完成
                    let lastPos = window.pageYOffset;           // 取得最後位置(Y軸)
                    const check = () => {                       // 定義檢查函式
                        const currentPos = window.pageYOffset;  // 取得目前位置(Y軸)
                        if (currentPos === lastPos) {           // 比對最後位置跟目前位置
                            resolve(true);                      // 停止捲動了, 回傳 true
                        } else {
                            lastPos = currentPos;               // 還在動,更新最後位置
                            setTimeout(check, 100);             // 100ms 後再檢查一次
                        }
                    };
                    setTimeout(check, 100);                     // 初次執行:等待 100ms 後開始檢查
                });
            """))
        except:
            pass

    def wait_for_react_fiber_ready(self, timeout=10):
        """等待 React Fiber 完成渲染 (改進版)"""
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(lambda driver: driver.execute_script("""
                // 檢查 React 根節點
                const rootElement = document.getElementById('root');
                if (!rootElement) return false;
                
                // 檢查是否有 React Fiber (兼容多個版本)
                const keys = Object.keys(rootElement);
                const hasFiber = keys.some(key => 
                    key === '_reactRootContainer' ||           // React 16-17
                    key.startsWith('__reactContainer') ||      // React 18+
                    key.startsWith('__reactInternalInstance')  // 舊版 React
                );
                
                // 檢查 React DevTools Hook (更可靠的方式)
                const hasReactDevTools = window.__REACT_DEVTOOLS_GLOBAL_HOOK__ !== undefined;
                
                // 確保 document 已載入完成
                return hasFiber && document.readyState === 'complete';
            """))
            # log_debug("React Fiber 已就緒")
            return True
        except:
            # log_debug("React Fiber 等待超時")
            return False
