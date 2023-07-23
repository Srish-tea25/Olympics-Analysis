import pandas as pd
import numpy as np
import re


def medals_tally(df):

    summer = df[df['season'] == 'Summer'].groupby('country').sum()[['gold', 'silver', 'bronze', 'total']]
    winter = df[df['season'] == 'Winter'].groupby('country').sum()[['gold', 'silver', 'bronze', 'total']]

    df1 = summer.merge(winter, how='outer', on='country').fillna(0)
    df1.columns = ['Gold_S', 'Silver_S', 'Bronze_S', 'Total_S', 'Gold_W', 'Silver_W', 'Bronze_W', 'Total_W']

    df1['Total Medals'] = df1['Total_S'] + df1['Total_W']
    final = df1.sort_values('Total Medals', ascending=False).reset_index()

    final['Gold_S'] = final['Gold_S'].astype('int')
    final['Silver_S'] = final['Silver_S'].astype('int')
    final['Bronze_S'] = final['Bronze_S'].astype('int')
    final['Total_S'] = final['Total_S'].astype('int')
    final['Gold_W'] = final['Gold_W'].astype('int')
    final['Silver_W'] = final['Silver_W'].astype('int')
    final['Bronze_W'] = final['Bronze_W'].astype('int')
    final['Total_W'] = final['Total_W'].astype('int')
    final['Total Medals'] = final['Total Medals'].astype('int')

    return final


def year_country_season(df):

    years = np.unique(df['year']).tolist()
    years.insert(0, 'Overall')

    country = np.unique(df['country']).tolist()
    country.insert(0, 'Overall')

    season = np.unique(df['season']).tolist()
    season.insert(0, 'Overall')

    return years, country, season


def fetch_values(df, year, country, season):

    if year == 'Overall' and country == 'Overall' and season == 'Overall':
        df2 = medals_tally(df)
    if year == 'Overall' and country == 'Overall' and season != 'Overall':
        df2 = df[df['season'] == season].sort_values('year').reset_index(drop=True)
    if year == 'Overall' and country != 'Overall' and season == 'Overall':
        df2 = df[df['country'] == country].sort_values('year').reset_index(drop=True)
    if year != 'Overall' and country == 'Overall' and season == 'Overall':
        df2 = df[df['year'] == year].sort_values('total', ascending=False).reset_index(drop=True)
    if year != 'Overall' and country != 'Overall' and season == 'Overall':
        df2 = df[(df['country'] == country) & (df['year'] == year)].sort_values('total',
                                                                                     ascending=False).reset_index(
            drop=True)
    if year == 'Overall' and country != 'Overall' and season != 'Overall':
        df2 = df[(df['country'] == country) & (df['season'] == season)].sort_values('year').reset_index(
            drop=True)
    if year != 'Overall' and country == 'Overall' and season != 'Overall':
        df2 = df[(df['season'] == season) & (df['year'] == year)].sort_values('total',
                                                                              ascending=False).reset_index(
            drop=True)
    if year != 'Overall' and country != 'Overall' and season != 'Overall':
        df2 = df[(df['country'] == country) & (df['year'] == year) & (df['season'] == season)]\
            .sort_values('total', ascending=False).reset_index(drop=True)

    return df2


def participating_nations_over_time(d_frame1, d_frame2):
    df = d_frame1.merge(d_frame2, on='country_noc')
    df1 = df.drop_duplicates(['edition', 'country']).reset_index(drop=True)

    country_count_of_summer_olympics = df1[df1['season'] == 'Summer']
    country_count_of_winter_olympics = df1[df1['season'] == 'Winter']

    summer_country_table = country_count_of_summer_olympics['year'].value_counts().reset_index().sort_values('year')
    summer_country_table.rename(columns={'year': 'Year', 'count': 'Number of Countries Participated'}, inplace=True)

    winter_country_table = country_count_of_winter_olympics['year'].value_counts().reset_index().sort_values('year')
    winter_country_table.rename(columns={'year': 'Year', 'count': 'Number of Countries Participated'}, inplace=True)

    return summer_country_table, winter_country_table


