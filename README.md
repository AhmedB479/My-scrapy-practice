# BOOKS TO SCRAPE BEING SCRAPED




## Acknowledgements
Here is a link if you ever wanna do it yourself
 - [Scrapy Course – Python Web Scraping for Beginners](https://www.youtube.com/watch?v=mBoX_JCKZTE)

 - [the website being scraped](https://books.toscrape.com/)


## Deployment

terminal commands to remember if you ever wanna run scrapy

### To install venv so that your third party libraries versions dont clash
```bash
pip install virtualenv
```
### To setup venv
```bash
python -m venv [folder name]
```
### To activate venv
```bash
source venv/Scripts/activate
```
### To install scrapy
```bash
pip install scrapy
```
### To create new project
```bash
scrapy startproject [projectname]
```
### To run and output spider -o to add, -O to overwrite (NOTE TO SELF MAKE SPIDER IN SPIDERS FOLDER)
```bash
scrapy crawl [filename] -o [filename].[format]
```
### To run shell for scrapy
Most of the code can be tested within scrapy shell before Deployment
```bash
scrapy shell
```
