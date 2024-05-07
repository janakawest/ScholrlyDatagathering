import subprocess

def install_module(module_name):
    subprocess.check_call(["pip", "install", module_name])

# List the required modules
required_modules = ['pandas', 'habanero', 'matplotlib', 'wordcloud']

# Try importing the modules and install the missing ones
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"{module} is not installed. Installing...")
        install_module(module)

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from habanero import Crossref

def fetch_crossref_data(query):
    cr = Crossref()
    papers = cr.works(query=query, limit=100)  # Adjust the limit as needed
    return papers

def process_crossref_data(papers):
    data = {'authors': [], 'doi': [], 'title': [], 'abstract': [], 'year': []}
    for paper in papers['message']['items']:
        authors = []
        for author in paper.get('author', []):
            given_name = author.get('given', '')
            family_name = author.get('family', '')
            if given_name and family_name:
                authors.append(given_name + ' ' + family_name)
            else:
                authors.append('Unknown')
        data['authors'].append(', '.join(authors))
        data['doi'].append(paper.get('DOI', ''))
        data['title'].append(paper.get('title', ['Untitled'])[0])
        data['abstract'].append(paper.get('abstract', ''))
        if 'published-print' in paper:
            data['year'].append(int(paper['published-print']['date-parts'][0][0]))
        elif 'published-online' in paper:
            data['year'].append(int(paper['published-online']['date-parts'][0][0]))
        else:
            data['year'].append(None)
    return data

# query = 'breast cancer AND radiology AND artificial intelligence'
query = 'breast cancer AND radiology AND artificial intelligence'

# Fetch data from Crossref
papers = fetch_crossref_data(query)

# Process the data
data = process_crossref_data(papers)

# Create DataFrame
df = pd.DataFrame(data)

# Save the data to an XLS file
df.to_excel('sheet_test.xlsx', index=False, columns=['authors', 'doi', 'title', 'abstract', 'year'])

# Plot the number of papers based on the published year
plt.figure(num='Number of papers based on the published year')
df['year'].value_counts().sort_index().plot(kind='bar')
plt.xlabel('Year')
plt.ylabel('Count')
plt.show()

# Get all titles together to add to a word cloud
titles_text = ' '.join(df['title'])

# Create the WordCloud object
wordcloud = WordCloud(width=1600, height=800, max_font_size=175, background_color='white').generate(titles_text)

# Plot the word cloud
plt.figure(num='Highlighted areas in the titles')
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
