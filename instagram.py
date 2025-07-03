from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import re
import time
import pandas as pd
from excel_merger import ExcelMerger
from date_formatter import DateFormatter

def initialize_driver():
    options = Options()
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.content_settings.exceptions.automatic_downloads": {"*": {"setting": 2}},
        "media.autoplay.default": 1
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--log-level=3")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-cookies")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def scroll_down(comments_section, driver):
    last_height = comments_section.get_property('scrollHeight')
    while True:
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", comments_section)
        time.sleep(1)
        new_height = comments_section.get_property('scrollHeight')
        if new_height == last_height:
            time.sleep(3)
            new_height = comments_section.get_property('scrollHeight')
            if new_height == last_height:
                try:    
                    hidden_comments = driver.find_element(By.XPATH, "//span[contains(@class, 'x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1fhwpqd xk50ysn x1roi4f4 x1s3etm8 x676frb x10wh9bi x1wdrske x8viiok x18hxmgj')]")
                    hidden_comments.click()
                    last_height = new_height
                    continue
                except:
                    break
        last_height = new_height
    time.sleep(1)

def load_more_replies(driver, wait):
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@style, 'line-height: var(--base-line-clamp-line-height); --base-line-clamp-line-height: 18px;')]")))
    more_replies = driver.find_elements(By.XPATH, "//*[contains(text(), 'View') and contains(text(), 'replies')]")
    for reply in more_replies:
        while True:
            try:
                reply.click()
            except:
                more_replies = driver.find_elements(By.XPATH, "//*[contains(text(), 'Show') and contains(text(), 'replies')]")
                continue
            finally:
                time.sleep(3)
                break

def login_to_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(2)
    driver.maximize_window()
    username_field = driver.find_element("name", 'username')
    password_field = driver.find_element("name", 'password')
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

def read_excel_columns(excel_file):
    df = pd.read_excel(excel_file)
    post_links = df['Link'].tolist()
    return post_links

def get_post_info(driver, wait):
    try:
        post_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj']")))
        post_text = '\n'.join([elem.text.strip() for elem in post_elements])
    except:
        post_text = "no post text"
        
    get_post_owner_link = driver.find_element(By.XPATH, "//a[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz notranslate _a6hd']")
    post_owner_link = get_post_owner_link.get_attribute("href")
    
    post_username = driver.find_element(By.XPATH, "//span[@class='_ap3a _aaco _aacw _aacx _aad7 _aade']").text
    
    date_element = driver.find_elements(By.XPATH, "//span[@class='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1fhwpqd xo1l8bm x1roi4f4 x1s3etm8 x676frb x10wh9bi x1wdrske x8viiok x18hxmgj']")
    post_date = date_element[0].find_element(By.XPATH, ".//time").get_attribute('datetime')
    
    try:
        get_post_like = driver.find_element(By.XPATH, "//span[@class='html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs']")
        post_like = get_post_like.get_attribute("innerText")
    except:
        post_like = "0"
        
    post_url =  driver.current_url
    match = re.search(r"instagram\.com/(?:p|reel)/([A-Za-z0-9_\-]+)/", post_url)
    post_id = match.group(1) if match else "no post link"

    parent_id = "null"
    
    return [post_text, post_url, post_username, post_date, post_like, post_owner_link, post_id, parent_id]

def get_comment_info(block):
    comments = block.find_elements(By.XPATH, ".//span[@class='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj']")
    if len(comments) >= 2:
        try:
            comment_text = comments[-1].text
        except:
            comment_text = "no comment text"
    else:
        comment_text = "no comment text"
    
    try:
        username = block.find_element(By.XPATH, ".//span[contains(@class, '_ap3a _aaco _aacw _aacx _aad7 _aade')]").text
    except:
        try:
            username = block.find_element(By.XPATH, ".//span[contains(@class, '_ap3a _aaco _aacw _aacz _aad7 _aade')]").text
        except:
            username = "no username text"

    try:
        get_date = block.find_element(By.XPATH, ".//time")
        comment_date = (get_date.get_attribute('datetime'))
    except:
        comment_date = "no date text"

    get_like_counts = block.find_elements(By.XPATH, ".//span[contains(@class, 'x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft')]")
    for get_like_count in get_like_counts:
        like_count = get_like_count.text
        if re.search(r'\d+', like_count):
            match = re.search(r'(\d+)', like_count)
            comment_like = match.group(1)
            break
        else:
            comment_like = "0"
    
    get_profile_link = block.find_element(By.XPATH, ".//a[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz notranslate _a6hd']")
    profile_link = get_profile_link.get_attribute("href")
    try:
        get_comment_link = block.find_element(By.XPATH, ".//a[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd']")
        comment_url = get_comment_link.get_attribute("href")
        comment_id = get_comment_link.get_attribute("href")
        match = re.search(r'/c/(\d+)/', comment_id)
        comment_id = match.group(1) if match else "no id info"
    except:
        comment_url = "no id info"
        comment_id = "no id info"
        
    parent_id = "null"
    
    return [comment_text, comment_url, username, comment_date, comment_like, profile_link, comment_id, parent_id]

