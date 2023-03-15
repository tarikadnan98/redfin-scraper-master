# redfin-scraper
A scraper for https://www.redfin.com

**HOW IT WORKS**
- Before running the script, you need to open the script and edit the code - input an URL to the first page of the search results for which you want to run the script. This is done in the following line of code (an example):<br/>
FIRST_PAGE_URL = "https://www.redfin.com/county/1825/NE/Lancaster-County/filter/max-days-on-market=3d"
- When the run is done, you should see a csv file with timestamped name created. You will also have a local database created in path with script, which will contain data for already scraped links so that in the future it doesn't visit these links again.

**REQUIREMENTS**
- Python 3.7
- lxml (pip install lxml)
- selenium (pip install selenium)
- Chrome web browser, keep updated to the last version
- chromedriver.exe placed on C:\ downloaded from http://chromedriver.chromium.org/downloads 



