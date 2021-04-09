import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

title = "Predicting Candidate Wind Farm Locations in the Philippines"
st.set_page_config(page_title=title, page_icon=":earth_asia:", initial_sidebar_state="auto")

intro = "Introduction"
dataInfo = "About the Data"
results = "Conclusion and Recommendations"
team = "The Team"

page_titles = [
  intro,
  dataInfo,
  results,
  team
]

page = st.sidebar.radio("Page Navigation", page_titles)

for_data_df = pd.read_csv("data/for_data.csv", index_col=0)
for_model_df = pd.read_csv("data/for_model.csv", index_col=0)

def insertBlankLines(num_of_blank_lines):
  for i in range(num_of_blank_lines):
    st.markdown("")

def center(text):
  st.markdown('<div style="text-align: center;font-size: 1rem;">' + text + '</div>', unsafe_allow_html=True)

def center_title(text):
  st.markdown('<div style="text-align: center;font-weight: bold;font-size: 2rem;">' + text + '</div>', unsafe_allow_html=True)

def medium(text):
  st.markdown('<div style="text-align: left;font-size: 1.2rem;">' + text + '</div>', unsafe_allow_html=True)

def bold(text, font=1):
  return '<span style="font-size: ' + str(font) + 'rem;font-weight: bold;">' + text + '</span>'

def italic(text):
  return '<span style="font-style: italic;">' + text + '</span>'

def quiet(text, font=1):
  return '<span style=": gray;font-size: ' + str(font) + 'rem;">' + text + '</span>'

def right(text):
  return '<p style="text-align: right;">' + text + '</p>'

def url_md(text, url):
  return "[" + text + "](" + url + ")"

def writeText(text, align="center"):
  st.write("<h3 style='text-align: " + align + ";'>" + text + "</h3>", unsafe_allow_html=True)

def plot_data_df(df, x_col, x_label):
  fig = plt.figure(figsize=(10, 14))
  font = {'family' : 'Arial',
          'weight' : 'normal',
          'size'   : 24}

  plt.rc('font', **font)
  clrs = ["lightskyblue" if (x < df[x_col].max()) else "dodgerblue" for x in df[x_col]]
  ax = sns.barplot(x=x_col, y="Anime", data=df, palette=clrs)
  ax.xaxis.set_ticks_position('top')
  # ax.xaxis.set_label_position('top')
  ax.set(xlabel="", ylabel="")
  plt.show()

  center("Showing " + str(len(df)) + " Anime Shows: " + x_label)
  fig

def plot_model_df(df):
  show_anime = True
  if len(df) < 3000:
    show_anime = False

  fig = px.scatter(df, width=700, height=400,
                   x='Polarity',
                   y='Subjectivity',
                   color='Analysis',
                   hover_data={'Polarity': True,
                               'Subjectivity': True,
                               'Analysis': True,
                               'Anime': show_anime,
                               'Season': True,
                               'Done': show_anime,
                               'mal_id': True })
  fig.update_layout(shapes=[dict(type='line',
                                 yref='paper', y0=0, y1=1,
                                 xref='x', x0=0, x1=0)])
  fig

def plot_time_df(df_grouped):
  fig = plt.figure(figsize=(10, 5))

  font = {'family' : 'Arial',
          'weight' : 'normal',
          'size'   : 14}

  plt.rc('font', **font)

  x = [0, 1, 2, 3, 4, 5]
  xi = list(range(len(x)))
  plt.xticks(xi, x)
  plt.ylabel('Polarity')
  sns.lineplot(data=df_grouped, x='Season', y='Polarity', hue='Anime', style='Anime', markers = True)
  plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc = "lower left", mode ="expand", ncol = 5)
  fig

