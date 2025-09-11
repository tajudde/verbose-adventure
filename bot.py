import time
time.sleep(2)

# === STEP 4: Selenium Test with Your Profile ===
print("\n🚀 Starting Selenium test with your profile...")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#from IPython.display import Image, display

# Configure Chrome options for Colab
options = webdriver.ChromeOptions()
chrome_options.add_argument("--user-data-dir=/home/runner/.config/google-chrome")
chrome_options.add_argument("--profile-directory=Default")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# Initialize the driver
driver = webdriver.Chrome(options=options)

def check_running_cells():
    """Check if there are any running Colab cells"""
    running_indicators = [
        "//div[contains(@class, 'running')]",
        "//div[contains(@class, 'spinner')]",
        "//div[contains(@class, 'progress')]",
        "//div[contains(@class, 'executing')]",
        "//*[contains(text(), 'Executing')]",
        "//*[contains(text(), 'Running')]"
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

def run_first_cell():
    """Run the first available Colab cell"""
    print("   ▶️  Attempting to run first cell...")
    
    # Try different selectors for Colab run buttons
    run_button_selectors = [
        "//button[contains(@class, 'run-button')]",
        "//button[contains(@aria-label, 'Run')]",
        "//div[contains(@class, 'run-cell')]",
        "//span[contains(text(), 'Run')]/ancestor::button",
        "//button[.//span[contains(text(), 'Run')]]"
    ]
    
    for selector in run_button_selectors:
        try:
            run_buttons = driver.find_elements(By.XPATH, selector)
            if run_buttons:
                print(f"   ✅ Found {len(run_buttons)} run buttons with selector: {selector}")
                # Click the first run button
                run_buttons[0].click()
                print("   🎯 Successfully clicked run button!")
                return True
        except Exception as e:
            print(f"   ❌ Failed to click with selector {selector}: {str(e)}")
            continue
    
    print("   ❌ Could not find a run button")
    return False

try:
    print("✅ Chrome driver initialized successfully!")

    # Visit the specified Google Colab URL
    print("\n🌐 Visiting Google Colab URL...")
    colab_url = "https://colab.research.google.com/drive/1MElDzVC3JbJ8zLmf5AMQp54mi_u3Uu7r"
    driver.get(colab_url)
    
    # Wait for page to load
    print("⏳ Waiting for page to load...")
    time.sleep(10)

    # Check if there are any running Colab cells
    print("🔍 Checking for running Colab cells...")
    
    cell_running = check_running_cells()
    
    if cell_running:
        print("   ⏳ Cells are running - waiting for completion...")
        # Wait additional time for cells to complete
        time.sleep(15)
        
        # Check again if cells are still running
        if check_running_cells():
            print("   ⚠️  Cells still running after wait, proceeding anyway...")
        else:
            print("   ✅ All cells completed execution")
    else:
        print("   ✅ No running cells detected - attempting to run first cell")
        # Try to run the first cell
        if run_first_cell():
            print("   ⏳ Waiting for cell to start running...")
            time.sleep(5)
            
            # Check if cell started running
            if check_running_cells():
                print("   ✅ Cell started running successfully!")
                print("   ⏳ Waiting for cell execution to complete...")
                time.sleep(15)
            else:
                print("   ⚠️  Cell may not have started running")
        else:
            print("   ⚠️  Could not run cell, proceeding with screenshot")

    # Scroll to capture more content
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
    print("⏱️  Total execution time: ~40 seconds")
    print("="*60)

    # Display screenshot
    #print("\n🖼️ Google Colab Screenshot:")
    #try:
        #display(Image(filename=screenshot_filename, width=800))
   # except FileNotFoundError:
        #print("   ❌ Screenshot not found")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

finally:
    print("\n🔍 Test completed. Browser remains open for inspection.")
    print("💡 Run 'driver.quit()' when finished.")
