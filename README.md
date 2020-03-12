# 591_web_crawler
An automated web crawler for the house rental website: https://www.591.com.tw/


## How to Install 
- OS: Windows 7+
- Python 3.7.0 
- Packages: 
    * pytesseract
        * install pytesseract via `pip`
        * install binary from https://github.com/UB-Mannheim/tesseract/wiki
        * add binary path to `PATH` in OS Settings
    * PIL
    * bs4
    * selenium
    * chrome driver 
       * download & install binary from https://chromedriver.chromium.org/downloads

## How to Run



## Potential Optimization
- Change the way of getting content: 
  * **Current method:** simulate browser behavior with `selenium` and parse `html` (powerful but time & memory consuming)
  * **Potential fix:** send requests directly and parse response `json` directly
- Computation resource: 
  * **Current method:** sequentially scan all pages, needs to wait in line
  * **Potential fix:** use parallel computation to get more timely results
