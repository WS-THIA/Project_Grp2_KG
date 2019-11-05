## About 
On branch `geraldine`, locally saved the data folders (ignored when pushed to remote) and code to scrape the data from Burpple website. 

## Project Structure
### data
Working folder where some results are stashed.
`sample_scraped.json` contains the scraped data of a single user.
`scraped_1042_users.json` contains about 1042 users' scraped data. 

### data_scraped
Contains the final data from 2 sub-folders:
- **User_scraping**: From the first round of scraping (Getting Reviews from Users).
- **Restaurant_scraping**: From the second round of scraping (Getting Reviews from Restaurants)

### scraping_code
Contains
- code for the scraping, in the form of `.ipynb` notebooks. There are 2 used for scraping reviews from Users and Restaurants respectively using bs4 and selenium for scraping. 
- webscrape_selenium folder from weisoon containing his code for selenium. 
- chrome drivers




