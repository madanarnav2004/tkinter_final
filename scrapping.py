import asyncio
import json
import time
import tkinter as tk
from threading import Thread
from tkinter import ttk

import requests
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# Create a function that will be called when the submit button is clicked

headers = {
    'User-Agent': 'TikTok 26.2.0 rv:262018 (iPhone; iOS 14.4.2; en_US) Cronet'
}
headers_wm = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

root = tk.Tk()
# Create the main window
root.geometry("1000x600")
root.title("Tiktok Downloader")

def download_async(vid_id):
    download = Thread(target=download_video, args=[vid_id])
    download.start()

def download_video(vid_id):
    url = 'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id='+vid_id

    # print(f'Downloading {count} of {total}')
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)

    new_url = json_data['aweme_list'][0]['video']['play_addr']['url_list'][0]

    file_name = f'{vid_id}.mp4'
    download_file = requests.get(new_url, headers=headers).content

    chunk_size = 1024

    print('saving file',vid_id)

    with open(file_name, 'wb') as file:
        for i in range(0, len(download_file), chunk_size):
            chunk = download_file[i:i+chunk_size]
            file.write(chunk)


def submit():
    # Get the text from the input box
    text = input_box.get()
    data = text.split(',')
    # Split the text into a list of strings

    username = text

    print('--->Setup selenium start : ')
    chrome_options = Options()
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-web-security')
    # chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--remote-debugging-port=9515")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_experimental_option("detach", True)
    prefs = {'download.default_directory' : '/home/harsh/Desktop/PHP/files/'}
    chrome_options.add_experimental_option('prefs', prefs)
    # chrome_options.add_argument('--disable-gpu')
    # service = Service(executable_path=chromedriver_path)

    capabilities = {
        "resolution": "max",
    }
    driver = webdriver.Chrome(options=chrome_options,
                                desired_capabilities=capabilities)

    driver.maximize_window()
    print('Setup selenium complete')
    print(
        "Current window size: ",
        driver.execute_script(
            "return [window.outerWidth, window.outerHeight];"))

    print(
        "Screen resolution: ",
        driver.execute_script(
            "return [window.screen.width, window.screen.height];"))

    driver.get(f"https://www.tiktok.com/@{username}/")
    time.sleep(5)


    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        try:
            captcha = driver.find_element(By.XPATH, ".//*[@class='verify-bar-close--icon']")
            captcha.click()
            print('closed captcha')
            time.sleep(1)
        except:
            pass

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(2)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        try:
            captcha = driver.find_element(By.XPATH, ".//*[@class='verify-bar-close--icon']")
            captcha.click()
            print('closed captcha')
            time.sleep(1)
        except:
            if new_height == last_height:
                break


    video_elements = driver.find_elements(By.TAG_NAME, 'a')

    video_links = []
    for video_element in video_elements:
        if video_element == None:
            continue
        try:
            if video_element.get_attribute("href").startswith(f"https://www.tiktok.com/@{username}/"):
                image = video_element.find_element(By.TAG_NAME, "img")
                print(image.get_attribute("src"))
                video_link = video_element.get_attribute("href")
                video_links.append(video_link)
        except Exception as e:
            print(e)
            continue

    print(len(video_links))
    for video_link in video_links:
        print(video_link)
    driver.quit()

    # video_links = ["https://www.tiktok.com/@selenagomez/video/6782218030668696837",
    #             "https://www.tiktok.com/@selenagomez/video/6781985952681233670",
    #             "https://www.tiktok.com/@selenagomez/video/6781886561756777734",
    #             "https://www.tiktok.com/@selenagomez/video/6781863942751816966",
    #             "https://www.tiktok.com/@selenagomez/video/6755264115582733573",
    #             "https://www.tiktok.com/@selenagomez/video/6752006132207865093",
    #             "https://www.tiktok.com/@selenagomez/video/6751923560693959941",
    #             "https://www.tiktok.com/@selenagomez/video/99443724056674304"]
    
    # Create a table with 6 columns (5 for the data and 1 for the button)
    for i,video_link in enumerate(video_links):
        # create button in second column
        video_id = video_link.split('/video/')[1]
        btn = tk.Button(root, text='Download', command=lambda video_id=video_id: download_async(video_id))
        btn.grid(row=i+3, column=2)
        # create label in first column
        label = tk.Label(root, text=video_link)
        label.grid(row=i+3, column=1)
        label2 = tk.Label(root, text=username)
        label2.grid(row=i+3, column=0)

# Set the style of the GUI
style = ttk.Style()
style.theme_use('clam')

# # Set the custom style for the Treeview widget
style.configure('Custom.Treeview', background='#f7f7f7', foreground='black', rowheight=25, fieldbackground='#f7f7f7', font=('Helvetica', 10))

# Create a label for the input box
input_label = tk.Label(root, text='Enter username:', font='Helvetica 12')
input_label.grid(row=0, column=0, padx=5, pady=5)

# Create the input box and submit button
input_box = tk.Entry(root, width=50, font='Helvetica 12')
input_box.grid(row=0, column=1, padx=5, pady=5)

submit_button = tk.Button(root, text='Submit', font='Helvetica 12', command=submit)
submit_button.grid(row=0, column=2, padx=5, pady=5)

# Start the main event loop
root.mainloop()

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def run_program(request):
    # Get input parameters from request
    param1 = request.POST.get('param1')
    param2 = request.POST.get('param2')
    
    # Call your program with input parameters
    result = submit(param1, param2)
    
    # Return result as JSON response
    return JsonResponse({'result': result})
