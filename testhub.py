import subprocess

def install_module(module_name):
    subprocess.check_call(["pip", "install", module_name])

# List the required modules
required_modules = ['pandas', 'scihub', 'matplotlib', 'wordcloud']

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
from scihub import SciHub

# Initialize SciHub
sh = SciHub()

# query = ['AI','Breast Cancer','Artificial intelligence','hormonal therapy']
query = 'Breast Cancer Treatment Radiology Radiotherapy Artificial Intelligence AI ML'

# Fetch papers from Sci-Hub
papers = sh.search(query, limit=10)

# Convert papers to DataFrame
data = pd.DataFrame(papers)

# Save DataFrame to Excel
data.to_excel('papers.xlsx', index=False)

# Count papers per year
data['year'] = pd.to_datetime(data['date']).dt.year
year_counts = data['year'].value_counts()

# Plot the bar graph
plt.figure(num='Number of papers based on the published year')  # Set the figure name
plt.bar(year_counts.index, year_counts.values)
# Add labels and title
plt.xlabel('Year')
plt.ylabel('Count')

# Get all titles together to add to a word cloud
titles = ' '.join(data['title'].tolist())

# Create the WordCloud object
wordcloud = WordCloud(width=1600, height=800, max_font_size=175, background_color='white').generate(titles)
# Plot the word cloud
plt.figure(num='Highlighted areas in the titles')  # Set the figure name
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()