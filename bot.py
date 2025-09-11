import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

def main():
    print("🚀 Starting Selenium test with your profile...")
    
    # Configure Chrome options for GitHub Actions
    chrome_options = Options()
    
    # === CRITICAL: Use the injected profile path ===
    chrome_options.add_argument('--user-data-dir=/home/runner/.config/google-chrome')
    chrome_options.add_argument('--profile-directory=Default')
    
    # Required for GitHub Actions/Linux environment
    chrome_options.add_argument('--headless=new')  # Use new headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Disable extensions and other settings for stability
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-dev-tools')
    chrome_options.add_argument('--remote-debugging-port=0')

    # Initialize the driver
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Chrome driver initialized successfully!")
    except WebDriverException as e:
        print(f"❌ Failed to initialize Chrome driver: {e}")
        return

    def check_running_cells():
        """Check if there are any running Colab cells"""
        running_indicators = [
            "//div[contains(@class, 'running')]",
            "//div[contains(@class, 'spinner')]",
            "//div[contains(@class, 'progress')]",
            "//div[contains(@class, 'executing')]",
            "//*[contains(text(), 'Executing')]",
            "//*[contains(text(), 'Running')]",
            "//circle[@id='filledCircle']",
            "//*[contains(@class, 'notebook-executing')]"
        ]
        
        for indicator in running_indicators:
            try:
                elements = driver.find_elements(By.XPATH, indicator)
                if elements:
                    print(f"   ⚡ Found {len(elements)} running cell indicators with: {indicator}")
                    return True
            except:
                continue
        return False

    def run_focused_cell():
        """Run the currently focused cell using Ctrl+Enter"""
        print("   ⌨️  Sending Ctrl+Enter to run focused cell...")
        
        try:
            # Get the currently focused element
            focused_element = driver.switch_to.active_element
            print(f"   🔍 Focused element: {focused_element.tag_name}")
            
            # Send Ctrl+Enter to the focused element
            focused_element.send_keys(Keys.CONTROL + Keys.ENTER)
            print("   ✅ Ctrl+Enter sent successfully!")
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to send Ctrl+Enter: {str(e)}")
            
            # Fallback: try sending to body as last resort
            try:
                print("   🔧 Trying fallback: sending Ctrl+Enter to body...")
                body = driver.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.CONTROL + Keys.ENTER)
                print("   ✅ Fallback Ctrl+Enter sent!")
                return True
            except Exception as fallback_error:
                print(f"   ❌ Fallback also failed: {str(fallback_error)}")
                return False

    def focus_first_cell():
        """Try to focus on the first code cell"""
        print("   🔍 Attempting to focus on first code cell...")
        
        cell_selectors = [
            "//div[contains(@class, 'code-cell')]",
            "//div[contains(@class, 'cell')]",
            "//div[contains(@class, 'input')]",
            "//div[@role='textbox']",
            "//div[contains(@class, 'monaco-editor')]"
        ]
        
        for selector in cell_selectors:
            try:
                cells = driver.find_elements(By.XPATH, selector)
                if cells:
                    print(f"   ✅ Found {len(cells)} potential code cells with: {selector}")
                    # Click on the first cell to focus it
                    cells[0].click()
                    print("   🎯 First code cell focused!")
                    return True
            except Exception as e:
                print(f"   ❌ Could not focus with {selector}: {str(e)}")
                continue
        
        print("   ⚠️  Could not find a code cell to focus")
        return False

    try:
        # Visit the specified Google Colab URL
        print("\n🌐 Visiting Google Colab URL...")
        colab_url = "https://colab.research.google.com/drive/1MElDzVC3JbJ8zLmf5AMQp54mi_u3Uu7r"
        driver.get(colab_url)
        
        # Wait for page to load
        print("⏳ Waiting for page to load...")
        time.sleep(15)

        # Check if there are any running Colab cells
        print("🔍 Checking for running Colab cells...")
        
        cell_running = check_running_cells()
        cell_started = False
        
        if cell_running:
            print("   ⏳ Cells are running - waiting for completion...")
            time.sleep(20)
            
            if check_running_cells():
                print("   ⚠️  Cells still running after wait, proceeding anyway...")
            else:
                print("   ✅ All cells completed execution")
        else:
            print("   ✅ No running cells detected - attempting to run first cell")
            
            if focus_first_cell():
                time.sleep(2)
            
            cell_started = run_focused_cell()
            
            if cell_started:
                print("   ⏳ Waiting for cell to start running...")
                time.sleep(5)
                
                if check_running_cells():
                    print("   ✅ Cell started running successfully!")
                    time.sleep(25)
                else:
                    print("   ⚠️  Cell may not have started running")

        # Scroll and take screenshot
        print("🖱️  Scrolling to capture notebook content...")
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(2)

        # Take screenshot
        screenshot_filename = 'colab_screenshot.png'
        driver.save_screenshot(screenshot_filename)
        print(f"   📸 Screenshot saved: {screenshot_filename}")

        # Display results
        print("\n" + "="*60)
        print("🎯 SCREENSHOT COMPLETE")
        print("="*60)
        print(f"📋 URL visited: {colab_url}")
        print(f"🔍 Running cells detected initially: {'Yes' if cell_running else 'No'}")
        print(f"🎬 Attempted to run cell: {'Yes' if not cell_running else 'No'}")
        print(f"🚀 Cell started successfully: {'Yes' if not cell_running and cell_started else 'No'}")
        print("="*60)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        # Always quit the driver in GitHub Actions
        driver.quit()
        print("\n✅ Browser closed. Test completed.")

if __name__ == "__main__":
    main()
