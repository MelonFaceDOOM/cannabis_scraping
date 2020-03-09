def strain_summary(df, strain):
    df = df[df['strain']==strain]
    if len(df) == 0:
        return 'strain not found'
    
    eighth_or_less = []
    quarter_or_less = []
    half_or_less = []
    ounce_or_less = []
    bulk = []
    
    for i, row in df.iterrows():
        for price_tuple in row['gram_prices']:
            if price_tuple[0] <= 3.5:
                eighth_or_less.append(price_tuple)
            elif price_tuple[0] <= 7:
                quarter_or_less.append(price_tuple)
            elif price_tuple[0] <= 14:
                half_or_less.append(price_tuple)
            elif price_tuple[0] <= 28:
                ounce_or_less.append(price_tuple)
            elif price_tuple[0] > 28:
                bulk.append(price_tuple)
                
    def _average(price_tuples):
        prices_per_gram = [p[1]/p[0] for p in price_tuples]
        try:
            price_per_gram = sum(prices_per_gram)/len(prices_per_gram)
        except:
            return float('nan')
        price_per_gram = float("{0:.2f}".format(price_per_gram))
        return price_per_gram
    
    sites = df['site'].tolist()
    print(strain)
    print("found in the following:")
    for site in sites:
        print(f"  - {site}")
    print("\n")
    print("average prices across sites:")
    print(f"3.5g or less: ${_average(eighth_or_less)} per gram" if eighth_or_less else "")
    print(f"3.5-7g:       ${_average(quarter_or_less)} per gram" if quarter_or_less else "")
    print(f"7-14g:        ${_average(half_or_less)} per gram" if half_or_less else "")
    print(f"14-28g:       ${_average(ounce_or_less)} per gram" if ounce_or_less else "")
    print(f"28g+:         ${_average(bulk)} per gram" if bulk else "")
