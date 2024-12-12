import requests
import json

# Replace with your GitHub Personal Access Token
GITHUB_TOKEN = "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"

# API headers
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Search query
SEARCH_QUERY = "awesome project in:name,description"

# API base URL
BASE_URL = "https://api.github.com/search/repositories"

# Output file
OUTPUT_FILE = "github_search_results.json"

def fetch_repositories(query, max_pages=5):
    """Fetch repositories from GitHub Search API."""
    all_results = []
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        params = {
            "q": query,
            "per_page": 30,  # Max items per page
            "page": page
        }
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        if response.status_code == 200:
            data = response.json()
            all_results.extend(data.get("items", []))
            if len(data.get("items", [])) < 30:
                break  # Stop if fewer results than a full page are returned
        else:
            print(f"Error: {response.status_code}, {response.json()}\nStopping fetch.")
            break
    return all_results

if __name__ == "__main__":
    # Fetch repositories
    print("Starting search...")
    results = fetch_repositories(SEARCH_QUERY)

    # Save results to a JSON file
    print(f"Saving {len(results)} repositories to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print("Done!")