if page == intro:
  center_title("Predicting Candidate Wind Farm<br/>"
    + "Locations in the Philippines<br/>"
    + "Through Time Series Modeling<br/>"
    + "and Spatial Downscaling")
  center(italic("By <a href=\"https://www.linkedin.com/in/jan-pasia/\">" + quiet("Jan Allen Pasia") + "</a>, 14 April 2021"))

  insertBlankLines(2)
  st.image("assets/intro-1.jpg", use_column_width=True)
  st.markdown(
    right(
      quiet(
        'Photo by <a href="https://unsplash.com/@anikinearthwalker?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Dimitry Anikin</a> '+
        'on <a href="https://unsplash.com/s/photos/wind-turbine?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>', 0.8
      )
    ),
    unsafe_allow_html=True)

  insertBlankLines(2)
  st.markdown(bold("What is a wind farm?"), True)

  st.markdown("A wind farm (also wind park, wind power station, wind power plant, or wind power system) " +
    "is a group of big machines called " + bold("wind turbines") + ". " +
    "Most wind turbines have the standard 3 blades. " +
    "These blades move when there is enough wind passing through the area of the turbine. " +
    "This movement rotates the generator, which in turn, generates electricity.", True)

  st.markdown("According to <a href=\"https://en.wikipedia.org/wiki/Wind_farm\">Wikipedia</a>, " +
    "wind farms vary in the size of land covered. " +
    "The size of the farm area is supported by the area's ability to harvest " + bold("wind energy") + ". " +
    "Wind farms can be built on either land or sea.", True)

  st.markdown(bold("Why should I care about wind farms?"), True)

  st.markdown(
    "According to the <a href=\"https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1530-9290.2012.00464.x\">" +
    "2012 study by Stacey L. Dolan and Garvin A. Heath</a>, " +
    "the median life cycle greenhouse gas emissions of utility-scale " + bold("wind power systems") + " is " +
    bold("11 grams") + " CO<sub>2</sub>-equivalent per kilowatt-hour of electricity produced. " +
    "This median value was computed from 126 estimates published across 49 literature references.", True)

  st.markdown(
    "Meanwhile, according to the <a href=\"https://onlinelibrary.wiley.com/doi/full/10.1111/j.1530-9290.2012.00465.x\">" +
    "2012 study by Michael Whitaker, Garvin A. Heath, Patrick R. O'Donoughue, and Martin Vorum</a>, " +
    "the median life cycle greenhouse gas emissions of " + bold("coal-fired electricity generation ") +
    "is " + bold("980 grams") + " CO<sub>2</sub>-equivalent per kilowatt-hour of electricity produced. " +
    "This median value was computed from 164 estimates published across 53 literature references.", True)

  st.markdown(
    "Lastly, according to the <a href=\"https://onlinelibrary.wiley.com/doi/abs/10.1111/jiec.12084\">" +
    "2014 study by Patrick R. O'Donoughue, Garvin A. Heath, Stacey L. Dolan, and Martin Vorum</a>, " +
    "the median life cycle greenhouse gas emissions of " +
    bold("natural gas‐fired combustion turbine (NGCT) and combined‐cycle (NGCC) systems ") +
    "are " + bold("450 grams and 670 grams ") +
    "CO<sub>2</sub>-equivalent per kilowatt-hour of electricity produced respectively. " +
    "These median values were computed from 69 estimates out of 42 references.", True)

  st.markdown(
    "In short, the carbon footprint of " + bold("wind power") + " is at best " + bold("89 and 40 times smaller") +
    " than that of " + bold("coal and natural gas systems") + " respectively. If the Philippines were to rely on " +
    "wind power systems instead of coal and natural gas, we could make an impact in curbing the amount of carbon emissions.", True)

  # col1, col2, col3 = st.beta_columns((1,7,1))
  # col2.image("assets/intro-1.png", use_column_width=True)


  # insertBlankLines(2)
  # center(bold("Background Context"))
  # st.markdown(
  #   "The production of anime shows is a key investment by production and entertainment studios. " +
  #   "Due to cost, time, and effort required in producing an anime, " +
  #   "the decision of determining the number of seasons to produce and the animation studios to work with " +
  #   "must be guided by sound and rational bases to ensure the sustainability of the investment.")

  # insertBlankLines(2)
  # center(bold("Questions in Mind"))

  # col4, col5, col6 = st.beta_columns((1,7,1))
  # col5.markdown("## How can production studios use audience perception of their anime to guide their production decisions moving forward?")

  # col7, col8, col9 = st.beta_columns(3)
  # col7.markdown("### How did people react to a key plot point?")
  # col8.markdown("### Do we have to change animation studios?")
  # col9.markdown("### Is it worthwhile to further invest in the anime and add another season?")

# elif page == dataInfo:
#   center_title(dataInfo)
#   insertBlankLines(1)
#   st.markdown("We picked 25 anime shows both ongoing and finished from the Top Anime list in the website. " +
#     "**Feel free to explore** the graph below by using the dropdown fields on the left sidebar of this page.")

#   df = for_data_df
#   features = ["Total Number of Reviews",
#               "Number of Seasons",
#               "Total Vote Count of Helpful Reviews",
#               "Mean Vote Count of Helpful Reviews",
#               "Median Vote Count of Helpful Reviews", ]
#   feature = st.sidebar.selectbox(
#       "Which features do you want to compare?",
#       features)

#   statuses = ["Any", "Ongoing", "Finished"]
#   status = st.sidebar.selectbox(
#       "Which anime do you want to compare with?",
#       statuses)

#   status_map = {"Any": "Any", "Finished": "Done", "Ongoing": "Not Done"}
#   if status_map[status] != "Any":
#     df = df[df["done"] == status_map[status]]

