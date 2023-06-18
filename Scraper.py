import requests
from bs4 import BeautifulSoup
#Uncomment the following imports if you want to use selenium.
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

class Scraper:
    def __init__(self, url):
        """
        Initialize the Scraper class.

        Args:
            url (str): The URL of the product page.
        """
        self.url = url
        # self.driver = webdriver.Chrome() # Uncomment for selenium driver.

    def extract_longest_continuous_numbers(self, string):
        """
        Extract the longest continuous sequence of digits from a string.

        Args:
            string (str): Input string.

        Returns:
            str: The longest continuous sequence of digits.
        """
        longest_sequence = ''
        current_sequence = ''
        for char in string:
            if char.isdigit():
                current_sequence += char
            elif current_sequence:
                if len(current_sequence) > len(longest_sequence):
                    longest_sequence = current_sequence
                current_sequence = ''
        if current_sequence:
            if len(current_sequence) > len(longest_sequence):
                longest_sequence = current_sequence
        return longest_sequence

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
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
            }
            response = requests.get(custom_url, headers=headers)
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

        
        # Following code is for Manual selenium browser driver scrolling

        # self.driver.get(self.url)
        # while True:
        #     try:
        #         self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #         WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "AllReviews_mainContainer__5I9ll")))
        #     except:
        #         break
        # html = self.driver.page_source
        # # html = self.fetch_html(self.url + '/reviews')
        # soup = BeautifulSoup(html, "html.parser")
        # review_container = soup.find(
        #     'div', class_='AllReviews_mainContainer__5I9ll')
        # reviews = []

        # if review_container:
        #     review_elements = review_container.find_all(
        #         'div', class_='RecentReviews_reviewAuthor__2W0xn')
        #     for review_element in review_elements:
        #         parent = review_element.parent
        #         name = review_element.string
        #         star_count = len(parent.find_all(
        #             'path', fill='url(#progress_1)'))
        #         description_element = parent.find(
        #             'div', class_='RecentReviews_reviewComment__63GHI')
        #         description = description_element.string if description_element else None
        #         date_element = parent.find(
        #             'div', class_='RecentReviews_reviewTime___cO0n')
        #         date = date_element.string if date_element else None
        #         reviews.append({'name': name, 'body': description,
        #                        'date': date, 'stars': star_count})
        # return reviews

        # Uncomment till here


        # Api Fetching
        api_number = self.extract_longest_continuous_numbers(self.url)
        all_reviews = []
        page = 1
        while True:
            review_url = f'https://pharmeasy.in/api/browse/product/reviews/{api_number}?page={page}&showAll=1'
            response = requests.get(review_url, headers=self.get_request_headers()).json()
            try:
                if not response['data']['response']:
                    break
            except KeyError:
                return []
            
            all_reviews.extend(response['data']['response'])
            page += 1
        return all_reviews

    def scrape_price(self):
        """
        Scrape the price from the product page.

        Returns:
            str: The price of the product.
        """
        html = self.fetch_html()
        soup = BeautifulSoup(html, "html.parser")
        if 'reviews' not in self.url:
            price_element = soup.find("div", class_="ProductPriceContainer_mrp__mDowM")
        else:
            price_element = soup.find("div", class_="ProductCard_ourPrice__yDytt")
        price = price_element.text.strip() if price_element else None
        return price

    def get_request_headers(self):
        """
        Get the request headers.

        Returns:
            dict: Request headers.
        """
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }


if __name__ == '__main__':
    url = input('Enter Website URL: ')
    while not url:
        print('Invalid URL, Please Try Again...')
        url = input('Enter Website URL: ')

    scraper = Scraper(url)

    reviews = scraper.scrape_reviews()
    if reviews:
        print("Reviews:")
        for review in reviews:
            print(f"Customer Name: {review['customerName']}")
            print(f"Review: {review['review']}")
            print(f"Posted Date: {review['posted']}")
            print(f"Stars: {review['score']}")
            print('')
    else:
        print('There are no reviews for the product yet. Please try again later.')

    price = scraper.scrape_price()
    print("Price:", price)
    # scraper.driver.quit()
