import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd

# Scrape top 10 songs from Wikipedia Spotify streaming records
wiki_url = "https://en.wikipedia.org/wiki/List_of_Spotify_streaming_records"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    response = requests.get(wiki_url, headers=headers, timeout=10)
    response.raise_for_status()
    
    # Parse the HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find tables on the page - Wikipedia pages usually have structured tables
    tables = soup.find_all('table', {'class': 'wikitable'})
    
    if tables:
        # The first table usually contains the top streamed songs
        table = tables[0]
        rows = table.find_all('tr')[1:]  # Skip header row
        
        songs_data = []
        for i, row in enumerate(rows[:10]):  # Get top 10
            cols = row.find_all('td')
            if len(cols) >= 3:
                # Extract song name, artist, and streams
                rank = i + 1
                song = cols[1].get_text(strip=True) if len(cols) > 1 else "N/A"
                artist = cols[2].get_text(strip=True) if len(cols) > 2 else "N/A"
                streams = cols[3].get_text(strip=True) if len(cols) > 3 else "N/A"
                
                songs_data.append({
                    'Rank': rank,
                    'Song': song,
                    'Artist': artist,
                    'Streams': streams
                })
        
        if songs_data:
            df = pd.DataFrame(songs_data)
            print("Top 10 Most Streamed Songs on Spotify:\n")
            print(df.to_string(index=False))
        else:
            print("Could not extract song data from the table.")
    else:
        print("No tables found on the page.")
        
except requests.exceptions.RequestException as e:
    print(f"Error fetching the page: {e}")
except Exception as e:
    print(f"Error parsing the page: {e}")

