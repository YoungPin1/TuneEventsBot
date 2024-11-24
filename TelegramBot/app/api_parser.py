from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.get("https://music.yandex.ru/users/robertchechenov/playlists/3")
XPath_Artist_Name = "/html/body/div[1]/div[16]/div[2]/div/div/div[4]/div/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/span/a"
artists_info = browser.find_elements(by=By.XPATH, value=XPath_Artist_Name)
Artists_ClassName = artists_info[0].get_attribute('class')
artists = browser.find_elements(by=By.CSS_SELECTOR, value=f"a[class='{Artists_ClassName}']")
for artist in artists:
    print(artist.text)

result = []
for artist in artists:
    if artist not in result:
        result.append(artist)
print('----------')
for artist in result:
    print(artist.text)