#!/usr/bin/python3
"""
Contains the number_of_subscribers function
"""

import requests

def count_words(subreddit, word_list, after=None, word_counts=None):
    if word_counts is None:
        word_counts = {}

    # Base case: if word_list is empty, print the sorted word counts
    if not word_list:
        sorted_counts = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(f"{word.lower()}: {count}")
        return

    # Get the first keyword from the list
    keyword = word_list[0].lower()

    # URL for the Reddit API endpoint to get hot articles
    url = f"https://www.reddit.com/r/{subreddit}/hot/.json"

    # Set a custom User-Agent header to identify your script (Reddit API requirement)
    headers = {"User-Agent": "MyRedditBot/1.0"}

    # Parameters for the API request
    params = {"limit": 100, "after": after}

    # Make the GET request to the Reddit API
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

        # Iterate through the articles and count occurrences of the keyword
        for post in data["data"]["children"]:
            title = post["data"]["title"].lower()
            word_counts[keyword] = word_counts.get(keyword, 0) + title.count(keyword)

        # If there are more pages of results, make a recursive call
        after = data["data"]["after"]
        if after:
            count_words(subreddit, word_list, after, word_counts)
        else:
            # Move to the next keyword in the list
            count_words(subreddit, word_list[1:], None, word_counts)
    else:
        print("Failed to retrieve data from Reddit API.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        keywords = [x for x in sys.argv[2].split()]
        count_words(subreddit, keywords)

