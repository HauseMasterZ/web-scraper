import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url):
        """
        Initialize the PharmEasyScraper class.

        Args:
            url (str): The URL of the product page.
        """
        self.url = url

    def fetch_html(self, custom_url=None):
        """
        Fetch the HTML content of the web page.

        Args:
            custom_url (str, optional): Custom URL to fetch HTML from. Defaults to None.

        Returns:
            str: The HTML content of the web page.

        Raises:
            Exception: If failed to fetch HTML content.
        """
        if custom_url is None:
            custom_url = self.url
        try:
            response = requests.get(custom_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
            })
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception("Failed to fetch HTML content.") from e

    def scrape_reviews(self):
        """
        Scrape the reviews from the product page.

        Returns:
            list: A list of dictionaries containing review information.
        """
        html = self.fetch_html(self.url + '/reviews')
        soup = BeautifulSoup(html, "html.parser")
        review_container = soup.find(
            'div', class_='AllReviews_mainContainer__5I9ll')
        reviews = []

        if review_container:
            review_elements = review_container.find_all(
                'div', class_='RecentReviews_reviewAuthor__2W0xn')

            for review_element in review_elements:
                parent = review_element.parent
                name = review_element.string
                star_count = len(parent.find_all(
                    'path', fill='url(#progress_1)'))
                description_element = parent.find(
                    'div', class_='RecentReviews_reviewComment__63GHI')
                description = description_element.string if description_element else None
                date_element = parent.find(
                    'div', class_='RecentReviews_reviewTime___cO0n')
                date = date_element.string if date_element else None
                reviews.append({'name': name, 'body': description,
                               'date': date, 'stars': star_count})

        return reviews

    def scrape_price(self):
        """
        Scrape the price from the product page.

        Returns:
            str: The price of the product.
        """
        html = self.fetch_html()
        soup = BeautifulSoup(html, "html.parser")
        price_element = soup.find(
            "div", class_="ProductPriceContainer_mrp__mDowM")
        price = price_element.text.strip() if price_element else None

        return price


url = input('Enter Website URL:')
scraper = Scraper(url)

reviews = scraper.scrape_reviews()
print("Reviews:")
for review in reviews:
    print(f"Name: {review['name']}")
    print(f"Body: {review['body']}")
    print(f"Date: {review['date']}")
    print(f"Stars: {review['stars']}")
    print('')

price = scraper.scrape_price()
print("Price:", price)
