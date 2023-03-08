import requests
import json


# Replace this with the URL of the page you want to scrape
url = "https://www.trendyol.com/kb-koycegiz-bali/cam-bali-850-gr-cam-kavanoz-p-33311761"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the JSON-LD script tag containing the review data
script_tag = soup.find("script", {"type": "application/ld+json"})
json_data = json.loads(script_tag.string)

# Parse the JSON-LD data using the JsonLdParser library


# Loop through each review and extract the relevant data
for review in reviews:
    rating = review["reviewRating"]["ratingValue"]
    text = review["reviewBody"]
    author = review["author"]["name"]
    print(f"Rating: {rating}, Text: {text}, Author: {author}")
