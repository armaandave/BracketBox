from app import app
from flask import render_template, url_for
import pandas as pd

master_table = pd.read_csv('mdata/final_result/master_table.csv') 


@app.route('/')
@app.route('/index/')
def index():
     
    return render_template('index.html')


@app.route('/movie_list')
def movie_list():
    num_movies = len(master_table)

    title_list = master_table["name"]
    year_list = master_table["year"]

    return render_template('movie_list.html', title_list = title_list, year_list = year_list, num_movies = num_movies)


@app.route('/movie_page/<movie_data>')
def movie_page(movie_data):
    movie_data = movie_data.split("^")
    title, year = movie_data[0], int(movie_data[1])
    movie_info = master_table[(master_table["name"] == title) & (master_table["year"] == year)]


    movie_dict = {
    'movie_score' : int(movie_info["bb_score"].values[0]),
    'movie_mpaa_rating' : (movie_info["mpaa_rating"].values[0]),
    'movie_runtime' : (movie_info["running_time"].values[0]),
    'movie_title' : (movie_info["name"].values[0]),
    'movie_year' : (movie_info["year"].values[0]),
    'movie_opening_weekend': (movie_info["opening_weekend"].values[0]),
    'movie_domestic_gross' : (movie_info["domestic_box_office"].values[0]),
    'movie_international_gross': (movie_info["international_box_office"].values[0]),
    'movie_worldwide_gross' : (movie_info["worldwide_box_office"].values[0]),
    'movie_budget' : (movie_info["production_budget"].values[0]),
    'movie_synopsis' : (movie_info["synopsis"].values[0]),
    'movie_poster': (movie_info["poster_path"].values[0]),
    'movie_distributor': (movie_info["production_companies"].values[0]),
    'movie_legs': (movie_info["legs"].values[0]),
    'movie_theaters': (movie_info["theater_counts"].values[0]),
    'movie_genre': (movie_info["genre"].values[0]),
    'movie_pscore': (movie_info["bb_profit_score"].values[0]),
    'movie_mscore': (movie_info["bb_multiple_score"].values[0])
    }


    return render_template('movie_page.html', movie_data = movie_dict)   



if __name__ == '__main__':
   app.run(debug = True)
