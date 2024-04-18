import os

from datetime import datetime

today = datetime.today()

# print data to console
def print_data(data):
    print("Detail print\n")
    for item in data: 
        if item != None:
            print("- " + str(item) + "\n")
    
    print("-------------------------------\n")

# write data to sheet excel
# return sheet
def write_data_to_sheet(sheet, cnt, data, page = None):
    start_col = 1

    sheet.write(cnt, 0, today.strftime("%d/%m/%y %H:%M:%S"))
    
    if page is not None:
        sheet.write(cnt, 1, page)
        start_col = 2

    col = start_col
    for item in data:
        sheet.write(cnt, col, item)
        col += 1
    
    return sheet

# write header to sheet
def write_headers_to_sheet(sheet, cnt, headers):
    # Ngày lấy tin
    sheet.write(cnt, 0, "Date crawler")

    col = 1
    for item in headers:
        sheet.write(cnt, col, item)
        col += 1
    
    return sheet

# next page or go to other page
def build_bds_page(url, page):
    page_str = "/p" + str(page)
    arr_url = url.split("?", 1)

    result = None
    if len(arr_url) == 1:
        result = arr_url[0] + page_str
        print(result)
        return result

    result = arr_url[0] + page_str  + "?" + arr_url[1]
    print(result)
    return result

# build all next page
# ex: https://batdongsan.com.vn/nha-dat-cho-thue?gtn=0-trieu&gcn=100-trieu, 
# https://batdongsan.com.vn/nha-dat-cho-thue/p2?gtn=0-trieu&gcn=100-trieu
def build_list_page(target_url, page_from, page_to):
    lst_page = []

    for r in range(page_from, page_to + 1):
        url = build_bds_page(target_url, r)
        lst_page.append(url)
    
    return lst_page

def encode_utf_8_windows(str):
    # print("Before encode: " + str)

    if str == None: 
        return None
    

    str = str.encode('utf-8').decode('utf-8', 'ignore')
    # print("After encode: " + str)
    return str

def create_file_name(str):
    str_arr = str.split("?", 1)
    if len(str_arr) > 1:
        str = str_arr[0]
    
    str_arr = str.split("/")
    lens = len(str_arr)
    str = str_arr[lens - 1]

    strtoday = today.strftime("%d%m%Y") + "-" + str
    return strtoday

def create_folder_from_spider_name(spider_name):
    folder_name = spider_name + "/"
    
    try:
        os.makedirs(folder_name)
    except FileExistsError:
        # directory already exists
        pass

    return folder_name

def create_output_filename_xls(folder_name, spider_name, ts, page_from, page_to = None):
    if page_to is not None:
        return "{}{}-{}-page{}-page{}.xls".format(folder_name, spider_name, str(ts), page_from, page_to)
    
    return "{}{}-{}-page{}.xls".format(folder_name, spider_name, str(ts), page_from)