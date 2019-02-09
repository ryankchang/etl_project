import pandas as pd
from sqlalchemy import create_engine
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
import pymysql 
pymysql.install_as_MySQLdb()

#read CSV files into pandas
#to access the data: https://www.kaggle.com/pschale/mlb-pitch-data-20152018#atbats.csv
csv_atbats = "data/atbats.csv"
csv_games = "data/games.csv"
csv_pitches = "data/pitches.csv"
csv_playernames = "data/player_names.csv"

atbats_data_df = pd.read_csv(csv_atbats)
games_data_df = pd.read_csv(csv_games)
pitches_data_df = pd.read_csv(csv_pitches)
playernames_data_df = pd.read_csv(csv_playernames)

#create the url's for each player
playernames_data_df['name_url'] = playernames_data_df['last_name'].str[0:5].str.lower() + playernames_data_df['first_name'].str[0:2].str.lower()
playernames_data_df['name_url_edit'] = playernames_data_df['name_url'].str.replace("'","")
playernames_data_df['name_url_edit'] = playernames_data_df['name_url'].str.replace(" ","")
playernames_data_df['search_url'] =  "https://www.baseball-reference.com/players/" +playernames_data_df['name_url_edit'].str[0:1]+"/"+ playernames_data_df['name_url_edit'] + "01.shtml"

#See which url's connect successfully
connection = []
for index, row in playernames_data_df.iterrows(): 
    request = requests.get(playernames_data_df['search_url'][index])
    if request.status_code == 200:
        connection.append(1)
    else:
        connection.append(0)

#append connection column to existing dataframe
playernames_data_df['connection'] = connection

#remove 404 connection errors
#playernames_success_df = playernames_data_df.loc[(playernames_data_df['connection'] == 1),:]
playernames_success_df = playernames_data_df

#reindex
playernames_success_df = playernames_success_df.reset_index(drop=True)

weight = []
for index,row in playernames_success_df.iterrows(): 
    html = row['search_url']
    response = requests.get(html)
    soup = bs(response.text, 'html.parser')
    try:
        weight.append(soup.find('span', itemprop='weight').text)
    except(AttributeError):
        weight.append("NA")

#append weight data to existing dataframe
playernames_success_df['weight'] = weight

#remove NA's
#playernames_success_df = playernames_success_df.loc[(playernames_success_df['weight'] != "NA"),:]

#reindex
playernames_success_df = playernames_success_df.reset_index(drop=True)

#drop the connection column
playernames_success_df = playernames_success_df.drop(['connection'],axis=1)

#drop index from all dataframes
atbats_data_df.set_index(['ab_id'],inplace=True)
pitches_data_df.set_index(['ab_id'],inplace=True)
games_data_df.set_index(['g_id'],inplace=True)
playernames_success_df.set_index(['id'],inplace=True)

#connect to local database
rds_connection_string = "root:Banking5%@127.0.0.1/baseball_db"
engine = create_engine(f'mysql://{rds_connection_string}')

#Get sql code to create tables
print(pd.io.sql.get_schema(pitches_data_df.reset_index(), 'pitches'))
print(pd.io.sql.get_schema(atbats_data_df.reset_index(), 'atbats'))
print(pd.io.sql.get_schema(games_data_df.reset_index(), 'games'))
print(pd.io.sql.get_schema(playernames_success_df.reset_index(), 'player_names'))

#export all data into MySQL
atbats_data_df.to_sql(name='atbats', con=engine, if_exists='replace', index=True)
playernames_success_df.to_sql(name='player_names', con=engine, if_exists='replace', index=True)
games_data_df.to_sql(name='games', con=engine, if_exists='replace', index=True)
pitches_data_df.to_sql(name='pitches', con=engine, if_exists='replace', index=True)

#confirm sql query works
pd.read_sql_query('select * from games', con=engine).head()