# bay-scrape

Price history scraping, archival and plotting for popular online auction market.

## Demo: GPUs

Interactive plot available at https://robot.emerge.moe/market/gpu.

![Demo image](/assets/demo.png)

## Stages

### 1. Scraping

Data is scraped via Selenium. What to scrape can be configured via [`config.py`](/scrape/config.py).  
The system is not perfect due to ever-changing HTML and a couple interesting issues on the website.  
Nonetheless, the output of the previous run can be passed to update the data and keep a full record.  

### 2. Filtering

Following the scraping process, the data is very noisy. There are many unwanted data points.  
Filtering uses regular expressions to remove unrelated items and improve accuracy.  

See the pre/post-filtering comparison:

![Pre/post-filtering comparison](/assets/filter.png)

### 3. Plotting

Plotly is used to plot the data. An HTML file is created.
