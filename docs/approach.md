Approach behind this crawler:

Breaking Down the Problem
The goal is simple: automate the process of finding product URLs from multiple e-commerce websites. But there are a few challenges:

Every website has a different URL structure, so there needs to be a way to recognize product pages.
Some sites rely on JavaScript to load content, which means Selenium is required instead of just requests.
It’s important to filter out duplicates and non-product links to keep the results clean.

How the Crawler is Built:

1) Choosing the Right Scraping Method:
Some websites work fine with requests and BeautifulSoup, but others need Selenium to handle JavaScript-loaded content.

2) Extracting Only Product Links:
Pattern-based filtering is used to ensure only product pages are collected while skipping ads, banners, and other unnecessary links.

3) Saving the Data:
The extracted URLs are stored in JSON and CSV formats to make them easy to use later.