#   titles = {"Total Number of Reviews": "review",
#             "Number of Seasons": "season",
#             "Total Vote Count of Helpful Reviews": "sum_helpful",
#             "Mean Vote Count of Helpful Reviews": "helpful_avg",
#             "Median Vote Count of Helpful Reviews": "helpful_median", }
#   plot_data_df(df, titles[feature], feature)

#   insertBlankLines(2)
#   st.markdown("Our data came from [MyAnimeList](https://myanimelist.net/). " +
#     "It is a big catalog of anime shows and manga books -- which is helpful to anime enthusiasts around the globe. " +
#     "At the time of writing, it has 120M page views per month and has been online for 16 years. " +
#     "Lastly, MyAnimeList has millions of members. " +
#     "For instance, the anime Fullmetal Alchemist: Brotherhood has been rated and/or reviewed by at least 2.3 million members.")

#   st.markdown("We chose these 25 anime shows from the top 50 in MyAnimeList. " +
#     "We excluded the movies, the special episodes, and the OVA series " +
#     "because they are not included in the scope of this project.")

#   st.markdown("First, we scraped the data using Jikan API, and got a total of 15,668 reviews. " +
#     "We used the following features of the shows: ")
#   st.markdown("- Anime name")
#   st.markdown("- Season number")
#   st.markdown("- Whether the Anime is Finished or Ongoing (1 Ongoing season of an anime means that it is still an ongoing show.)")
#   st.markdown("- Vote Count for Helpful Reviews")
#   st.markdown("- Review Date")
#   st.markdown("- Review Content")

#   st.markdown("Second, we removed the unwanted characters and words through spacy and NLTK libraries. " +
#     "We followed the criteria below: ")
#   st.markdown("- Lowercase")
#   st.markdown("- Non-numerical")
#   st.markdown("- No special characters")
#   st.markdown("- No stop words (from NLTK)")
#   st.markdown("- No non-English words (from NLTK")

#   st.markdown("Lastly, after the review texts has been cleaned, we proceeded to the juicy part of our process: " +
#     "sentiment analysis and topic modeling. Head over the next page to play with our results.")

# elif page == sentiment_1:
#   center_title(sentiment_1)
#   insertBlankLines(1)
#   st.markdown("The team used the Python library TextBlob to determine the sentiment values of the anime reviews. " +
#     "**Feel free to explore** the charts below by using the dropdown fields on the left sidebar of this page.")

#   shows = [ "All" ] + for_model_df["Anime"].sort_values().unique().tolist()
#   show_1 = st.sidebar.selectbox(
#       "Pick one show from the list:",
#       shows)

#   show_2 = st.sidebar.selectbox(
#       "Pick another show compare it with:",
#       shows)

#   df = for_model_df
#   title = "Overall Sentiment Chart"

#   if show_1 != "All":
#     df = for_model_df[for_model_df["Anime"] == show_1]
#     title = show_1

#   center(bold(title))
#   plot_model_df(df)


#   df = for_model_df
#   title = "Overall Sentiment Chart"

#   if show_2 != "All":
#     df = for_model_df[for_model_df["Anime"] == show_2]
#     title = show_2

#   center(bold(title))
#   plot_model_df(df)

# elif page == sentiment_2:
#   center_title(sentiment_2)

#   insertBlankLines(1)
#   st.markdown("To further compare the anime shows, the **mean polarity** values were obtained per season. " +
#     "The shows were picked according to the number of seasons it has. " +
#     "The first line graph below shows the finished anime shows that have 5 seasons each. " +
#     "Based on the sentiments of the reviewer comments, " +
#     "most of these anime shows received more negative reviews after its first season. " +
#     "This may indicate a need for more evaluation when ordering new seasons for long-running series.")

#   df = for_model_df
#   df_more3 = df[(df['Anime']=='Gintama') | (df['Anime']=='Sword Art Online') | (df['Anime']=='Haikyuu!!')]
#   df_grouped = df_more3.groupby(['Anime', 'Season'])['Polarity'].mean()
#   df_grouped = df_grouped.reset_index()

#   plot_time_df(df_grouped)

#   insertBlankLines(3)
#   st.markdown("The line graph below shows the ongoing anime shows that have at least 4 seasons each.")

#   df = for_model_df
#   df_more3 = df[(df['Anime']=='My Hero Academia') | (df['Anime']=='Shingeki no Kyojin') ]
#   df_grouped = df_more3.groupby(['Anime', 'Season'])['Polarity'].mean()
#   df_grouped = df_grouped.reset_index()

#   plot_time_df(df_grouped)

