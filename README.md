# 591_web_crawler
An automated web crawler for the house rental website: https://www.591.com.tw/


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



## Potential Optimization
- Change the way of getting content: 
  * **Current solution:** simulate browser behavior with `selenium`, `chromedriver` and parse `html`
  * **Potential fix:** send requests directly and parse the `json` response
- Optimze computation method: 
  * **Current solution:** sequentially scan all pages, needs to wait in line
  * **Potential fix:** use parallel computation to get more timely results
