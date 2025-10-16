import requests # Used to make HTTP requests to the Wikipedia API

def fetch_revisions(article_name):
    # Define the Wikipedia API endpoint
    url = "https://en.wikipedia.org/w/api.php"
    
    # Set up the parameters for the API request
    params = {
        "action": "query", # We're querying data
        "format": "json", # We want the response in JSON format
        "prop": "revisions", # We want revision information
        "titles": article_name, # The title of the article to fetch
        "rvprop": "timestamp|user", # We want the timestamp and user of each
        "rvlimit": "30", # Limit to the last 30 revisions
        "redirects": "" # Follow redirects if the article name changes
    }

    try:
        # Send thee GET request to Wikipedia
        response = requests.get(url, params = params)
        response.raise_for_status() # Raise an error if the request failed

        # Parse the JSON response
        data = response.json()

        # Extract the 'query' section from the response
        query = data.get("query", {})
        pages = query.get("pages", ())

        # If no pages were returned, the article dosn't exist
        if not pages:
            raise ValueError("No Wikipedia page found.")
        
        # Get the first page object ( there should only be one )
        page = next(iter(pages.values()))

        # If the page is marked as missing, raise an error
        if "missing" in page:
            raise ValueError("Wikipedia page not found.")
        
        # Get the list of revisions (timestamp and user)
        revisions = page.get("revisions", [])

        # Get the final article title (after redirect, if any)
        title = page.get("title", article_name)

        # Check if the query involved a redirect
        redirected = "redirects" in query

        # Return the parsed data in a structured format
        return {
            "title": title,
            "redirected": redirected,
            "revisions": revisions
        }
    
    except requests.exceptions.RequestException as e:
        # Raise a connection error if the request failed
        raise ConnectionError("Unable to connect to Wikipedia.") from e