def participating_athletes_over_time(d_frame1, d_frame2):
    df = d_frame1.merge(d_frame2, on='country_noc')
    df2 = df.drop_duplicates(['edition', 'athlete_id']).reset_index(drop=True)

    athlete_count_of_summer_olympics = df2[df2['season'] == 'Summer']
    athlete_count_of_winter_olympics = df2[df2['season'] == 'Winter']

    summer_athlete_table = athlete_count_of_summer_olympics['year'].value_counts().reset_index().sort_values('year')
    summer_athlete_table.rename(columns={'year': 'Year', 'count': 'Number of Athletes Participated'}, inplace=True)

    winter_athlete_table = athlete_count_of_winter_olympics['year'].value_counts().reset_index().sort_values('year')
    winter_athlete_table.rename(columns={'year': 'Year', 'count': 'Number of Athletes Participated'}, inplace=True)

    return summer_athlete_table, winter_athlete_table


def events_over_time(d_frame1, d_frame2):
    df = d_frame1.merge(d_frame2, on='country_noc')
    df3 = df.drop_duplicates(['edition', 'event']).reset_index(drop=True)

    event_count_of_summer_olympics = df3[df3['season'] == 'Summer']
    event_count_of_winter_olympics = df3[df3['season'] == 'Winter']

    summer_event_table = event_count_of_summer_olympics['year'].value_counts().reset_index().sort_values('year')
    summer_event_table.rename(columns={'year': 'Year', 'count': 'Number of Events'}, inplace=True)

    winter_event_table = event_count_of_winter_olympics['year'].value_counts().reset_index().sort_values('year')
    winter_event_table.rename(columns={'year': 'Year', 'count': 'Number of Events'}, inplace=True)

    return summer_event_table, winter_event_table


def heatmap_summer_winter(d_frame1, d_frame2):
    df = d_frame1.merge(d_frame2, on='country_noc')
    x_summer = df[df['season'] == 'Summer'].drop_duplicates(['year', 'sport', 'event']).reset_index(drop=True)
    x_winter = df[df['season'] == 'Winter'].drop_duplicates(['year', 'sport', 'event']).reset_index(drop=True)

    return x_summer, x_winter


def best_athletes(d_frame1, d_frame2, sport):
    df = d_frame1.merge(d_frame2, on='country_noc')
    athlete_with_medals = df[df['medal'] != 'na'].reset_index(drop=True)
    if sport == 'Overall':
        ss = athlete_with_medals[['athlete', 'sport']].value_counts().reset_index()
        ss = ss.merge(athlete_with_medals, on=['athlete', 'sport'])
        ss = ss.drop_duplicates(['athlete', 'sport']).reset_index()[['athlete', 'count', 'sport', 'country']]
        ss.rename(columns={'athlete': 'Athlete', 'count': 'Medals'}, inplace=True)
    else:
        ss = athlete_with_medals[athlete_with_medals['sport'] == sport]['athlete'].value_counts().reset_index()
        ss = ss.merge(athlete_with_medals, left_on='athlete', right_on='athlete')
        ss = ss[['athlete', 'count', 'sport', 'country']].drop_duplicates('athlete').rename(
            columns={'athlete': 'Athlete', 'count': 'Medals'}).reset_index(drop=True)

    return ss.head(15)


def country_analysis_summer(df, country):
    total_medals_summer = df[(df['country'] == country) & (df['season'] == 'Summer')][['year', 'total']].\
        reset_index(drop=True)

    return total_medals_summer


def country_analysis_winter(df, country):
    total_medals_winter = df[(df['country'] == country) & (df['season'] == 'Winter')][['year', 'total']]. \
        reset_index(drop=True)

    return total_medals_winter


def heatmap_country(d_frame1, d_frame2, country):
    dff = d_frame1[d_frame1['medal'] != 'na'].drop_duplicates(['edition', 'sport', 'event',
                                                               'pos', 'medal', 'isTeamSport', 'season'])
    dff = dff.merge(d_frame2, on='country_noc')
    dff = dff[dff['country'] == country]
    dff = dff.pivot_table(index='sport', columns='year', values='medal', aggfunc='count').fillna(0).astype('int')

    return dff


