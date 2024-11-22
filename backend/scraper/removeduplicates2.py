import json

def remove_duplicates(articles):
    # Use a set to track unique links
    unique_links = set()
    unique_articles = []

    for article in articles:
        title = article['title']
        link = article['link']

        if link not in unique_links and title != 'Sign in':  # Check for duplicates and filter 'Sign in'
            unique_links.add(link)
            unique_articles.append(article)

    return unique_articles  # Return the unique articles as a list
