# 591_web_crawler
An automated web crawler for the house rental website: https://www.591.com.tw/
- Purpose: get all property information on the platform. 

## How to Install 
- OS: Windows 7+
- Python 3.7.0 
- Packages: 
    * pandas==0.24.2
    * Pillow==5.2.0
    * pytesseract==0.3.2
        * install pytesseract via `pip`
        * install binary from https://github.com/UB-Mannheim/tesseract/wiki
        * add binary path to `PATH` in OS Settings
    * beautifulsoup4==4.6.3
    * requests==2.23.0
    * selenium==3.141.0
    * chrome driver 
       * download & install binary from https://chromedriver.chromium.org/downloads

## How to Run
- **Connection:** set connection id & password if required
  * if your internet connection requires id & password, set them up in `bs4_591.py`: `RootPageInitiator.login()`
  * if not, skip this section 
- **Run:** run `bs4_591.py`

## Known Issue
- **Data repetition:** 1,967 columns are duplicate columns from a total of ~23,261 columns in all counties in Taiwan. (as of 2020/3)
  * Possible reason 1: time lag from web crawling work 
  * Possible reason 2: 591-website changes link sequence everytime browser is refreshed 
  * Possible reason 2: 591-website repeats property links itself 
- **Low Performance:** currently it takes ~2 hrs to parse 900 properties, which would take ~51 hrs (2-3 days) to parse all ~23,000 properties online. 

## Possible Extension
- **Extend function:** extend function to include the latitude and longitude of property

## Potential Optimization
- **Improve Performance & Data Repetition:** 
   - Change the way of getting content: 
     * Current solution: simulate browser behavior with `selenium`, `chromedriver` and parse `html`
     * Potential fix: send requests directly and parse the `json` response
   - Optimze computation method: 
     * Current solution: sequentially scan all pages, needs to wait in line
     * Potential fix: use parallel computation to get more timely results
