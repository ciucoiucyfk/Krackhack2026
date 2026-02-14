from serpapi.google_search import GoogleSearch


def amazon_price(keyword):
    params = {
        "engine": "amazon",
        "amazon_domain": "amazon.in",
        "q": keyword,
        "api_key": "YOUR_API_KEY"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    print(results)

print(amazon_price("iPhone 15"))
