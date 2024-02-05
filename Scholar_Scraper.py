"""
/*******************************************************
 * Copyright (c) 2024 
 
 * Authors:
 *   - Janaka Wijekoon
 *   - Rashini Liyanarachchi
 *******************************************************/

"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def GetGoogleScholarData(query,num_pages):
    URL = 'https://scholar.google.com/scholar'
    results = []
    for page in range(0, num_pages):
        params = {
            'q': query,
            'hl': 'en',
            'start': page * 10  # Each page displays 10 results
        }
        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}
        response = requests.get(URL, params=params, headers=headers)
       
        #response = requests.get(URL, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')
       
        for item in soup.select('.gs_r'):
            title = item.select_one('.gs_rt a')
            abstract = item.select_one('.gs_rs')
            journal = item.select_one('.gs_a')

            title_text = title.get_text() if title else 'Title not available'
            abstract_text = abstract.get_text() if abstract else 'Abstract not available'
        
            if journal and title_text != 'Title not available':
                bib_text = journal.get_text()
                publisher_text = bib_text.split('-')[-1].strip()
                authors_text = bib_text.split('-')[0].strip()
                journal_text = bib_text.split('-')[1].strip()

            else:
                journal_text = 'Journal information not available'
                publisher_text = 'Publisher not available'
                authors_text = 'Authors information not available'

            results.append({
                'Title': title_text,
                'Abstract': abstract_text,
                'Journal': journal_text,
                'Publisher': publisher_text,
                'Authors': authors_text
            })
    df = pd.DataFrame(results)
    df.to_excel('Sheet_test_scholar_scraper.xlsx', index=False)
    # WORDCLOUD FOR TITLES
    titles = ' '.join (df['Title'].tolist ())
    # Create the WordCloud object
    wordcloud = WordCloud(width=1600, height=800, max_font_size=175, background_color='white').generate(titles)
    # Plot the word cloud
    plt.figure(num='Highlighted areas in the titles')  
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    ## WORDCLOUD FOR PUBLISHERS
    publishers = ' '.join (df['Publisher'].tolist ())
    # Create the WordCloud object
    wordcloud = WordCloud(width=1600, height=800, max_font_size=175, background_color='white').generate(publishers)
    # Plot the word cloud
    plt.figure(num='Publishers accessed')  
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


    return results

if __name__ == '__main__':
    matchedData = GetGoogleScholarData("(Breast Cancer Treatment) AND (Radiology OR Radiotherapy) AND (Artificial Intelligence OR AI OR ML)", 10)