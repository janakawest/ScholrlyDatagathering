from Config import Config

# List the required modules
required_modules = ['pandas', 'scholarly', 'openpyxl', 'matplotlib', 'wordcloud']

# Try importing the modules and install the missing ones
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"{module} is not installed. Installing...")
        Config.install_module(module)

# Now import the necessary modules
import pandas as pd
from scholarly import ProxyGenerator, scholarly
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# As a fix for MaxTriesExceededException: Cannot Fetch from Google Scholar
# But this is very temporal, as many times it doesn't work. 
pg = ProxyGenerator()
success = pg.FreeProxies()
scholarly.use_proxy(pg)
#scholarly.search_author_id('<Your Google Scholar ID>')

search_query = scholarly.search_pubs(Config.SEARCHKEY)

# Create an empty DataFrame to store the data
data = pd.DataFrame(columns=['Title', 'Author', 'Abstract', 'Publication URL', 'Year'])

for i in range(Config.NUMRECORDS):
    item = next(search_query)
    if 'title' not in item['bib'] or 'pub_url' not in item or 'url_related_articles' not in item:
        print (f"{item}  is not in the search queary, Continuing...")
        continue
    
    title = item['bib']['title']
    author = item['bib']['author']
    abstract = item['bib']['abstract']
    pub_url = item['pub_url']
    year = item['bib']['pub_year']
    
    # Create a new DataFrame with the data to be added
    new_data = pd.DataFrame({'Title': [title], 'Author': [author], 'Abstract': [abstract],
                             'Publication URL': [pub_url], 'Year': [year]})

    # Concatenate the new DataFrame with the existing DataFrame
    data = pd.concat([data, new_data], ignore_index=True)
# Save the DataFrame to an Excel file
name = Config.SEARCHKEY + '.xlsx'
data.to_excel(name, index=False)

# Generate a year wise summery of the found data
# Categorize the data based on the year and get the counts
year_counts = data['Year'].value_counts()

# Plot the bar graph
plt.figure(num='Number of papers based on the published year')  # Set the figure name
plt.bar(year_counts.index, year_counts.values)
# Add labels and title
plt.xlabel('Year')
plt.ylabel('Count')

# Get all titles together to add to a word cloud
titles = ' '.join (data['Title'].tolist ())

# Create the WordCloud object
wordcloud = WordCloud(width=1600, height=800, max_font_size=175, background_color='white').generate(titles)
# Plot the word cloud
plt.figure(num='Highlighted areas in the titles')  # Set the figure name
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