#   st.markdown("Things are looking good for **Shingeki no Kyojin** with a comeback between seasons 3 and 4. " +
#     "Some of the reviews are highlighted below.")

#   col1, col2, col3 = st.beta_columns((1,7,1))
#   col2.markdown("\"And for me, every season leading up to this one " +
#     "has met these high standards and been great.\"")
#   col2.markdown("\"Characters 11/10. Rating this just a 10 is a shame, " +
#     "since **characters** are what makes this anime great.\"")
#   col2.markdown("\"Oh lawd, and then we were blessed with Season 3 Part 2. " +
#     "How perfect and utterly flawless those 10 **episodes** were.\"")

#   st.markdown("On the other hand, **My Hero Academia** is in a bad spot. " +
#     "This can be implied from the falling mean polarity values, moving towards the negative. " +
#     "Some of the reviews were pulled up from the show's pool.")

#   col4, col5, col6 = st.beta_columns((1,7,1))
#   col5.markdown("\"Major **arcs** were bad and boring...\"")
#   col5.markdown("\"It pains me how much My Hero Academias **animation** is declining.\"")
#   col5.markdown("\"The season doesn’t live up to the previous seasons " +
#     "and it shows as some scenes either **lack** substance or its rushed.\"")
#   col5.markdown("\"That said, there were too many \"empty\" episodes, where the plot didnt move along at all.\"")

# elif page == results:
#   center_title("Conclusion")

#   insertBlankLines(2)
#   medium("- The main topics that showed up were \"anime\", \"season\", \"like\", \"show\" and \"story\".")
#   insertBlankLines(1)
#   medium("- Most of the anime with multiple seasons tend to receive more negative reviews " +
#     "after its first season based on the sentiments of the viewers. " +
#     "This may indicate a need for more evaluation when ordering new seasons for long-running series.")

#   insertBlankLines(3)
#   center_title("Recommendations")

#   insertBlankLines(2)
#   medium("- Consider other sources of audience sentiment and opinion such as discussion forums, reddit, twitter, tumblr, etc.")
#   insertBlankLines(1)
#   medium("- Incorporate review comments per episode and not just per season of the anime series.")
#   insertBlankLines(1)
#   medium("- Evaluate entities in reviews such as character names to identify fan-favorites and hated characters.")

# elif page == team:
#   st.title("Team Leah")
#   insertBlankLines(3)

#   col1, col2, col3 = st.beta_columns(3)
#   with col1:
#     st.image("assets/team-1.png", width=100)
#     col1.markdown(bold("Fili Emerson Chua"), unsafe_allow_html=True)
#     col1.markdown(italic("Mentor"), unsafe_allow_html=True)
#     col1.markdown(url_md("LinkedIn", "https://www.linkedin.com/in/fili-emerson-chua/"), unsafe_allow_html=True)

#     insertBlankLines(3)
#     st.image("assets/team-4.png", width=100)
#     col1.markdown(bold("Razel Manapat"), unsafe_allow_html=True)
#     col1.markdown(italic("Member"), unsafe_allow_html=True)
#     col1.markdown(url_md("LinkedIn", "https://www.linkedin.com/in/razel-manapat-745650166/"), unsafe_allow_html=True)

#   with col2:
#     st.image("assets/team-2.png", width=100)
#     col2.markdown(bold("Joseph Figuracion"), unsafe_allow_html=True)
#     col2.markdown(italic("Member"), unsafe_allow_html=True)
#     col2.markdown(url_md("LinkedIn", "https://www.linkedin.com/in/josephfiguracion/"), unsafe_allow_html=True)

#     insertBlankLines(3)
#     st.image("assets/team-5.png", width=100)
#     col2.markdown(bold("Jan Allen Pasia"), unsafe_allow_html=True)
#     col2.markdown(italic("Member"), unsafe_allow_html=True)
#     col2.markdown(url_md("LinkedIn", "https://www.linkedin.com/in/jan-pasia/"), unsafe_allow_html=True)

#   with col3:
#     st.image("assets/team-3.png", width=100)
#     col3.markdown(bold("Jessica Joy Isidro"), unsafe_allow_html=True)
#     col3.markdown(italic("Member"), unsafe_allow_html=True)
#     col3.markdown(url_md("LinkedIn", "https://www.linkedin.com/in/jessica-joy-isidro/"), unsafe_allow_html=True)

#     insertBlankLines(3)
#     st.image("assets/team-6.png", width=100)
#     col3.markdown(bold("Juan Miguel Sevilla"), unsafe_allow_html=True)
#     col3.markdown(italic("Member"), unsafe_allow_html=True)
#     col3.markdown(url_md("LinkedIn", "https://www.linkedin.com/in/juan-miguel-sevilla-840a8845/"), unsafe_allow_html=True)
