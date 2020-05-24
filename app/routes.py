from app import app
from flask import render_template, url_for
import pandas as pd
from datetime import date
from flask import json

current_year = date.today().year
master_table = pd.read_csv('mdata/final_result/master_table.csv')
weekly_table = pd.read_csv('mdata/thenum/weekly_tops/weekly_tops.csv')
yearly_table = pd.read_csv('mdata/thenum/yearly_tops/2020_tops.csv')
binned_table = pd.read_csv('mdata/final_result/binned_table.csv')
genre_table = pd.read_csv('mdata/final_result/genre_table.csv')


@app.route('/')
def index():

    yearly_dict = {
        "movie_name": yearly_table["name"].values
    }

    weekly_dict = {
        "movie_name": weekly_table["name"].values
    }
    master_table.sort_values(by='worldwide_box_office',
                             ascending=False, inplace=True)
    x = 6
    top_4 = master_table[:x]
    movie_dict = {
        'movie_score': top_4["bb_score"].values,
        'movie_poster': top_4["poster_path"].values,
        'movie_title': top_4["name"].values
    }

    return render_template('index.html', movie_dict=movie_dict, weekly_dict=weekly_dict, yearly_dict=yearly_dict, x=x)


@app.route('/movie_list')
def movie_list():
    num_movies = len(master_table)

    title_list = master_table["name"]
    year_list = master_table["year"]

    return render_template('movie_list.html', title_list=title_list, year_list=year_list, num_movies=num_movies)


@app.route('/movie_page/<movie_data>')
def movie_page(movie_data):
    labels = binned_table.binned.to_list()
    values = binned_table.bb_score.to_list()
    movie_data = movie_data.split("^")
    title, year = movie_data[0], int(movie_data[1])
    movie_info = master_table[(master_table["name"] == title) & (
        master_table["year"] == year)]

    movie_dict = {
        'movie_score': int(movie_info["bb_score"].values[0]),
        'movie_mpaa_rating': (movie_info["mpaa_rating"].values[0]),
        'movie_runtime': (movie_info["running_time"].values[0]),
        'movie_title': (movie_info["name"].values[0]),
        'movie_year': (movie_info["year"].values[0]),
        'movie_opening_weekend': (movie_info["opening_weekend"].values[0]),
        'movie_domestic_gross': (movie_info["domestic_box_office"].values[0]),
        'movie_international_gross': (movie_info["international_box_office"].values[0]),
        'movie_worldwide_gross': (movie_info["worldwide_box_office"].values[0]),
        'movie_budget': (movie_info["production_budget"].values[0]),
        'movie_synopsis': (movie_info["synopsis"].values[0]),
        'movie_poster': (movie_info["poster_path"].values[0]),
        'movie_distributor': (movie_info["production_companies"].values[0]),
        'movie_legs': (movie_info["legs"].values[0]),
        'movie_theaters': (movie_info["theater_counts"].values[0]),
        'movie_genre': (movie_info["genre"].values[0]),
        'movie_pscore': (movie_info["bb_profit_score"].values[0]),
        'movie_mscore': (movie_info["bb_profit_multiple_score"].values[0])
    }

    movie_dict['genre_bb'] = genre_table[genre_table.genre ==
                                         movie_dict['movie_genre']].bb_score.values[0]

    return render_template('movie_page.html', movie_data=movie_dict, labels=labels, values=values)


@app.route('/about_us')
def about_us():

    return render_template('about_us.html')


if __name__ == '__main__':
    app.run(debug=True)
