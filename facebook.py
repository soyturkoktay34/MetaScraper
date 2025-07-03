from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
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
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait
    
def login_to_facebook(driver, username, password):
    driver.get("https://www.facebook.com/")
    time.sleep(2)
    username_field = driver.find_element(By.NAME, 'email')
    password_field = driver.find_element(By.NAME, 'pass')
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)
    
def load_more_comments(driver, wait):
    while True:
        try:
            buttons = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//span[contains(@class, 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xi81zsa')]")))
            if len(buttons) > 5:
                last_button = buttons[-1]
                driver.execute_script("arguments[0].click();", last_button)
                time.sleep(2)
            else:
                break
        except Exception:
            break
            
def get_post_info(driver, wait):
    try:
        owner_element = driver.find_element(By.XPATH, "//a[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u x1s688f']")
        owner_name = owner_element.text
        owner_profile_link = owner_element.get_attribute("href")
        try:
            post_elements = driver.find_elements(By.XPATH, "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h']")
            post_text = '\n'.join([elem.text.strip() for elem in post_elements])
        except:
            post_text = "no post text"
        get_post_date = driver.find_element(By.XPATH, "//a[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 xo1l8bm']")
        hover = ActionChains(driver).move_to_element(get_post_date)
        hover.perform()
        post_date = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1nxh6w3 x1sibtaa xo1l8bm xzsf02u']"))).text
        try:
            post_like_element = driver.find_element(By.XPATH, "//span[@class='x1e558r4']")
            post_like = post_like_element.text
        except:
            post_like = "0"
        post_url = driver.current_url
        post_id_start = post_url.find("posts/") + len("posts/")
        post_id = post_url[post_id_start:]
        try:
            get_post_shares = driver.find_elements(By.XPATH, "//div[contains(@class, 'x1i10hfl x1qjc9v5 xjqpnuy xa49m3k xqeqjp1 x2hbi6w x1ypdohk xdl72j9 x2lah0s xe8uvvx x2lwn1j xeuugli xggy1nq x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1lku1pv x1a2a7pz xjyslct xjbqb8w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1heor9g xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 xt0b8zv x1hl2dhg x1ja2u2z') and not(@aria-expanded='true')]")
            post_share = get_post_shares[0].text
        except:
            post_share = "0"
        parent_id = "null"
        return [post_text, post_url, owner_name, post_date, post_like, owner_profile_link, post_id, parent_id, post_share]
    except Exception as e:
        print("Error:", e)
        return None

def get_comment_info(driver, wait, block):
    try:
        load_more_button = block.find_element(By.XPATH, "//div[@role='button'][contains(@class, 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 xggy1nq x1a2a7pz xt0b8zv x1hl2dhg xzsf02u x1s688f')]")
        load_more_button.click()
    except:
        pass
    try:
        comment_element = block.find_element(By.XPATH, ".//div[@class='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs']")
        comment_text = comment_element.text
    except NoSuchElementException:
        comment_text = "no comment text"
    user_element = block.find_element(By.XPATH, ".//span[contains(@class, 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa x1s688f xzsf02u')]")
    username = user_element.text
    date_element = block.find_element(By.XPATH, ".//span[@class='html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs']")
    hover = ActionChains(driver).move_to_element(date_element)
    hover.perform()
    date_text = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa xo1l8bm xzsf02u']"))).text
    likes = block.find_elements(By.XPATH, ".//span[@class='xi81zsa x1nxh6w3 x1fcty0u x1sibtaa xexx8yu xg83lxy x18d9i69 x1h0ha7o xuxw1ft']")
    like_text = likes[0].text if likes else "0"
    profile_link_element = block.find_element(By.XPATH, ".//a[contains(@class, 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 xggy1nq x1a2a7pz x1heor9g xt0b8zv x1hl2dhg') and @href]")
    profile_link = profile_link_element.get_attribute('href')
    cleaned_link = profile_link.split('comment_id=')[0]
    profile_link = cleaned_link
    link_element = block.find_element(By.XPATH, ".//a[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 xggy1nq x1a2a7pz xt0b8zv x1hl2dhg xi81zsa xo1l8bm']")
    href = link_element.get_attribute('href')
    params = dict(param.split('=') for param in href.split('?')[1].split('&') if '=' in param)
    if "reply_comment_id" in params:
        parent_id = params["comment_id"]
        comment_id = params["reply_comment_id"]
    else:
        parent_id = "null"
        comment_id = params["comment_id"]
    url = href
    comment_share = "0"
    return [comment_text, url, username, date_text, like_text, profile_link, comment_id, parent_id, comment_share]

