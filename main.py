#   Project 1 : Main
# Import sys to access command-line arguments and exit codes
import sys

# Import the function that handles Wikipedia API requests
from wikipedia_api import fetch_revisions

# Define the main function that runs when the script is executed
def main():
    # Checks if the user provided an article name as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: No article name provided.")
        sys.exit(1) # Exit with error code 1 for missing input

    article_name = sys.argv[1]

    try:
        # Call the function to fetch revision data from Wikipedia
        result = fetch_revisions(article_name)

        # If the article was redirected, print the new title
        if result.get("redirected"):
            print(f"Redirected to: {result['title']}")

        # Loop through each revision and print the timestamp and print the timestamp and username
        for rev in result["revisions"]:
            print(f"{rev['timestamp']} {rev['user']}")

        # Exit with success code 0
        sys.exit(0)

    except ConnectionError as e:
        print(f"Network error: {e}")
        sys.exit(3) # ERxit with error code 3 for network issues

# Run the main function only if this file is executed directly
if __name__ == "__main__":
    main()