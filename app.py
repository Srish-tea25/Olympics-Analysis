import streamlit as st
import pandas as pd
import helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff


medal_tally = pd.read_csv('Olympic_Games_Medal_Tally.csv')
countries = pd.read_csv('Olympics_Country.csv')
event_results = pd.read_csv('Olympic_Athlete_Event_Results.csv')
results = pd.read_csv('Olympic_Results.csv')
bio = pd.read_csv('Olympic_Athlete_Bio.csv')

medal_tally['season'] = medal_tally['edition'].str.split(" ", n=2, expand=True)[1]

medal_tally = medal_tally[(medal_tally['season'] == 'Summer') | (medal_tally['season'] == 'Winter')]


event_results['year'] = event_results['edition'].str.split(" ", n=2, expand=True)[0]
event_results['season'] = event_results['edition'].str.split(" ", n=2, expand=True)[1]

st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':
    st.header("Medal Tally")
    years, country, season = helper.year_country_season(medal_tally)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    selected_season = st.sidebar.selectbox("Select Season", season)

    output1 = helper.fetch_values(medal_tally, selected_year, selected_country, selected_season)
    if (selected_season == 'Overall') & (selected_country == 'Overall') & (selected_year == 'Overall'):
        st.title("Overall Tally")
        st.write("Here _S represents Values for Summer Olympics and _W represents Values for Winter Olympics.")
    if (selected_season == 'Overall') & (selected_country == 'Overall') & (selected_year != 'Overall'):
        st.title("Tally of countries in " + str(selected_year))
    if (selected_season != 'Overall') & (selected_country == 'Overall') & (selected_year == 'Overall'):
        st.title("Tally of countries in " + selected_season + " Olympics")
    if (selected_season == 'Overall') & (selected_country != 'Overall') & (selected_year == 'Overall'):
        st.title("Overall Tally of " + selected_country)
    if (selected_season != 'Overall') & (selected_country == 'Overall') & (selected_year != 'Overall'):
        st.title("Tally of countries in " + selected_season + " Olympics of " + str(selected_year))
    if (selected_season != 'Overall') & (selected_country != 'Overall') & (selected_year == 'Overall'):
        st.title("Tally of " + selected_country + " in " + selected_season + " Olympics")
    if (selected_season == 'Overall') & (selected_country != 'Overall') & (selected_year != 'Overall'):
        st.title("Tally of " + selected_country + " in " + str(selected_year) + " Olympics")
    if (selected_season != 'Overall') & (selected_country != 'Overall') & (selected_year != 'Overall'):
        st.title("Tally of " + selected_country + " in " + selected_season + " Olympics of " + str(selected_year))
    st.table(output1)


