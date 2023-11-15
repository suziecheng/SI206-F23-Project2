from bs4 import BeautifulSoup
import re
import os
import csv
import unittest

# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"

An example of that within the function would be:
    open("filename", "r", encoding="utf-8-sig")

There are a few special characters present from Airbnb that aren't defined in standard UTF-8 (which is what Python runs by default). This is beyond the scope of what you have learned so far in this class, so we have provided this for you just in case it happens to you. Good luck!
"""

def get_listings(html_file): 
    """
    get_listings(html_file) -> list 

    TODO Write a function that takes file data from the variable html_file, reads it, and loads it into a BeautifulSoup object 

    Parse through the object, and return a list of tuples that includes the listing title and the listing id. 
        
        The listing id is found in the url of a listing. For example, for https://www.airbnb.com/rooms/1944564 the listing id is 1944564.

    Example output: 
        [('Loft in Mission District', '1944564'), ('Home in Mission District', '49043049'), ...]

    """

    # create the beautiful soup ~
    with open(html_file, "r", encoding="utf-8-sig") as file:
        contents = file.read()
        soup = BeautifulSoup(contents, "html.parser")
    
    # find listing title
    listing_titles = soup.find_all("div", class_="t1jojoys dir dir-ltr")

    # find listing id
    listing_ids = []
    for id in listing_titles:
        match = re.search(r'\d+', id.get('id'))
        listing_id = match.group() if match else None
        listing_ids.append(listing_id)

    # create tuple
    output = []
    for i in range(len(listing_titles)):
        output.append((listing_titles[i].text.strip(), listing_ids[i]))
    return output


def get_listing_data(listing_id): 
    """
    get_listing_data(listing_id) -> tuple

    TODO Write a function that takes a string containing the listing id of an Airbnb and returns a tuple that includes the policy number, the place type, the number of reviews, and the nightly price of the listing. 

        Policy number (data type: str) - either a string of the policy number, "Pending", or "Exempt". 
            This field can be found in the section about the host.
            Note that this is a text field the lister enters, this could be a policy number, or the word "Pending" or "Exempt" or many others. Look at the raw data, decide how to categorize them into the three categories.

        Place type (data type: str) - either "Entire Room", "Private Room", or "Shared Room"
            Note that this data field is not explicitly given from this page. Use the following to categorize the data into these three fields.
                "Private Room": the listing subtitle has the word "private" in it
                "Shared Room": the listing subtitle has the word "shared" in it
                "Entire Room": the listing subtitle has neither the word "private" nor "shared" in it

        Number of reviews (data type: int)
            Do not forget to account for listings which have no reviews 

        Nightly price of listing (data type: int)

    Example output: 
        ('2022-004088STR', 'Entire Room', 422, 181)

    """
    # create file path
    file_path = os.path.join('html_files', f"listing_{listing_id}.html")

    # create the beautiful soup ~
    with open(file_path, "r", encoding="utf-8-sig") as file:
        contents = file.read()
        soup = BeautifulSoup(contents, "html.parser")

    # find policy number
    policy_number = []
    policy = soup.find("li", class_="f19phm7j dir dir-ltr")
    policy_number = policy.text[15:]

    # find place type
    place_type = []
    title = soup.find("div", class_="_cv5qq4")
    if title:
        if "private" in title.text.lower():
            place_type = "Private Room"
        elif "shared" in title.text.lower():
            place_type = "Shared Room"
        else:
            place_type = "Entire Room"

    # find number of reviews
    reviews = []
    number = soup.find('span', class_='_s65ijh7')
    reviews = int(number.text[:-8]) if number else 0

    # find nightly price
    price = []
    amount = soup.find('div', class_='_1jo4hgw')
    num = re.sub(r'\D', '', amount.text)
    price = int(num) if num else 0

    # create tuple
    output = (policy_number, place_type, reviews, price)
    return output

    

def create_detailed_listing_data(html_file): 
    """
    create_detailed_listing_data(html_file) -> list

    TODO Write a function that takes in a variable representing the path of the search_results.html file then calls the functions get_listings() and get_listing_data() in order to create and return the complete listing information. 
    
    This function will use get_listings() to create an initial list of Airbnb listings. Then use get_listing_data() to obtain additional information about the listing to create a complete listing, and return this information in the structure: 

        [
        (Listing Title 1,Listing ID 1,Policy Number 1,Place Type 1, Number of Reviews 1, Nightly Rate 1),
        (Listing Title 2,Listing ID 2,Policy Number 2,Place Type 2, Number of Reviews 2, Nightly Rate 2), 
        ... 
        ]

    NOTE: get_listings() returns a list of tuples where the tuples are of length 2, get_listing_data() returns just a tuple of length 4, and THIS FUNCTION returns a list of tuples where the tuples are of length 6. 

    Example output: 
        [('Loft in Mission District', '1944564', '2022-004088STR', 'Entire Room', 422, 181), ('Home in Mission District', '49043049', 'Pending', 'Entire Room', 67, 147), ...]    
    """
    
    # call get_listings
    listings = get_listings(html_file)

    # call get_listing_data
    complete_listings = []
    for listing in listings:
        listing_id = listing[1]
        info = get_listing_data(listing_id)
    
    # create tuple
        if info:
            combined_info = listing + info
            complete_listings.append(combined_info)

    return complete_listings


def output_csv(data, filename): 
    """
    TODO Write a function that takes in a list of tuples called data, (i.e. the one that is returned by create_detailed_listing_data()), sorts the tuples in ascending order by cost, writes the data to a csv file, and saves it to the passed filename. 
    
    The first row of the csv should contain "Listing Title", "Listing ID", "Policy Number", "Place Type", "Number of Reviews", "Nightly Rate", respectively as column headers. 
    
    For each tuple in the data, write a new row to the csv, placing each element of the tuple in the correct column. The data should be written in the csv in ascending order from the least costly to the most costly.

    Example output in csv file: 
        Listing Title,Listing ID,Policy Number,Place Type,Number of Reviews,Nightly Rate
        Private room in Mission District,23672181,STR-0002892,Private Room,198,109
        Guesthouse in San Francisco,49591060,STR-0000253,Entire Room,79,110
        ...


    """
    pass

def validate_policy_numbers(data):
    """
    validate_policy_numbers(data) -> list

    TODO Write a function that takes in a list of tuples called data, (i.e. the one that is returned by create_detailed_listing_data()), and parses through the policy number of each, validating that the policy number matches the policy number format. Ignore any pending or exempt listings. 

    Return a list of tuples that contains the name of the listing and listing id for listings whose respective policy numbers that do not match the correct format.
        
        Policy numbers are a reference to the business license San Francisco requires to operate a short-term rental. These come in two forms below. # means any digit 0-9.

            20##-00####STR
            STR-000####

    Example output: 
    [('Loft in Mission District', '1944564'), ...]

    """
    pass 

# EXTRA CREDIT 
def get_google_scholar_articles(query): 
    """
    get_google_scholar_articles(query) -> list

    TODO Write a function that imports requests library of Python
    and sends a request to google scholar with the passed query.
    
    Using BeautifulSoup, find all titles and return the list of titles you see on page 1. 
    (that means, you do not need to scrape results on other pages)

    You do not need to write test cases for this question.

    Example output using 'airbnb' as query: 
        ['Progress on Airbnb: a literature review',
        'Digital discrimination: The case of Airbnb. com',
        'COVID19 and Airbnb–Disrupting the disruptor',
        'Unravelling airbnb: Urban perspectives from Barcelona',
        'Poster child and guinea pig–insights from a structured literature review on Airbnb',
        'A first look at online reputation on Airbnb, where every stay is above average',
        'A Lefebvrian analysis of Airbnb space',
        'Airbnb: the future of networked hospitality businesses',
        'Who benefits from the" sharing" economy of Airbnb?',
        'Why tourists choose Airbnb: A motivation-based segmentation study']

    * see PDF instructions for more details
    """
    pass

# TODO: Don't forget to write your test cases! 
class TestCases(unittest.TestCase):

    def test_get_listings(self):
        # call get_listings("html_files/search_results.html")
        # and save to a local variable
        listings = get_listings("html_files/search_results.html")

         # check that the number of listings extracted is correct (18 listings)
        self.assertEqual(len(listings), 18)

        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(listings), list)

        # check that each item in the list is a tuple

        # check that the first title and listing id tuple is correct (open the search results html and find it)

        # check that the last title and listing id tuple is correct (open the search results html and find it)

    def test_get_listing_data(self):
        html_list = ["467507",
                     "1550913",
                     "1944564",
                     "4614763",
                     "6092596"]
        
        # call get_listing_data for i in html_list:
        listing_informations = [get_listing_data(id) for id in html_list]

        # check that the number of listing information is correct (5)
        self.assertEqual(len(listing_informations), 5)
        for listing_information in listing_informations:
            # check that each item in the list is a tuple
            self.assertEqual(type(listing_information), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(listing_information), 4)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(listing_information[0]), str)
            self.assertEqual(type(listing_information[1]), str)
            # check that the third element in the tuple is an int
            self.assertEqual(type(listing_information[2]), int)
            self.assertEqual(type(listing_information[3]), int)

        # check that the first listing in the html_list has the correct policy number

        # check that the last listing in the html_list has the correct place type

        # check that the third listing has the correct cost

    def test_create_detailed_listing_data(self):
        # call create_detailed_listing_data on "html_files/search_results.html"
        # and save it to a variable
        detailed_data = create_detailed_listing_data("html_files/search_results.html")

        # check that we have the right number of listings (18)
        self.assertEqual(len(detailed_data), 18)

        for item in detailed_data:
            # assert each item in the list of listings is a tuple
            self.assertEqual(type(item), tuple)
            # check that each tuple has a length of 6

        # check that the first tuple is made up of the following:
        # ('Loft in Mission District', '1944564', '2022-004088STR', 'Entire Room', 422, 181)

        # check that the last tuple is made up of the following:
        # ('Guest suite in Mission District', '467507', 'STR-0005349', 'Entire Room', 324, 165)

    def test_output_csv(self):
        # call create_detailed_listing_data on "html_files/search_results.html"
        # and save the result to a variable
        detailed_data = create_detailed_listing_data("html_files/search_results.html")

        # call output_csv() on the variable you saved
        output_csv(detailed_data, "test.csv")

        # read in the csv that you wrote
        csv_lines = []
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.csv'), 'r') as f:
            csv_reader = csv.reader(f)
            for i in csv_reader:
                csv_lines.append(i)

        # check that there are 19 lines in the csv
        self.assertEqual(len(csv_lines), 19)

        # check that the header row is correct

        # check that the next row is Private room in Mission District,23672181,STR-0002892,Private Room,198,109

        # check that the last row is Guest suite in Mission District,50010586,STR-0004717,Entire Room,70,310

    def test_validate_policy_numbers(self):
        # call get_detailed_listing_data on "html_files/search_results.html"
        # and save the result to a variable
        detailed_data = create_detailed_listing_data("html_files/search_results.html")

        # call validate_policy_numbers on the variable created above and save the result as a variable
        invalid_listings = validate_policy_numbers(detailed_data)

        # check that the return value is a list
        self.assertEqual(type(invalid_listings), list)

        # check that the elements in the list are tuples
        # and that there are exactly two element in each tuple

def main (): 
    detailed_data = create_detailed_listing_data("html_files/search_results.html")
    output_csv(detailed_data, "airbnb_dataset.csv")
    non_valid_airbnbs = validate_policy_numbers(detailed_data)

if __name__ == '__main__':
    unittest.main(verbosity=2)
    #main()