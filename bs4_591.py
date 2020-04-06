from bs4 import BeautifulSoup
import requests
import re
from PIL import Image
import pytesseract  
#download binary from https://github.com/UB-Mannheim/tesseract/wiki. then add pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe' to your script. (replace path of tesseract binary if necessary)
#
#references: https://pypi.org/project/pytesseract/ (INSTALLATION section) and https://github.com/tesseract-ocr/tesseract/wiki#installation
from selenium import webdriver


from io import BytesIO
import pandas as pd
import time
import random
import math

#%%
class PropertyPageParser(): 
    def __init__(self, url): 
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    
    def parse_all(self): 
        response = requests.get(self.url, headers=self.headers, verify=False)
        text = response.text
#        print(text)
        
        soup = BeautifulSoup(text, "html.parser")
        
        property_number, address = self.parse_property_num_n_addr(soup)
        location = self.parse_location(soup)
        monthly_price = self.parse_price(soup)
        phone_number = self.parse_phone_number(soup)
        
        destination = [property_number, address, location, monthly_price, phone_number]
        
        return destination
    
    def parse_property_num_n_addr(self, soup): 
        propNav = soup.find('div', {'id': 'propNav'})
        
        prop_number = propNav.find('i').text
        prop_number = re.search('（([A-Za-z\d]*?)）', prop_number)
        prop_number = prop_number.group(1)
        addr = propNav.find('span').text
        
        return prop_number, addr
    
    def parse_location(self, soup): 
#        block = soup.find('div', {'jstcache': '36'})
#        print(block)
        return ''
    
        
    def parse_price(self, soup): 
        price_block = soup.find('div', {'class': 'price clearfix'}).text
        monthly_price = re.search('([\d,]*) 元/月', price_block).group(1)
        return monthly_price

    def parse_phone_number(self, soup): 
        '''
        return value: 
            - cell phone number if applies 
            - blank string ('') if it shows 591 number (land lord turns on 'protect number' function)
        '''
        
        try: 
            block = soup.find('div', {'class': 'j-phone infoTwo clearfix-new phone-hide kfDialingNum'})
            pic_url = 'http:'+block.find('img')['src']+'.png'
            phone_number = self.image_to_str(pic_url)
        except TypeError: 
            phone_number = ''
            
        return phone_number
    
    def image_to_str(self, img_url, whitelist='0123456789-'): 
        response = requests.get(img_url, headers=self.headers, verify=False)
    
        image = Image.open(BytesIO(response.content))
        
        for i in range(1,10): 
            resized_image = image.resize((140*i, 20*i))
            phone_number = pytesseract.image_to_string(resized_image, lang='eng', config='-c tessedit_char_whitelist={}'.format(whitelist)) 
            
            cell_match = re.match('\d{4}-\d{3}-\d{3}', phone_number)
            home_match = re.match('\d{2}-\d{8}', phone_number)
            
            if((home_match is not None) or (cell_match is not None)): 
                break
        
        return phone_number
    
class ListPageParser(): 
    def __init__(self): 
        pass
    
    def parse_all_links(self, text): 
        soup = BeautifulSoup(text, "html.parser")
    
        obj_list = soup.find_all('ul', {'class': 'listInfo clearfix '})
        
        data_list = []
        error_pages = []
        retry_pages = []
        sleeper = RandomSleeper()
        count = 0 
        for obj in obj_list: 
            for i in range(10):  # retry mechanism
                print("{0}: {1} run".format(count, i))
                href_text = obj.find('a')['href']
                href_text = href_text.replace(' ','')
                url = 'http:'+href_text
                print(url)
#                try: 
#                    print(url)
#                    break
#                except:
#                    pass
                try: 
                    data = [url]
                    page = PropertyPageParser(url=url)
                    data.extend(page.parse_all())
                    data_list.append(data)
                    sleeper.sleep()
                    break
                except Exception as e:
                    print(e)
                    if(i==0): 
                        retry_pages.append(url)
                    elif(i==9): 
                        error_pages.append(url)
                    if(i!=9): 
                        time.sleep(i*10)
                    continue 
            count=count+1
        
        destination_df = pd.DataFrame(data=data_list, columns=['url', 'property_number', 'address', 'location', 'monthly_price', 'phone_number'])
        destination_df = destination_df[['property_number', 'url', 'address', 'location', 'monthly_price', 'phone_number']]
        
        return destination_df, error_pages, retry_pages

class RandomSleeper(): 
    def __init__(self): 
        pass
    def sleep(self, max_time=5): 
        time.sleep(random.randint(0, max_time))

