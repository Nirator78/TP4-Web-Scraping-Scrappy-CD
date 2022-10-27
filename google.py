from selenium import webdriver
from selenium.webdriver.common.by import By
from binascii import a2b_base64
import time

print("Launch Firefox")
driver = webdriver.Firefox()
BASE_URL = "https://www.google.com/search?q=subaru&source=lnms&tbm=isch"
driver.get(BASE_URL) 
time.sleep(1)

# Accept the cookies
print("Accepting cookies")
driver.find_element(By.XPATH, "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span").click()

time.sleep(2)
# Get div of image list
print("Get div of image list")
images = driver.find_elements(By.CSS_SELECTOR, "div.isv-r.PNCib.MSM1fd.BUooTd")
print("Nb images: ", len(images))

# Display list of image
for index, image in enumerate(images[:10]):
    image.click()
    data = image.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img").get_attribute("src")
    alt = image.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img").get_attribute("alt")
    print(alt)

    data = data.split(",")[1]

    binary_data = a2b_base64(data)
    with open('images/subaru-' + str(index) + '.png', 'wb') as fd:
        fd.write(binary_data)

driver.close()