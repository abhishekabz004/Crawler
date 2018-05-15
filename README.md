# AmazonScrapper
Scrapes product details from ecommerse site Amazon. On average this crawler gets about 5000 dataset for each product category defined in our taxonomy.

## How is it done?
- The defined taxonomy is formed as a map(**"Amazon_Map.csv"**) with respect to this website and thus categories when fetched would be converted according to our system's definition. 
- For instance, when a product is found to be belonging under the category**Clothing&Accessories:Men:T-Shirts&Polos** when fetched  will be converted into **Men>Topwear>Casual>Tshirts&Polos**.
- In case if any new category comes up, we can simply run the code again after adding the category details in the map file.

## Guidelines to run the scrapper
Clone this project and install the project's virtual environment setting using conda 
```
conda install --name a_crawler --file  venvRequirements.txt
```
Activate the virtual environment.
```
source activate a_crawler
```
Run the spider defined to start crawling data.
```
scrapy crawl TshirtsSpider
```
