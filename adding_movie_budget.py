import pandas as pd

# Load the two datasets
movies_only = pd.read_csv('movies_only_dataset_with_names.csv', low_memory=False)  # First dataset
movies_metadata = pd.read_csv('movies_metadata.csv', low_memory=False)  # Second dataset with budget, revenue, etc.

# Merge the datasets on 'tconst' and 'imdb_id' with a left join
# Merge the datasets on the common column (e.g., 'tconst' and 'imdb_id')
merged_df = pd.merge(movies_only, movies_metadata, left_on='tconst', right_on='imdb_id', how='inner')

print("Available columns after merge:", merged_df.columns)


# Extract only the desired columns
final_columns = [
    'tconst', 'titleType', 'primaryTitle', 'isAdult', 'startYear', 'runtimeMinutes',
    'genres_x', 
    'averageRating', 'numVotes', 'directors', 'writers', 'primary_director', 
    'budget', 'revenue', 'original_language', 'production_companies', 'production_countries'
]

# Keep only the final columns in the merged dataset
final_df = merged_df[final_columns]

# Save the final dataset to a new CSV file
final_df.to_csv('final_movies_dataset.csv', index=False)

print("Final dataset created with selected columns.")