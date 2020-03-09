# number of listings
number_of_listings = len(df_flower)

# number of strains
number_of_strains = len(df_flower['strain'].value_counts().keys().tolist())

# most commonly found strains
# drop duplicates to prevent the same strain from being counted twice on one site
df_flower[['strain', 'site']].drop_duplicates()['strain'].value_counts()[:10]

print(f"There were {number_of_strains} strains found in {number_of_listings} cannabis flower listings")
print("The most common strains were:")
print(df_flower[['strain', 'site']].drop_duplicates()['strain'].value_counts()[:10])