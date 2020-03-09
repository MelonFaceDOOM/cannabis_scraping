# # classifying new categories
# raw = df['categories'].tolist()
# new_categories = list({c for categories in raw for c in categories})
# category_tuples = []
# with open("categories_flowers.csv", 'r') as f:
    # reader = csv.reader(f)
    # for row in reader:
        # category_tuples.append(row)
# old_categories = [c[0] for c in category_tuples]
# for c in new_categories:
    # c = c.strip().lower()
    # if c not in old_categories:
        # category_tuples.append([c, ''])
# with open("new_categories.csv", "w", newline="") as f:
    # writer = csv.writer(f)
    # writer.writerows(category_tuples)

    
#df_no_weighted_prices = df_flower.loc[set(df_flower.index) - set(df_weighted_prices.index)]


# raw = df_weighted_prices['prices'].map(lambda prices: [price[0] for price in prices]).to_list()
# unique_prices = list({price for prices in raw for price in prices })


# # get all values for the 2nd item in the price tuple
# dollar_values = df_weighted_prices['gram_prices'].apply(lambda x: [p[1] for p in x]).to_list()
# # flatten list of lists and keep unique
# dvs = list({item for row in dollar_values for item in row })