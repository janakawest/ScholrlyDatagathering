from Config import Config

# List the required modules
required_modules = ['pandas', 'scholarly', 'openpyxl']

# Try importing the modules and install the missing ones
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"{module} is not installed. Installing...")
        Config.install_module(module)

# Now import the necessary modules
import pandas as pd
from scholarly import scholarly

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
data.to_excel('papers.xlsx', index=False)