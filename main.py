import time 
import helper

from xlwt import Workbook
from selenium.webdriver.common.by import By 
from browser import get_browser

SPIDER_NAME = "top100folder"
folder_name = helper.create_folder_from_spider_name(SPIDER_NAME)

# parse each page
def parse_post_detail(driver):
    # get list element in page
    lst_h3 = driver.find_elements(By.CSS_SELECTOR, "#fsb h3")
    lst_p = driver.find_elements(By.CSS_SELECTOR, "#fsb p[id*=row]")

    result = []
    cnt = 0
    for itm_h3 in lst_h3:
        itm_p = lst_p[cnt]
        cnt += 1
        
        if cnt == 15:
            break

        name = itm_h3.find_element(By.CSS_SELECTOR, "a").text
        
        try:
            url_feed = itm_h3.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            address = itm_p.find_element(By.CSS_SELECTOR, "span[class*=location_new]").text
            rss = itm_p.find_element(By.CSS_SELECTOR, "a[class*=ext]").get_attribute("href")
            url_website = itm_p.find_element(By.CSS_SELECTOR, "a[class*=extdomain]").get_attribute("href")
            short_desc = itm_p.find_element(By.CSS_SELECTOR, "span[class*=feed_desc]").text
            follow_fb = None

            try:
                follow_fb = itm_p.find_element(By.CSS_SELECTOR, "span[class*=fs-facebook] span").text
            except:
                pass

            follow_x = None
            try:
                follow_x = itm_p.find_element(By.CSS_SELECTOR, "span[class*=fs-twitter] span").text
            except:
                pass

            frequence = None
            try:
                frequence = itm_p.find_element(By.CSS_SELECTOR, "span[class*=fs-frequency] span").text
            except:
                pass

            print("Parse done {}".format(name))
            result.append([name, url_feed, address, rss, url_website, short_desc, follow_fb, follow_x, frequence])
        except:
            print("Parse fail {}".format(name))
    
    return result

# from list page and for each post
# create and write data to excel file
def parse_post(driver, target_url = 'https://rss.feedspot.com/ai_rss_feeds/#rightModal', page_from = 1, page_to = 1):
    # create header
    headers = ["Name", "URL feedspot", "Address", "RSS", "URL website", "Short Description", "Follow FB", "Follow X", "Frequence"]

    # create file name, get timestampt to distinct with each file
    # ts = int(time.time())
    ts = helper.create_file_name(target_url)

    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')

    # write header, file 
    helper.write_headers_to_sheet(sheet1, 1, headers)
    filename_output = helper.create_output_filename_xls(folder_name, SPIDER_NAME, ts, 1)

    try:
        driver.get(target_url)
        time.sleep(5)
    except:
        print(target_url)
        wb.save(filename_output)

    data_result = parse_post_detail(driver)

    cnt_2 = 2
    for item in data_result:    
        sheet1 = helper.write_data_to_sheet(sheet1, cnt_2, item, None)
        cnt_2 += 1

    wb.save(filename_output)

if __name__ == '__main__':
    driver = get_browser()
    parse_post(driver)
    driver.close()