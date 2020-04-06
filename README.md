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
- **Get all proprety info:** run `bs4_591.py`, program outputs results for every county to `tmp/` in the form of `591_output_{county}_{cnt}.xlsx`
  * scan main page for each counties (filter: "租屋"+"屋主"+指定縣市) & get total page count, ex: https://rent.591.com.tw/?kind=0&region=1&shType=host
  * scan each page and get link for properties
  * scan each property page to get property information

- **Analyze:** run `analyze.py` to combine all `*.xlsx` files and plot an X-Y chart to demonstrate expected income for different landlords (below are results as of 2020/3/27)
  * combine all county's information to one dataframe: 23,261 records
  * dedup records: 21,294 records after dedup
  * group by cell phone number to calculate total rental income for each landlord: recognized 15,266 numbers (landlords)
  * plot an X-Y chart to demonstrate (see `591.png`)
       * X-axis: total rental income for this landlord
       * Y-axis: number of properties this landlord owns

## Known Issue
- **Data repetition:** 1,967 columns are duplicate columns from a total of ~23,261 columns in all counties in Taiwan. (as of 2020/3/27)
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
