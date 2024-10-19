import pandas as pd

# Load the dataset
df = pd.read_csv('final_movies_dataset.csv', low_memory=False)

# Total number of movies in the dataset
total_movies = df.shape[0]
print(f'Total number of movies in the dataset: {total_movies}')

# Count movies with non-null budget and revenue
count_with_budget = df['budget'].notna().sum()
count_with_revenue = df['revenue'].notna().sum()
print(f'Total movies with budget: {count_with_budget}')
print(f'Total movies with revenue: {count_with_revenue}')

# Count movies with valid budget and revenue
valid_budget_revenue_count = df[(df['budget'] > 0) & (df['revenue'] > 0)].shape[0]
print(f'Count of movies with valid budget and revenue: {valid_budget_revenue_count}')

# Count movies with zero budget but valid revenue
zero_budget_valid_revenue_count = df[(df['budget'] == 0) & (df['revenue'] > 0)].shape[0]
print(f'Number of movies with zero budget but valid revenue: {zero_budget_valid_revenue_count}')

# Count movies with valid budget but zero revenue
valid_budget_zero_revenue_count = df[(df['budget'] > 0) & (df['revenue'] == 0)].shape[0]
print(f'Number of movies with valid budget but zero revenue: {valid_budget_zero_revenue_count}')

# Unique values in budget and revenue columns for inspection
print(f'Unique values in budget: {df["budget"].unique()}')
print(f'Unique values in revenue: {df["revenue"].unique()}')

# Check the data types of budget and revenue
print(df[['budget', 'revenue']].dtypes)