class RootPageInitiator(): 
    def __init__(self): 
        pass
    
    def login(self, browser): 
        user = browser.find_element_by_id("user")
        user.send_keys('')
        
        pswd = browser.find_element_by_id("passwd")
        pswd.send_keys('')
        
        submit = browser.find_element_by_id("submit")
        submit.click()
        
        return browser
        
    def init(self, root_url): 
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        browser = webdriver.Chrome(executable_path="D:\chromedriver.exe", options=chrome_options)
        browser.get(root_url)
        
        try:
            time.sleep(3)
            browser = self.login(browser)
            browser.get(root_url)
        except: 
            pass
        
        time.sleep(3)
        return browser 


class CountyParser(): 
    def __init__(self): 
        pass
    
    def link_county(self, county, root_url='https://rent.591.com.tw/?kind=0&shType=host'): 
        initiator = RootPageInitiator()
        browser = initiator.init(root_url)
        
        county_button = browser.find_element_by_xpath("//div[@id='area-box-body']/dl[@class='clearfix']/dd[@google-data-stat='首頁_縣市選擇_{}']".format(county))
        county_button.click()
        time.sleep(5)
        
        return browser
    
    def parse(self, county, start_segment): 
        browser = self.link_county(county)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        pages = soup.find_all('a', {'class': 'pageNum-form'})
        try: 
            last_page = pages[-1]
            total_pages = int(last_page.text)

        except: 
            total_pages = 1
        print(county, ":", total_pages)
        browser.quit()
    
        all_error_pages = dict()
        all_retry_pages = dict()
        
        pages_per_seg = 30
        total_segment = math.ceil(total_pages/pages_per_seg)
        all_df = pd.DataFrame()
        
        for page_seg in range(start_segment, total_segment): 
            print("\n\nSEG: ", page_seg)
            browser = self.link_county(county)
            
            destination_df = pd.DataFrame()
            start_page = page_seg*pages_per_seg+1
            end_page = min((page_seg+1)*pages_per_seg, total_pages)
            for page in range(start_page,end_page+1): 
                for i in range(10): 
                    try: 
                        print("\n\n*************** page {0}: {1} run ***************".format(page, i))
                        url = 'https://rent.591.com.tw/?kind=0&shType=host&firstRow={1}'.format(1, (page-1)*30)
                        browser.get(url)
                        time.sleep(3)
                        
                        text = browser.page_source
                        parser = ListPageParser()
                        df, error_pages, retry_pages = parser.parse_all_links(text)
                        
                        destination_df = destination_df.append(df, ignore_index=True)
                        
                        if(len(error_pages)!=0): 
                            all_error_pages.update({page:error_pages})
                        if(len(retry_pages)!=0): 
                            all_retry_pages.update({page: retry_pages})
                        break
                    except: 
                        time.sleep(60*10)
            
            browser.quit()
            destination_df.to_excel('tmp/591_output_{0}_{1}.xlsx'.format(county, page_seg), encoding='big5')
            all_df = all_df.append(destination_df, ignore_index=True)
            time.sleep(60*5)
        return all_df, all_retry_pages, all_error_pages
        

#%%
if __name__ == '__main__':     
    import warnings
    warnings.filterwarnings('ignore')
    
    root_url = 'https://rent.591.com.tw/?kind=0&shType=host'
    county_list = ['台北市', '新北市', '桃園市', '新竹市', '新竹縣', '宜蘭縣', '基隆市', '台中市','彰化縣','雲林縣','苗栗縣','南投縣','高雄市','台南市','嘉義市','嘉義縣','屏東縣',
                   '台東縣','花蓮縣','澎湖縣','金門縣','連江縣']
#    all_counties_df = pd.DataFrame()
#    all_counties_retry = dict()
#    all_counties_error = dict()
    
    for county in county_list: 
#        if(county=='高雄市'): 
#            start_segment = 3
#        else: 
        if(True): 
            start_segment = 0 
        
        parser = CountyParser()
        all_df, all_retry_pages, all_error_pages = parser.parse(county, start_segment)
        
#        all_df.to_excel('tmp/591_output_{}.xlsx'.format(county), encoding='big5')
        print("*"*8, "retry_pages: {}".format(len(all_retry_pages)), "*"*8)
        print(all_retry_pages)
        print("\n", "*"*8, "error_pages: {}".format(len(all_error_pages)), "*"*8)
        print(all_error_pages)
        
#        all_counties_df = all_counties_df.append(all_df, ignore_index=True)
#        all_counties_retry.update({county:all_retry_pages})
#        all_counties_error.update({county:all_error_pages})

#    all_counties_df.to_excel('591_output.xlsx', encoding='big5')
#    print("retry: ", all_counties_retry)
#    print("error: ", all_counties_error)