if user_menu == 'Overall Analysis':

    Years = medal_tally['year'].unique().shape[0]
    Countries = medal_tally['country'].unique().shape[0]
    Sports = event_results['sport'].unique().shape[0]
    Athletes = bio['name'].unique().shape[0]
    Editions = event_results['edition'].unique().shape[0]
    Events = event_results['event'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(Editions)
    with col2:
        st.header("Countries")
        st.title(Countries)
    with col3:
        st.header("Sports")
        st.title(Sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Athletes")
        st.title(Athletes)
    with col2:
        st.header("Result Locations")
        st.title(Years)
    with col3:
        st.header("Events")
        st.title(Events)

    summer_nations, winter_nations = helper.participating_nations_over_time(event_results, countries)
    fig1 = px.line(summer_nations, x="Year", y="Number of Countries Participated")
    st.title("Participating Nations over Years in Summer Olympics")
    st.plotly_chart(fig1)
    fig2 = px.line(winter_nations, x="Year", y="Number of Countries Participated")
    st.title("Participating Nations over Years in Winter Olympics")
    st.plotly_chart(fig2)

    summer_athletes, winter_athletes = helper.participating_athletes_over_time(event_results, countries)
    fig3 = px.line(summer_athletes, x="Year", y="Number of Athletes Participated")
    st.title("Participating Athletes over Years in Summer Olympics")
    st.plotly_chart(fig3)
    fig4 = px.line(winter_athletes, x="Year", y="Number of Athletes Participated")
    st.title("Participating Athletes over Years in Winter Olympics")
    st.plotly_chart(fig4)

    summer_events, winter_events = helper.events_over_time(event_results, countries)
    fig5 = px.line(summer_events, x="Year", y="Number of Events")
    st.title("Events over Years in Summer Olympics")
    st.plotly_chart(fig5)
    fig6 = px.line(winter_events, x="Year", y="Number of Events")
    st.title("Events over Years in Winter Olympics")
    st.plotly_chart(fig6)

    st.title('Number of Events over Years(in every Sport)')
    fig, ax = plt.subplots(figsize=(30, 30))
    x_summer, x_winter = helper.heatmap_summer_winter(event_results, countries)
    st.write("Heatmap for Summer Olympics")
    ax = sns.heatmap(
        x_summer.pivot_table(index='sport', columns='year', values='event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)
    fig, ax = plt.subplots(figsize=(20, 20))
    st.write("Heatmap for Winter Olympics")
    ax = sns.heatmap(
        x_winter.pivot_table(index='sport', columns='year', values='event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = event_results['sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox("Select Sport", sport_list)
    x = helper.best_athletes(event_results, countries, selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    country_list = medal_tally['country'].unique().tolist()
    country_list.sort()
    selected_country_for_analysis = st.sidebar.selectbox("Select Country", country_list)

    if medal_tally[(medal_tally['country'] == selected_country_for_analysis) & (medal_tally['season'] == 'Summer')].shape[0] == 0:
        st.write(selected_country_for_analysis + "has never won or participated in Summer Olympics")
    else:
        total_medals_summer = helper.country_analysis_summer(medal_tally, selected_country_for_analysis)
        fig = px.line(total_medals_summer, x='year', y='total')
        st.title("Number of Medals over year for " + selected_country_for_analysis + " in Summer Olympics ")
        st.plotly_chart(fig)

    if medal_tally[(medal_tally['country'] == selected_country_for_analysis) & (medal_tally['season'] == 'Winter')].shape[0] == 0:
        st.write(selected_country_for_analysis + " has never won or participated in Winter Olympics")
    else:
        total_medals_winter = helper.country_analysis_winter(medal_tally, selected_country_for_analysis)
        fig = px.line(total_medals_winter, x='year', y='total')
        st.title("Number of Medals over year for " + selected_country_for_analysis + " in Winter Olympics ")
        st.plotly_chart(fig)

    heatmap_country = helper.heatmap_country(event_results, countries, selected_country_for_analysis)
    fig, ax = plt.subplots(figsize=(20, 20))
    st.title(selected_country_for_analysis + " performance in every Sport.")
    ax = sns.heatmap(heatmap_country, annot=True)
    st.pyplot(fig)

    table_country = helper.table_country(event_results, countries, selected_country_for_analysis)
    st.title("Most Successful athletes in " + selected_country_for_analysis)
    st.table(table_country)

if user_menu == 'Athlete-wise Analysis':
    x1, x2, x3, x4, x, sport_name, athlete_df = helper.extract_ages(bio, event_results)

    fig1 = ff.create_distplot([x1, x2, x3, x4], ['OverAll Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                              show_hist=False, show_rug=False)
    fig1.update_layout(autosize=False, width=900, height=500)
    st.title('Distribution of Age in Olympics')
    st.plotly_chart(fig1)

    fig = ff.create_distplot(x, sport_name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=900, height=500)
    st.title('Distribution of Age in Top Sports')
    st.plotly_chart(fig)

    sport_list = event_results['sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox("Select Sport", sport_list)

    sport_df = helper.athlete_analysis(bio, event_results, selected_sport)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(data=sport_df, x='weight', y='height', hue='medal', style='sex', s=70)
    st.title('Weight Vs Height in Top Sports')
    st.pyplot(fig)

    final_summer, final_winter = helper.men_vs_women(event_results, bio)
    fig = px.line(final_summer, x='year', y=['Male', 'Female'])
    st.title("Participation of Men and Women over the years in Summer Olympics")
    st.plotly_chart(fig)
    fig = px.line(final_winter, x='year', y=['Male', 'Female'])
    st.title("Participation of Men and Women over the years in Winter Olympics")
    st.plotly_chart(fig)

