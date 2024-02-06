"""
/*******************************************************
 * Copyright (c) 2024 
 
 * Authors:
 *   - Janaka Wijekoon
 *   - Rashini Liyanarachchi
 *******************************************************/

"""

import subprocess

def install_module(module_name):
    subprocess.check_call(["pip", "install", module_name])
# List the required modules

required_modules = ['pandas', 'paperscraper', 'matplotlib', 'wordcloud']

# Try importing the modules and install the missing ones
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"{module} is not installed. Installing...")
        install_module(module)


from paperscraper.pubmed import get_and_dump_pubmed_papers
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# query = ['AI','Breast Cancer','Artificial intelligence','hormonal therapy']
query = ['(Breast Cancer Treatment) AND (Radiology OR Radiotherapy) AND (Artificial Intelligence OR AI OR ML)']
get_and_dump_pubmed_papers(query, output_filepath='sheet_test.jsonl')


# Read the data from the JSONL file
data = pd.read_json('sheet_test.jsonl', lines=True)

# Save the data to an XLS file
data.to_excel('sheet_test.xlsx', index=False)
print(data)

data['year'] = pd.to_datetime(data['date']).dt.year

year_counts = data['year'].value_counts()

# Plot the bar graph
plt.figure(num='Number of papers based on the published year')  # Set the figure name
plt.bar(year_counts.index, year_counts.values)
# Add labels and title
plt.xlabel('Year')
plt.ylabel('Count')

# Get all titles together to add to a word cloud
titles = ' '.join (data['title'].tolist ())

# Create the WordCloud object
wordcloud = WordCloud(width=1600, height=800, max_font_size=175, background_color='white').generate(titles)
# Plot the word cloud
plt.figure(num='Highlighted areas in the titles')  # Set the figure name
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()



