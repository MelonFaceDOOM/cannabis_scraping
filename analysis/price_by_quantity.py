from scraping.build_dataframe import merge_all_parsed
from cleaning.categorization import extract_flower
from cleaning.clean_weight_price import price_tuple_to_grams
from cleaning.flower_cleaning import clean_name, specific_replacements, standardize_og_kush
import matplotlib.pyplot as plt


def main():
    df = merge_all_parsed()
    df = extract_flower(df)

    df['strain'] = df['name'].apply(clean_name)
    df['strain'] = df['strain'].apply(specific_replacements)
    df['strain'] = df['strain'].apply(standardize_og_kush)

    df['gram_prices'] = df['prices'].apply(price_tuple_to_grams)

    legal_sites = ["ocs"]
    df_legal = df[df['site'].isin(legal_sites)]
    df_illegal = df.loc[set(df.index) - set(df_legal.index)]

    # # get list of unique weight values
    # weights = df_flower['gram_prices'].apply(lambda x: [p[0] for p in x]).to_list()
    # sorted(list({item for row in weights for item in row }))

    df_legal = calc_price_per_gram(df_legal)
    df_illegal = calc_price_per_gram(df_illegal)

    ppg5_legal = df_legal['ppg_5'].mean()
    ppg15_legal = df_legal['ppg_15'].mean()
    ppg28_legal = df_legal['ppg_28'].mean()
    ppgbulk_legal = df_legal['ppg_bulk'].mean()

    ppg5_illegal = df_illegal['ppg_5'].mean()
    ppg15_illegal = df_illegal['ppg_15'].mean()
    ppg28_illegal = df_illegal['ppg_28'].mean()
    ppgbulk_illegal = df_illegal['ppg_bulk'].mean()

    # TODO: check the weight values in each price category
    #  (i.e. is ppg_28 purely 28g, or are there some between 14 and 28g)

    txt_output = []
    txt_output.append(f'Average price 5g or less (legal - illegal): {ppg5_legal:0.2f} - {ppg5_illegal:0.2f}')
    txt_output.append(f'Average price for 5-15g (legal - illegal): {ppg15_legal:0.2f} - {ppg15_illegal:0.2f}')
    txt_output.append(f'Average price for 15-28g (legal - illegal): {ppg28_legal:0.2f} - {ppg28_illegal:0.2f}')
    txt_output.append(f'Average price for >28g (legal - illegal): {ppgbulk_legal:0.2f} - {ppgbulk_illegal:0.2f}')

    # cheapest listings
    # df_legal.sort_values(by=['ppg_3.5']

    count_5_i = df_illegal['ppg_5'].count()
    count_15_i = df_illegal['ppg_15'].count()
    count_28_i = df_illegal['ppg_28'].count()
    count_bulk_i = df_illegal['ppg_bulk'].count()

    count_5_l = df_legal['ppg_5'].count()
    count_15_l = df_legal['ppg_15'].count()
    count_28_l = df_legal['ppg_28'].count()
    count_bulk_l = df_legal['ppg_bulk'].count()

    txt_output.append(f'there were {count_5_i} illegal listings under 5g')
    txt_output.append(f'there were {count_15_i} illegal listings at 5-15g')
    txt_output.append(f'there were {count_28_i} illegal listings at 15-28g')
    txt_output.append(f'there were {count_bulk_i} illegal listings over 28g')

    txt_output.append(f'there were {count_5_l} legal listings under 5g')
    txt_output.append(f'there were {count_15_l} legal listings at 5-15g')
    txt_output.append(f'there were {count_28_l} legal listings at 15-28g')
    txt_output.append(f'there were {count_bulk_l} legal listings over 28g')

    save_hist(df_legal['ppg_5'], '_l', 1, 25)
    save_hist(df_legal['ppg_15'], '_l')
    save_hist(df_legal['ppg_28'], '_l')
    save_hist(df_legal['ppg_bulk'], '_l')
    save_hist(df_illegal['ppg_5'], '_i')
    save_hist(df_illegal['ppg_15'], '_i')
    save_hist(df_illegal['ppg_28'], '_i')
    save_hist(df_illegal['ppg_bulk'], '_i', 1, 7)

    legal_strains = df_legal['strain'].drop_duplicates().tolist()
    df_common_illegal = df_illegal[df_illegal['strain'].isin(legal_strains)][
        ['strain', 'ppg_5', 'ppg_15', 'ppg_28', 'ppg_bulk']]
    illegal_strains = df_common_illegal['strain'].drop_duplicates().tolist()
    df_common_legal = df_legal[df_legal['strain'].isin(illegal_strains)]

    df_common_illegal = df_common_illegal.groupby('strain').mean().reset_index()
    df_common_legal = df_common_legal.groupby('strain').mean().reset_index()

    df_common_strains = df_common_illegal.merge(df_common_legal, on='strain', suffixes=['_i', '_l'])

    txt_output.append(
        f"There were {len(df_common_strains)} strains from OCS.ca that were also found on the illegal market")
    df_illegal_cheaper = df_common_strains[df_common_strains['ppg_5_i'] < df_common_strains['ppg_5_l']]

    #len(df_illegal_cheaper)
    df_illegal_not_cheaper = df_common_strains.loc[set(df_common_strains.index) - set(df_illegal_cheaper.index)]

    df_common_strains[['ppg_5_i', 'ppg_5_l']].plot.bar(figsize=(20, 8))
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel('')
    plt.ylabel('Price ($CAD)', fontsize=18)
    plt.legend(('Illegal, 5 grams or less', 'Legal, 5 grams or less'), fontsize=18)
    plt.savefig("strain_comp.png", bbox_inches='tight', pad_inches=0)
    plt.close()

    with open("price_by_quality_info.txt", "w") as f:
        for line in txt_output:
            f.write(line)
            f.write('\n')


def calc_price_per_gram(df):
    """Add four different price-per-gram columns to df"""
    def _price_per_gram(prices, min_weight, max_weight):
        """ Returns the average price-per gram of all price tuples within the min/max provided.

        Arguments:
        prices -- list of tuples of weight and price (i.e. [("1g", "$5")("5g","$20")]
        min_weight -- the minimum weight to be included
        max_weight -- the maximum weight to be included"""

        price_tuples_within_range = []
        for price in prices:
            if price[0] >= min_weight and price[0] <= max_weight:
                price_tuples_within_range.append(price[1]/price[0])
        if not price_tuples_within_range:
            return float('nan')
        return sum(price_tuples_within_range)/len(price_tuples_within_range)
    
    df['ppg_5'] = df['gram_prices'].apply(_price_per_gram, min_weight=0, max_weight=5)
    df['ppg_15'] = df['gram_prices'].apply(_price_per_gram, min_weight=5.1, max_weight=15)
    df['ppg_28'] = df['gram_prices'].apply(_price_per_gram, min_weight=15.1, max_weight=28)
    df['ppg_bulk'] = df['gram_prices'].apply(_price_per_gram, min_weight=28.1, max_weight=1000)
    
    return df


def save_hist(df_column, suffix=None, start=1, end=15):
    """Save histogram of distributions of values within provided dataframe column"""
    df_column.hist(bins=20, facecolor='gray', ec='black', range=[start, end], figsize=(12, 8), grid=False)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel('Price ($CAD)', fontsize=18)
    plt.ylabel('Number of Listings', fontsize=18)
    plt.savefig(f"{df_column.name}{suffix}.png", bbox_inches='tight', pad_inches = 0)
    plt.close()


if __name__ == "__main__":
    main()
