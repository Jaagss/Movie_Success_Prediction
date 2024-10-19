import pandas as pd
import ast

# # Load title basics
# title_basics = pd.read_csv('title.basics.tsv/title.basics.tsv', sep='\t', low_memory=False)

# # Load title ratings
# title_ratings = pd.read_csv('title.ratings.tsv/title.ratings.tsv', sep='\t', low_memory=False)

# # Load title principals (cast and crew)
# title_crew = pd.read_csv('title.crew.tsv/title.crew.tsv', sep='\t', low_memory=False)

# # Load name basics (director, actor names)
# name_basics = pd.read_csv('name.basics.tsv/name.basics.tsv', sep='\t', low_memory=False)

# # Step 2: Replace '\N' with None in relevant columns for proper handling
# title_basics.replace({'\\N': None}, inplace=True)
# title_crew.replace({'\\N': None}, inplace=True)
# name_basics.replace({'\\N': None}, inplace=True)

# # Step 3: Convert columns with numeric values to proper types
# title_basics['startYear'] = pd.to_numeric(title_basics['startYear'], errors='coerce')
# title_basics['runtimeMinutes'] = pd.to_numeric(title_basics['runtimeMinutes'], errors='coerce')

# # Step 4: Merge title_basics and title_ratings based on 'tconst'
# merged_data = pd.merge(title_basics, title_ratings, on='tconst', how='inner')

# # Step 5: Merge title_crew with the existing dataset to add director and writer info
# merged_data = pd.merge(merged_data, title_crew[['tconst', 'directors', 'writers']], on='tconst', how='left')

# # Step 6: Split the directors and writers into lists (they are comma-separated in the dataset)
# merged_data['directors'] = merged_data['directors'].str.split(',')
# merged_data['writers'] = merged_data['writers'].str.split(',')

# # Step 7: Explode the 'directors' and 'writers' columns so that each director and writer is in a separate row
# merged_data = merged_data.explode('directors').explode('writers')

# # Step 8: Merge with names_basics to get director and writer names based on 'nconst'
# # Directors
# merged_data = pd.merge(merged_data, name_basics[['nconst', 'primaryName']], 
#                        left_on='directors', right_on='nconst', how='left')
# merged_data.rename(columns={'primaryName': 'director_name'}, inplace=True)

# # Writers
# merged_data = pd.merge(merged_data, name_basics[['nconst', 'primaryName']], 
#                        left_on='writers', right_on='nconst', how='left')
# merged_data.rename(columns={'primaryName': 'writer_name'}, inplace=True)

# # Step 9: Group by 'tconst' to aggregate the director and writer names into lists
# merged_data_grouped = merged_data.groupby('tconst').agg({
#     'primaryTitle': 'first',  # Keep first title
#     'averageRating': 'first',  # Keep the IMDb rating
#     'numVotes': 'first',  # Keep the number of votes
#     'startYear': 'first',  # Keep the start year
#     'runtimeMinutes': 'first',  # Keep the runtime
#     'genres': 'first',  # Keep the genre
#     'director_name': lambda x: ', '.join(x.dropna().unique()),  # Join unique director names
#     'writer_name': lambda x: ', '.join(x.dropna().unique())  # Join unique writer names
# }).reset_index()

# # Step 10: Save the final merged dataset to a CSV file
# merged_data_grouped.to_csv('merged_movie_data_complete.csv', index=False)

# # Step 11: Print the first few rows of the final merged dataset to verify
# print(merged_data_grouped.head())


# data = pd.read_csv('merged_movie_data_with_directors_writers.csv')

# movies_only = data[data['titleType'] == 'movie']

# # Save the filtered dataset to a new CSV file
# movies_only.to_csv('movies_only_dataset.csv', index=False)

# print("Dataset has been updated with only movies.")

name_basics = pd.read_csv('name.basics.tsv/name.basics.tsv', sep='\t', low_memory=False)


movies_only = pd.read_csv('movies_only_dataset.csv', low_memory=False)

nconst_to_name = dict(zip(name_basics['nconst'], name_basics['primaryName']))

def get_name(nconst):
    if pd.isna(nconst) or nconst == '':
        return None
    try:
        nconsts = ast.literal_eval(nconst) if isinstance(nconst, str) and nconst.startswith('[') else nconst.split(',')
    except (ValueError, SyntaxError):
        nconsts = [nconst]
    return [nconst_to_name.get(n.strip(), 'Unknown') for n in nconsts]

movies_only['directors'] = movies_only['directors'].apply(get_name)
movies_only['writers'] = movies_only['writers'].apply(get_name)
movies_only['primary_director'] = movies_only['primary_director'].apply(get_name)

movies_only['directors'] = movies_only['directors'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
movies_only['writers'] = movies_only['writers'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
movies_only['primary_director'] = movies_only['primary_director'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

movies_only.to_csv('movies_only_dataset_with_names.csv', index=False)

print(movies_only.head())

# Load the dataset
df = pd.read_csv('movies_only_dataset_with_names.csv', low_memory=False)

# Remove the 'endYear' column
df = df.drop(columns=['endYear'])

# Save the updated dataset back to a CSV file
df.to_csv('movies_only_dataset_with_names.csv', index=False)

print("endYear column removed successfully!")
