import pandas as pd

# Load the datasets from CSV files
# tmdb_df = pd.read_csv('archive/tmdb_movies.csv', low_memory=False)
# movies_df = pd.read_csv('movies_only_dataset_with_names.csv', low_memory=False)

# # Merge the datasets based on imdb_id (from tmdb) and tconst (from movies_only)
# merged_df = pd.merge(tmdb_df, movies_df[['tconst', 'directors', 'writers', 'primary_director']], 
#                      left_on='imdb_id', right_on='tconst', how='left')

# # Drop the tconst column as it's now redundant
# merged_df = merged_df.drop(columns=['tconst'])

# # Save the merged dataset to a new CSV file
# merged_df.to_csv('merged_dataset.csv', index=False)

# # Display the first few rows of the merged dataset
# print(merged_df.head())

# merged_df = pd.read_csv('merged_dataset.csv', low_memory=False)

# columns_to_drop = ['backdrop_path', 'homepage', 'poster_path', 'tagline', 'overview']
# merged_df = merged_df.drop(columns=columns_to_drop)

# # Save the cleaned merged dataset to a new CSV file
# merged_df.to_csv('merged_dataset_cleaned.csv', index=False)

merged_df = pd.read_csv('merged_dataset_cleaned.csv', low_memory=False)

filtered_df = merged_df[(merged_df['budget'] > 0) & (merged_df['revenue'] > 0)]

# Count the number of such movies
count_movies = filtered_df.shape[0]
print(f'Number of movies with both budget and revenue greater than 0: {count_movies}')

# Check for null values in the filtered dataset
null_values = filtered_df.isnull().sum()
print("\nNull values in columns:")
print(null_values)