def get_post_data(driver, wait, formatter, post_link):
    driver.get(post_link)
    time.sleep(3)
    
    post_ids = []
    social_media_id = []
    comment_texts = []
    url = []
    username_texts = []
    comment_dates = []
    comment_likes = []
    profile_links = []
    comment_ids = []
    parent_ids = []
    comment_set_ids = set()
    
    try:
        comments_section = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x5yr21d xw2csxc x1odjw0f x1n2onr6')]")))
    except:
        return None

    check_comments = driver.find_elements(By.XPATH, "//span[@class='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x133cpev x1xlr1w8 x5n08af x2b8uid x4zkp8e x41vudc x10wh9bi x1wdrske x8viiok x18hxmgj']")
    if check_comments:
        post_owner_info = get_post_info(driver, wait)
        post_data = {
            'PostId': [post_owner_info[6]],
            'SocialMediaId': [5],
            'Text': [post_owner_info[0]],
            'TextUrl': [post_owner_info[1]],
            'Name': [post_owner_info[2]],
            'PostDate': [formatter.format_date(post_owner_info[3])],
            'LikeCount': [post_owner_info[4]],
            'ProfileUrl': [post_owner_info[5]],
            'CommentId': ["null"],
            'ParentId': [post_owner_info[7]]
        }
        return post_data

    scroll_down(comments_section, driver)
    
    load_more_replies(driver, wait)

    comment_blocks = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xsag5q8 xz9dl7a x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']")))
    comment_blocks.pop(0)
    owner_info = get_post_info(driver, wait)
    comment_texts.insert(0, owner_info[0])
    url.insert(0, owner_info[1])
    username_texts.insert(0, owner_info[2])
    comment_dates.insert(0, formatter.format_date(owner_info[3]))
    comment_likes.insert(0, owner_info[4])
    profile_links.insert(0, owner_info[5])
    post_ids.insert(0, owner_info[6])
    comment_ids.insert(0, "null")
    parent_ids.insert(0, owner_info[7])
    
    for block in comment_blocks:
        comment_info = get_comment_info(block)
        comment_set_id = ''.join(comment_info)
        if comment_set_id not in comment_set_ids:
            comment_set_ids.add(comment_set_id)
            comment_texts.append(comment_info[0])
            url.append(comment_info[1])
            username_texts.append(comment_info[2])
            comment_dates.append(formatter.format_date(comment_info[3]))
            comment_likes.append(comment_info[4])
            profile_links.append(comment_info[5])
            post_ids.append(owner_info[6])
            comment_ids.append(comment_info[6])
            parent_ids.append(comment_info[7])
            parent_comment_id = comment_info[6]
            try:
                parent_element = block.find_element(By.XPATH, ".//ancestor::div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']")
                replies_containers = parent_element.find_element(By.XPATH, ".//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1 x540dpk']")
                reply_blocks = replies_containers.find_elements(By.XPATH, ".//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xsag5q8 xz9dl7a x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']")
                for block in reply_blocks:
                    comment_info = get_comment_info(block)
                    comment_set_id = ''.join(comment_info)
                    if comment_set_id not in comment_set_ids:
                        comment_set_ids.add(comment_set_id)
                        comment_texts.append(comment_info[0])
                        url.append(comment_info[1])
                        username_texts.append(comment_info[2])
                        comment_dates.append(formatter.format_date(comment_info[3]))
                        comment_likes.append(comment_info[4])
                        profile_links.append(comment_info[5])
                        post_ids.append(owner_info[6])
                        comment_ids.append(comment_info[6])
                        parent_ids.append(parent_comment_id)
            except:
                continue
    for _ in comment_texts:
        social_media_id.append(5)
        
    post_data = {
        'PostId': post_ids,
        'SocialMediaId': social_media_id,
        'Text': comment_texts,
        'TextUrl': url,
        'Name': username_texts,
        'PostDate': comment_dates,
        'LikeCount': comment_likes,
        'ProfileUrl': profile_links,
        'CommentId': comment_ids,
        'ParentId': parent_ids
    }
    return post_data

def main():
    excel_file = "posts_data_06-05-2024.xlsx"
    post_links = read_excel_columns(excel_file)
    driver, wait = initialize_driver()
    formatter = DateFormatter()
    login_to_instagram(driver, "username", "password")

    all_post_data = {
        'PostId': [],
        'SocialMediaId': [],
        'Text': [],
        'TextUrl': [],
        'Name': [],
        'PostDate': [],
        'LikeCount': [],
        'ProfileUrl': [],
        'CommentId': [],
        'ParentId': []
    }

    for post_link in post_links:
        post_data = get_post_data(driver, wait, formatter, post_link)
        if post_data is None:
            continue
        for key in all_post_data.keys():
            all_post_data[key].extend(post_data.get(key, []))

    driver.quit()
    df = pd.DataFrame(all_post_data)
    
    instagram_scraped = f"{excel_file[:-5]}_instagram_comments.xlsx"
    df.to_excel(instagram_scraped, index=False)
    
    merger = ExcelMerger("standart.xlsx")
    merger.merge(instagram_scraped)
    merger.save("standart.xlsx")

if __name__ == "__main__":
    main()
