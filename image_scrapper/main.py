import requests
import webbrowser
import urllib.request
import os
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def download_whole():
    print("Download entire search result or partial? (y/n) defualt: partial")
    thread = input()
    if (thread == 'y'):
        return True
    return False

def get_input():
    print("Enter a keyword")
    keyword = input()
    print("Enter a number of " + keyword + " images to get")
    img_count = input()
    valid_input = False
    while (valid_input == False):
        try:
            img_count = int(img_count)
            if (img_count > 1):
                valid_input = True
            else:
                print("Number must be greater than 1")
                img_count = input()
        except ValueError:
            print("That's not an integer!") 
            img_count = input()      
    
    return keyword, img_count

def url_builder(keyword):
    url = "https://www.google.com/search?q=" + keyword + "&rlz=1C1SQJL_enKR858KR858&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjvyIThp8_qAhUcwosBHb2ZDwAQ_AUoAXoECBgQAw&biw=1920&bih=937"
    return url

def get_image_urls(url):
    # driver = webdriver.Chrome("./chromedriver")
    driver = webdriver.Chrome("./image_scrapper/chromedriver.exe")
    driver.get(url)
    
    elem = driver.find_element_by_tag_name("body")

    for i in range(60):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
    
    button = driver.find_element_by_xpath('//input[@type="button"]')
    button.click()

    for i in range(60):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    print("Reached end of the search result")

    photo_grid_boxes = driver.find_elements_by_xpath('//div[@class="bRMDJf islir"]')

    image_urls = []

    for box in photo_grid_boxes:
        try:
            imgs = box.find_elements_by_tag_name("img")
            for img in imgs:
                src = img.get_attribute("src")
                # Google preloads 20 images as base64
                if str(src).startswith('data:'):
                    src = img.get_attribute("data-iurl")
                image_urls.append(src)

        except Exception:
            print("Error: System Crashed. Returning saved image urls.")
            return image_urls

    print("Found " + str(len(image_urls)) + " image urls")
    return image_urls

def make_dir(keyword):
    dir_path = "./image_folder/" + keyword
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

# download function without multithreading
def download_images(urls, dir_path, keyword, img_count):
    print("Downloading first " + str(img_count) + " images from " + str(len(urls)) + " urls found")
    
    success_count = 0
    fail_count = 0

    for i in range(len(urls)):
        if (success_count == img_count):
            break

        try:
            file_path = dir_path + "/" + keyword + str(success_count + 1) + ".jpg"
            # urllib.request.urlretrieve(urls[i], file_path)
            # second method
            response = urllib.request.urlopen(urls[i])
            image = response.read()
            with open(file_path, "wb") as file:
                file.write(image)
            
            success_count += 1
        except Exception:
            fail_count += 1
    print("Detected " + str(fail_count) + " invalid links")
    print("Downloaded " + str(success_count) + " images")

    if (success_count < img_count):
        print("Try searching with synonyms to download more images")

# download function with multithreading
def download_images_multithread(url, i, dir_path, keyword):
    try:
        file_path = dir_path + "/" + keyword + str(i) + ".jpg"
        response = urllib.request.urlopen(url)
        image = response.read()
        with open(file_path, "wb") as file:
            file.write(image)
        # urllib.request.urlretrieve(url, file_path)
    except Exception:
        return

def set_multithread(urls, dir_path, keyword):
    threads = list()
    
    for i in range(len(urls)):
        processThread = threading.Thread(target=download_images_multithread, args=(urls[i], i, dir_path, keyword))
        threads.append(processThread)
        processThread.start()
    
    for thread in threads:
        thread.join()
    
    print("Detected " + str(len(urls) - len(os.listdir(dir_path))) + " invalid urls")
    print("Downloaded " + str(len(os.listdir(dir_path))) + " images")
    print("Try searching with synonyms to download more images")

def rename_files(keyword, path):
    for count, filename in enumerate(os.listdir(path)):
        dst = keyword + str(count + 1) + ".jpg"
        src = path+ "/" + filename 
        dst = path+ "/" + dst 
        os.rename(src, dst) 


thread = download_whole()
if (thread == True):
    print("Enter a keyword")
    keyword = input()
else:
    keyword, img_count = get_input()

start_time = time.time()

url = url_builder(keyword)
image_urls = get_image_urls(url)
path = make_dir(keyword)

if (thread == True):
    set_multithread(image_urls, path, keyword)
    rename_files(keyword, path)
else:
    download_images(image_urls, path, keyword, img_count)

print("---Took %s seconds ---" % (time.time() - start_time))
