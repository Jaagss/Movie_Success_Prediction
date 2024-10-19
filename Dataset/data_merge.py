import pandas as pd
import numpy as np

def clean_gross_column(column):
    """Clean and convert gross columns to numeric."""
    column = column.astype(str)
    column = column.replace('Gross Unknown', pd.NA)
    column = column.str.replace('[$,]', '', regex=True)
    column = column.str.replace('M', 'e6', regex=False).str.replace('K', 'e3', regex=False)
    return pd.to_numeric(column, errors='coerce')

def clean_and_standardize_data(df):
    """Clean the merged DataFrame."""
    # Remove unwanted columns
    cols_to_drop = ['budget_y', 'genre_y'] + [
        "rating", "released", "country",  "company",
        "plot_keywords", "language", "aspect_ratio", "movie_facebook_likes", "movie_imdb_link",
        "num_user_for_reviews", "num_critic_for_reviews", "duration", "color", "actor_3_name",
        "cast_total_facebook_likes", "title_year",  "facenumber_in_poster",
        "content_rating", "director_facebook_likes", "actor_3_facebook_likes", "actor_2_facebook_likes",
        "actor_1_facebook_likes", "Censor", "side_genre", "IMDB_ID", "Released",
        "Production", "Language", "Plot", "MetaCritic", "Rotten Tomatoes",
        "Type", "Movie_ID", "Crew", "Studios", "Keywords", "Languages", "Countries", "Filming_Location", "ListOfCertificate"
    ]
    df = df.drop(cols_to_drop, axis=1, errors='ignore')  # Use drop and create a new DataFrame
    
    # Handle missing values and standardize movie names
    df.fillna({'budget_2': 0, 'cast_6': 'Unknown', 'genre_4': 'Unknown'}, inplace=True)
    df['movie_name'] = df['movie_name'].str.replace('&apos;', "'", regex=False)

    # Convert budget columns to numeric
    df['budget_2'] = pd.to_numeric(df['budget_2'], errors='coerce')

    return df

def merge_datasets():
    """Read and merge datasets."""
    # Read datasets
    data_files = [
        "data/movies.csv", 
        "data/metadata.csv", 
        "data/IMDB 5000+.csv", 
        "data/moviedatasetomdbsorted.csv", 
        "data/data_joined.csv"
    ]
    
    # Read and select relevant columns
    dataframes = []
    selected_columns = [
        {'movie_name': 'movie_name', 'score': 'imdb_rating_1', 'star': 'cast_1', 'budget': 'budget', 'gross': 'gross'},
        {'movie_name': 'movie_name', 'genres': 'genre', 'imdb_score': 'imdb_rating_2', 'gross': 'gross_2', 'director_name': 'director', 'actor_1_name': 'cast_2', 'actor_2_name': 'cast_3'},
        {'movie_name': 'movie_name', 'Total_Gross': 'gross_3', 'main_genre': 'genre_2', 'Rating': 'imdb_rating_3', 'Actors': 'cast_4'},
        {'movie_name': 'movie_name', 'Actors': 'cast_5', 'Genre': 'genre_3', 'IMDB_Rating': 'imdb_rating_4', 'Box_Office': 'gross_4'},
        {'movie_name': 'movie_name', 'Gross_worldwide': 'gross_5', 'Genre': 'genre_4', 'Rating': 'imdb_rating_5', 'Cast': 'cast_6', 'Budget': 'budget_2'}
    ]
    
    for i, file in enumerate(data_files):
        df = pd.read_csv(file, encoding='ISO-8859-1')
        df = df[list(selected_columns[i].keys())].copy()  # Use .copy() to ensure it's a separate DataFrame
        df.rename(columns=selected_columns[i], inplace=True)
        dataframes.append(df)

    # Merge DataFrames
    merged_data = dataframes[0]
    for df in dataframes[1:]:
        merged_data = pd.merge(merged_data, df, on='movie_name', how='outer')

    return merged_data

def aggregate_movies(df):
    """Aggregate movie data by taking the mean of numeric columns and joining non-numeric columns."""
    
    # Combine IMDb ratings
    df['imdb'] = df[['imdb_rating_1', 'imdb_rating_2', 'imdb_rating_3', 'imdb_rating_4', 'imdb_rating_5']].mean(axis=1)

    # Drop individual IMDb rating columns
    df = df.drop(columns=['imdb_rating_1', 'imdb_rating_2', 'imdb_rating_3', 'imdb_rating_4', 'imdb_rating_5'], errors='ignore')

    # Create maximum budget and gross columns
    df['max_budget'] = df[['budget', 'budget_2']].max(axis=1)
    df['max_gross'] = df[['gross', 'gross_2', 'gross_3', 'gross_4', 'gross_5']].max(axis=1)

    # Define aggregation functions
    aggregation_functions = {
        'imdb': 'mean',
        'max_budget': 'mean',
        'max_gross': 'mean',
        'cast_1': lambda x: ', '.join(x.dropna().unique()),  # Join unique cast names
        'cast_2': lambda x: ', '.join(x.dropna().unique()),
        'cast_3': lambda x: ', '.join(x.dropna().unique()),
        'cast_4': lambda x: ', '.join(x.dropna().unique()),
        'cast_5': lambda x: ', '.join(x.dropna().unique()),
        'cast_6': lambda x: ', '.join(x.dropna().unique()),
        'genre': lambda x: ', '.join(x.dropna().unique()),  # Join unique genres
        'genre_2': lambda x: ', '.join(x.dropna().unique()),
        'genre_3': lambda x: ', '.join(x.dropna().unique()),
        'genre_4': lambda x: ', '.join(x.dropna().unique()),
    }

    # Group by movie_name and apply aggregation
    aggregated_data = df.groupby('movie_name', as_index=False).agg(aggregation_functions)

    return aggregated_data

def main():
    # Merge datasets
    merged_data = merge_datasets()
    print("Merged DataFrame shape:", merged_data.shape)
    print("Merged DataFrame columns:", merged_data.columns)

    # Clean gross columns
    gross_columns = ['gross', 'gross_2', 'gross_3', 'gross_4', 'gross_5']
    for col in gross_columns:
        merged_data[col] = clean_gross_column(merged_data[col])

    merged_data[gross_columns] = merged_data[gross_columns].fillna(0)

    # Clean and standardize data
    cleaned_data = clean_and_standardize_data(merged_data)
    
    # Remove rows where 'movie_name' and 'budget_2' are both NaN
    cleaned_data = cleaned_data.dropna(subset=['movie_name', 'budget_2'], how='all')

    # Aggregate movie data
    aggregated_data = aggregate_movies(cleaned_data)

    # Remove movies with 0 budget and 0 gross
    aggregated_data = aggregated_data[
        (aggregated_data['max_budget'] > 0) | (aggregated_data['max_gross'] > 0)
    ]

    # Remove movies with no budget information
    aggregated_data = aggregated_data[aggregated_data['max_budget'] > 0]


    # Print the shape of the aggregated DataFrame
    print("Aggregated DataFrame shape:", aggregated_data.shape)

    # Optionally, check the first few rows of the aggregated DataFrame
    print(aggregated_data.head())

    # Print summary of aggregated data
    print(aggregated_data.describe(include='all'))

    # Write aggregated data to a CSV file
    aggregated_data.to_csv('aggregated_movies_data.csv', index=False)
    print("Aggregated data saved to 'aggregated_movies_data.csv'.")

if __name__ == "__main__":
    main()