def table_country(d_frame1, d_frame2, country):
    df = d_frame1.merge(d_frame2, on='country_noc')
    df = df[df['medal'] != 'na']
    df = df[df['country'] == country]['athlete'].value_counts().reset_index().merge(df, on='athlete')
    df = df.drop_duplicates('athlete')[['athlete', 'count', 'country', 'sport']].reset_index(drop=True)
    df.rename(columns={'count': 'Medals'}, inplace=True)

    return df.head(10)


def find(x):
    try:
        result = re.findall(r'\d+', x)[0]
    except IndexError:
        result = 'na'
    return result


def avg(x):
    try:
        lst = [eval(i) for i in re.findall(r'\d+', x)]
        result = sum(lst)/len(lst)
    except ZeroDivisionError:
        result = 'na'
    return result


def extract_ages(df1, df2):
    athlete_df = df1.drop_duplicates('athlete_id').merge(df2.drop_duplicates('athlete_id'), on='athlete_id')
    athlete_df['born_year'] = athlete_df['born'].apply(lambda x: find(x))
    athlete_df = athlete_df[athlete_df['born_year'] != 'na']
    athlete_df['age'] = athlete_df['year'].astype('int') - athlete_df['born_year'].astype('int')
    x1 = athlete_df['age']
    x2 = athlete_df[athlete_df['medal'] == 'Gold']['age']
    x3 = athlete_df[athlete_df['medal'] == 'Silver']['age']
    x4 = athlete_df[athlete_df['medal'] == 'Bronze']['age']

    famous_sports = athlete_df['sport'].value_counts().head(49).index.tolist()
    x = []
    sport_name = []
    for i in famous_sports:
        sport_df = athlete_df[athlete_df['sport'] == i]
        x.append(sport_df[sport_df['medal'] == 'Gold']['age'])
        sport_name.append(i)

    return x1, x2, x3, x4, x, sport_name, athlete_df


def athlete_analysis(df1, df2, sport):
    x1, x2, x3, x4, x, sport_name, athlete_df = extract_ages(df1, df2)

    athlete_df['weight'] = athlete_df['weight'].apply(lambda x: avg(x))
    athlete_df['weight'].replace('na', athlete_df[athlete_df['weight'] != 'na']['weight'].median(), inplace=True)
    athlete_df['height'].replace('na', athlete_df[athlete_df['height'] != 'na']['height'].astype('float').mean(),
                                 inplace=True)
    athlete_df['height'] = athlete_df['height'].astype('float')
    athlete_df['medal'].replace('na', 'No Medal', inplace=True)
    if sport == 'Overall':
        sport_df = athlete_df
    else:
        sport_df = athlete_df[athlete_df['sport'] == sport]

    return sport_df


def men_vs_women(df1, df2):
    df = df1.merge(df2, on='athlete_id')
    men_df_summer = df[(df['sex'] == 'Male') & (df['season'] == 'Summer')].groupby('year')[
        'athlete_id'].nunique().reset_index()
    women_df_summer = df[(df['sex'] == 'Female') & (df['season'] == 'Summer')].groupby('year')[
        'athlete_id'].nunique().reset_index()
    final_summer = women_df_summer.merge(men_df_summer, on='year')
    final_summer.rename(columns={'athlete_id_x': 'Female', 'athlete_id_y': 'Male'}, inplace=True)
    men_df_winter = df[(df['sex'] == 'Male') & (df['season'] == 'Winter')].groupby('year')[
        'athlete_id'].nunique().reset_index()
    women_df_winter = df[(df['sex'] == 'Female') & (df['season'] == 'Winter')].groupby('year')[
        'athlete_id'].nunique().reset_index()
    final_winter = women_df_winter.merge(men_df_winter, on='year')
    final_winter.rename(columns={'athlete_id_x': 'Female', 'athlete_id_y': 'Male'}, inplace=True)

    return final_summer, final_winter
