# * A list in Python that contains the names of columns for a dataframe.
Columns_springer_info = ['Href', 'Title', 'Subtitle', 'Authors', 'Publication_title', 'Year', 'DOI']
Columns_springer_info_lower = [i.lower() for i in Columns_springer_info]

print(Columns_springer_info_lower)