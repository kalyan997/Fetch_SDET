from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys

# Set up the Chrome WebDriver
driver = webdriver.Chrome()  # Make sure you have the chromedriver installed and in your PATH

# Open the website
driver.get("http://sdetchallenge.fetch.com/")  # Replace with the correct URL
num_weighs = 0

def weigh(left_bars, right_bars):
    # Reset the scale for a new measurement
    global num_weighs
    

    for i in range(9):
        left_input = driver.find_element(By.CSS_SELECTOR, f"input[id='left_{i}']")
        right_input = driver.find_element(By.CSS_SELECTOR, f"input[id='right_{i}']")
        
        for _ in range(10):  
            left_input.send_keys(Keys.BACK_SPACE)
            right_input.send_keys(Keys.BACK_SPACE)

    #driver.find_element(By.ID, "reset").click()
    #wait = WebDriverWait(driver, 10)
    #button = driver.find_element(By.ID, "reset")
    #driver.execute_script("arguments[0].click();", button)
    #time.sleep(15)

    print(left_bars, right_bars)
    for i, bar in enumerate(left_bars):
        #print(i, bar)
        driver.find_element(By.CSS_SELECTOR, f"input[id='left_{i}']").send_keys(str(bar))

    # Place bars on the right bowl
    for i, bar in enumerate(right_bars):
        #print(i, bar)
        driver.find_element(By.CSS_SELECTOR, f"input[id='right_{i}']").send_keys(str(bar))

    # Perform the weighing
    time.sleep(15)
    driver.find_element(By.ID, "weigh").click()
    num_weighs += 1
    time.sleep(15)  # Wait for the weighing to complete

    result = driver.find_element(By.CSS_SELECTOR, "div[class='result']").text
    result = result[-1]
    curr_weighing = "  "+ ",".join(str(c) for c in left_bars) + " " +result + "  "+ ",".join(str(c) for c in right_bars) + "  "
    weighings.append(curr_weighing) 
    return result

def find_fake_bar():
    bars = list(range(9))  # Bar identifiers [0-8]
    # Divide bars into three groups
    group1, group2, group3 = bars[:3], bars[3:6], bars[6:]

    # First weighing: Compare group1 and group2
    result = weigh(group1, group2)
    #print(result)
    if result == "=":
        suspected_group = group3
    elif result == ">":
        suspected_group = group2
    else:
        suspected_group = group1  # If equal, fake bar is in group3

    print("fake bar is in group: ", suspected_group)
    # Second weighing: Take two bars from the suspected group and compare
    result = weigh(suspected_group[:1], suspected_group[1:2])
    #print(result)
    if result == "=":
        fake_bar = suspected_group[2]
    elif result == ">":
        fake_bar = suspected_group[1]
    else:
        fake_bar = suspected_group[0]
    

    return fake_bar

def get_alert_message():
    try:
        alert = Alert(driver)
        alert_text = alert.text
        alert.accept()  # Close the alert
        return alert_text
    except NoSuchElementException:
        return "No alert present."

# Start the process of finding the fake bar
weighings = []  # Initialize list to store the results of weighings

try:
    fake_bar = find_fake_bar()
    driver.find_element(By.CSS_SELECTOR, f"button[id='coin_{fake_bar}']").click()

    alert_message = get_alert_message()  # Capture the alert message

    # Output the results
    print(f"The fake gold bar is bar number {fake_bar}.")
    print(f"Alert message: {alert_message}")
    print(f"Number of weighings made: {num_weighs}")
    print(f"List of weighings made: {weighings}")

finally:
    # Keep the browser open for a short time and then close it
    time.sleep(5)
    driver.quit()
