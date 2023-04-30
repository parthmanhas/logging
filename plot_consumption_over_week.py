import matplotlib.pyplot as plt

def plot_consumption_over_last_week(last_7_days_description_df_combined_categories, today = None, save_image = False):

    x = list(last_7_days_description_df_combined_categories['food'].keys())
    y = [x for x in last_7_days_description_df_combined_categories['food'].values()]

    # add cigarette consumption
    x.extend(list(last_7_days_description_df_combined_categories['smoking'].keys()))
    y.append(last_7_days_description_df_combined_categories['smoking']['cigarette'])

    plt.figure(figsize=(10, 10))
    plt.bar(x, y, width=0.5)

    plt.xticks(rotation=90)

    plt.title('Consumptions over last week')
    plt.ylabel('Count')
    
    if not save_image:
        plt.show()

    if save_image and today is not None:
        plt.savefig(f"last_7_days/{today.strftime('%Y-%m-%d')}-consumption.png")
    else:
        print('Today is missing')
