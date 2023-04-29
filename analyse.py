import json
import pandas as pd
from datetime import date
from datetime import timedelta
from collections import Counter
import re

from plot_consumption_over_week import plot_consumption_over_last_week

# in minutes
POMO_TIME = 20

# final df will contain only CATEGORIES_MAPPING.values()
with open('CATEGORIES_MAPPING.json') as f:
    CATEGORIES_MAPPING = json.load(f)

UNIQUE_CATEGORIES = list(set(CATEGORIES_MAPPING.values()))

# will give fro example {'food': {'last seven days combined data'}} for all CATEGORIES_MAPPING.values()
def initialize_last_7_days_description_df_combined_categories():
    for category in CATEGORIES_MAPPING.values():
        last_7_days_description_df_combined_categories[category] = []


def initialize_stats_dict():
    last_7_days_stats = {}
    last_3_days_stats = {}

    for key in list(CATEGORIES_MAPPING.values()):
        last_7_days_stats[key] = []
        last_3_days_stats[key] = []
        for i in range(7):
            last_7_days_stats[key].append(
                {((today - timedelta(days=i+1)).strftime('%Y-%m-%d')): ''})

        for i in range(3):
            last_3_days_stats[key].append(
                {((today - timedelta(days=i+1)).strftime('%Y-%m-%d')): ''})


def update_categories(action):
    return CATEGORIES_MAPPING[action]

# convert ['daal + 2 roti'] -> convert_item_count(['daal', '2 roti']) -> ['daal', 'roti', 'roti']
def clean_combined(combined):
    arr = []
    for item in combined:
        parts = item.split(' + ')
        parts = map(convert_item_count, parts)
        flat_parts = [item for sublist in parts for item in (
            sublist if isinstance(sublist, list) else [sublist])]
        arr.extend(flat_parts)
    return arr

# convert '2 roti' -> ['roti', 'roti']
# return 'moong hari daal' as it is
def convert_item_count(str):
    if 'am' in str or 'AM' in str or 'pm' in str or 'PM' in str:
        return str
    regex = re.compile(r'\d{1,2} *')
    match = regex.search(str)
    if match:
        count = match.group(0).split(' ')[0]
        str = str.split(match.group(0))
        ret = []
        for i in range(int(count)):
            ret.append(str[1])
        return ret
    else:
        return str


def combine_foods(foods_arr):
    # print('## combine_foods start')
    foods_dict = {}
    updated_foods = []
    for food in foods_arr:
        if food not in foods_dict:
            foods_dict[food] = 1
        else:
            foods_dict[food] += 1

    for food in foods_dict:
        if foods_dict[food] > 1:
            updated_foods.append(f'{foods_dict[food]} {food}')
        else:
            updated_foods.append(f'{food}')

    return updated_foods


with open(r'C:\Users\parth\Desktop\self_logging\example_response_sheet_get.json', 'r') as f:
    # Load the JSON data into a Python object
    data = json.load(f)
    data = data['values']
    analysis_df = pd.DataFrame(columns=['datetime', 'action', 'description'])
    for row in data:
        # skip heading
        if 'Date' in row[0]:
            continue
        analysis_df = pd.concat([analysis_df, pd.DataFrame(
            {'datetime': [row[0]], 'action': [row[1]], 'description': [row[2]]})])
    analysis_df['datetime'] = pd.to_datetime(
        analysis_df['datetime'], format='%Y-%m-%d %H:%M:%S')
#     analysis_df['datetime'] = analysis_df['datetime'].dt.tz_localize('UTC')
#     analysis_df['datetime'] = analysis_df['datetime'].dt.tz_convert('Asia/Kolkata')
    analysis_df['date'] = analysis_df['datetime'].dt.date
#     analysis_df['time'] = analysis_df['datetime'].dt.time
    analysis_df = analysis_df[['date', 'action', 'description']]
    analysis_df['action'] = analysis_df['action'].apply(update_categories)
    grouped_by_date = analysis_df.groupby('date')
    grouped_by_action = analysis_df.groupby('action')

    today = date.today()
    yesterday = today - timedelta(days=1)
    last_7_days_pomo = {}
    foods_last_7_days = {}
    total_pomo_yesterday = 0
    total_pomo_today = 0

    initialize_stats_dict()

    for i in range(7):
        last_7_days_pomo[(today - timedelta(days=i+1)
                          ).strftime('%Y-%m-%d')] = ''
        foods_last_7_days[(today - timedelta(days=i+1)
                           ).strftime('%Y-%m-%d')] = []

    foods_today = []
    foods_yesterday = []

    # last seven days data per day
    last_7_days_description_df = {}

    # last seven days data combined by category
    last_7_days_description_df_combined_categories = {}

    # iterate through the groups
    for date, group in grouped_by_date:
        # print('Group:', date)
        value_counts = group['action'].value_counts()
        description_df = {}
        for category in CATEGORIES_MAPPING.values():
            combined = []

            def combine_series(item):
                global combined
                combined.append(item)
            group[group['action'] == category]['description'].apply(
                combine_series)
            combined = clean_combined(combined)
            counts = Counter(combined)
            description_df[category] = dict(counts)
        last_7_days_description_df[date.strftime('%Y-%m-%d')] = description_df

    initialize_last_7_days_description_df_combined_categories()

    for date in last_7_days_description_df.keys():

        day_df = last_7_days_description_df[date]
        for category in UNIQUE_CATEGORIES:
            last_7_days_description_df_combined_categories[category].append(
                day_df[category])

    for category in last_7_days_description_df_combined_categories.keys():
        last_7_days_description_df_combined_categories[category] = dict(sum(map(
            Counter, [dict for dict in last_7_days_description_df_combined_categories[category]]), Counter()))

    total_pomo_time = sum(
        [count for count in last_7_days_description_df_combined_categories['pomo'].values()])
    total_pomo_time = total_pomo_time * POMO_TIME / 60
    total_pomo_time = f'{total_pomo_time:.2f} h'
    last_7_days_description_df_combined_categories['pomo'] = total_pomo_time

    with open(f'last_7_days/{today}.json', 'w') as f:
        # Write the dictionary to the file in JSON format
        json.dump(last_7_days_description_df_combined_categories, f)
        plot_consumption_over_last_week(last_7_days_description_df_combined_categories, today, True)
        print('Saved json and plot in last_7_days/')

    # print(last_7_days_description_df_combined_categories)