def get_post_data(driver, wait, formatter, post_link):
    driver.get(post_link)
    time.sleep(3)
    
    post_ids = []
    social_media_id = []
    comment_texts = []
    post_urls = []
    usernames = []
    date_texts = []
    like_texts = []
    profile_links = []
    comment_ids = []
    parent_ids = []
    post_shares = []
    
    post_info = get_post_info(driver, wait)
    if post_info:
        post_ids.insert(0, post_info[6])
        social_media_id.insert(0, 4)
        comment_texts.insert(0, post_info[0])
        post_urls.insert(0, post_info[1])
        usernames.insert(0, post_info[2])
        date_texts.insert(0, formatter.format_date(post_info[3]))
        like_texts.insert(0, post_info[4])
        profile_links.insert(0, post_info[5])
        comment_ids.insert(0, "null")
        parent_ids.insert(0, post_info[7])
        post_shares.insert(0, post_info[8])
        
    try:
        sort_comments = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//span[contains(@class, 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xi81zsa')])")))
        time.sleep(1)
        sort_comments[4].click()
        sort_all_comments = sort_all_comments = driver.find_elements(By.XPATH, "(//span[contains(@class, 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h')])")
        time.sleep(1)
        sort_all_comments[-1].click()
        time.sleep(3)
    except:
        post_data = {
            'PostId': post_ids,
            'SocialMediaId': social_media_id,
            'Text': comment_texts,
            'TextUrl': post_urls,
            'Name': usernames,
            'PostDate': date_texts,
            'LikeCount': like_texts,
            'ProfileUrl': profile_links,
            'CommentId': comment_ids,
            'ParentId': parent_ids,
            'RetweetCount': post_shares
        }
        return post_data
        
    load_more_comments(driver, wait)

    comment_blocks = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='x78zum5 xdt5ytf']")))
    comment_blocks.pop(0)
    
    for block in comment_blocks:
        comment_info = get_comment_info(driver, wait, block)
        post_ids.append(post_info[6])
        social_media_id.append(4)
        comment_texts.append(comment_info[0])
        post_urls.append(comment_info[1])
        usernames.append(comment_info[2])
        date_texts.append(formatter.format_date(comment_info[3]))
        like_texts.append(comment_info[4])
        profile_links.append(comment_info[5])
        comment_ids.append(comment_info[6])
        parent_ids.append(comment_info[7])
        post_shares.append(comment_info[8])

    post_data = {
        'PostId': post_ids,
        'SocialMediaId': social_media_id,
        'Text': comment_texts,
        'TextUrl': post_urls,
        'Name': usernames,
        'PostDate': date_texts,
        'LikeCount': like_texts,
        'ProfileUrl':profile_links,
        'CommentId': comment_ids,
        'ParentId': parent_ids,
        'RetweetCount': post_shares
    }
    return post_data

def main():
    driver, wait = initialize_driver()
    login_to_facebook(driver, "username", "password")
    formatter = DateFormatter()
    post_links = ["post links"]
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
        'ParentId': [],
        'RetweetCount': []
    }

    for post_link in post_links:
        post_data = get_post_data(driver, wait, formatter, post_link)
        for key in all_post_data.keys():
            all_post_data[key].extend(post_data.get(key, []))

    df = pd.DataFrame(all_post_data)
    driver.quit()

    facebook_scraped = "facebook_comments.xlsx"
    df.to_excel(facebook_scraped, index=False)
        
    merger = ExcelMerger("standart.xlsx")
    merger.merge(facebook_scraped)
    merger.save("standart.xlsx")
    
if __name__ == "__main__":
    main()
