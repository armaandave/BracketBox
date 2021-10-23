from app import app
from flask import render_template, url_for
import pandas as pd
from datetime import date
from flask import json
import ast
import random


current_year = date.today().year
master_table = pd.read_csv('mdata/final_result/master_table.csv')
weekly_table = pd.read_csv('mdata/thenum/weekly_tops/weekly_tops.csv')
yearly_table = pd.read_csv('mdata/thenum/yearly_tops/2021_tops.csv')
binned_table = pd.read_csv('mdata/final_result/binned_table.csv')
genre_table = pd.read_csv('mdata/final_result/genre_table.csv')
in_theateres_table = pd.read_csv(
    'mdata/final_result/trending/current_in_theater.csv')
upcoming_theateres_table = pd.read_csv(
    'mdata/final_result/trending/upcoming_in_theater.csv')
popular_movies_table = pd.read_csv(
    'mdata/final_result/trending/popular_movies.csv')
popular_tv_table = pd.read_csv(
    'mdata/final_result/trending/popular_tv.csv')
demo_table = pd.read_csv('mdata/final_result/demo_table.csv')
all_time_adjusted_domestic = pd.read_csv(
    'mdata/thenum/charts/all_time_adjusted_domestic.csv')
all_time_animated_domestic = pd.read_csv(
    'mdata/thenum/charts/all_time_animated_domestic.csv')
all_time_animated_international = pd.read_csv(
    'mdata/thenum/charts/all_time_animated_international.csv')
all_time_domestic = pd.read_csv('mdata/thenum/charts/all_time_domestic.csv')
all_time_international = pd.read_csv(
    'mdata/thenum/charts/all_time_international.csv')
all_time_worldwide = pd.read_csv('mdata/thenum/charts/all_time_worldwide.csv')
average_table = pd.read_csv('mdata/final_result/final_averages.csv')
print(len(average_table))


@app.route('/')
def index():

    popular_title_list = popular_movies_table["title"]
    popular_poster_list = popular_movies_table["poster_path"]

    demo_dict = {
        "movie_name": demo_table["name"].values,
        "movie_imdb": demo_table["imdb_score"].values,
        "movie_meta": demo_table["meta_score"].values,
        "movie_score": demo_table["bb_score"].values,
        "d_office": demo_table["domestic_box_office"].values,
        "w_office": demo_table["worldwide_box_office"].values,
        "i_office": demo_table["international_box_office"].values,
        "opening_weekend": demo_table["opening_weekend"].values,
        "budget": demo_table["budget"].values
    }

    w = random.randint(0, len(demo_table)-1)
    print(w)

    yearly_dict = {
        "movie_name": yearly_table["name"].values
    }

    weekly_dict = {
        "movie_name": weekly_table["name"].values
    }
    y = len(weekly_dict["movie_name"])
    master_table.sort_values(by='worldwide_box_office',
                             ascending=False, inplace=True)
    x = 6
    top_4 = master_table[:x]
    movie_dict = {
        'movie_score': top_4["bb_score"].values,
        'movie_poster': top_4["poster_path"].values,
        'movie_title': top_4["name"].values
    }

    return render_template('index.html', movie_dict=movie_dict, weekly_dict=weekly_dict, yearly_dict=yearly_dict, x=x, popular_poster_list=popular_poster_list, popular_title_list=popular_title_list, y=y, demo_dict=demo_dict, w=w)


@app.route('/movie_list')
def movie_list():
    num_movies = len(master_table)

    title_list = master_table["name"]
    year_list = master_table["year"]

    return render_template('movie_list.html', title_list=title_list, year_list=year_list, num_movies=num_movies)


@app.route('/movie_page/<movie_data>')
def movie_page(movie_data):
    print(movie_data)
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
        'movie_opening_weekend': ("{:,}".format(int(movie_info["opening_weekend"].values[0]))),
        'movie_domestic_gross': ("{:,}".format(int(movie_info["domestic_box_office"].values[0]))),
        'movie_international_gross': ("{:,}".format(int(movie_info["international_box_office"].values[0]))),
        'movie_worldwide_gross': ("{:,}".format(int(movie_info["worldwide_box_office"].values[0]))),
        'movie_budget': ("{:,}".format(int(movie_info["production_budget"].values[0]))),
        'movie_synopsis': (movie_info["synopsis"].values[0]),
        'movie_poster': (movie_info["poster_path"].values[0]),
        'movie_distributor': (movie_info["production_companies"].values[0]),
        'movie_legs': (movie_info["legs"].values[0]),
        'movie_theaters': (movie_info["theater_counts"].values[0]),
        'movie_genre': (movie_info["genre"].values[0]),
        'movie_pscore': (movie_info["bb_profit_score"].values[0]),
        'movie_mscore': (movie_info["bb_profit_multiple_score"].values[0]),
        'movie_sim_movies': (ast.literal_eval(movie_info["similar_movies"].values[0])),
        'movie_imdb_score': (movie_info["imdb_score"].values[0]),
        # 'movie_meta_score': int(round(movie_info["meta_score"].values[0])),
        'movie_imdb_id': (movie_info["tconst"]).values[0],
        'movie_slug_name': (movie_info["name_slug"].values[0]),
        'movie_domestic_share': int(movie_info["domestic_share"].values[0]),
        'movie_international_share': int(movie_info["international_share"].values[0])


    }

    average_dict = {

        'domestic_box_office': int(average_table["domestic_box_office"]),
        'international_box_office': int(average_table["international_box_office"]),
        'worldwide_box_office': int(average_table["worldwide_box_office"]),
        'opening_weekend': int(average_table["opening_weekend"]),
        'production_budget': int(average_table["production_budget"]),
        'theater_counts': int(average_table["theater_counts"]),
        'running_time': int(average_table["running_time"]),
        'imdb_score': int(average_table["imdb_score"]),
        'bb_profit': int(average_table["bb_profit"]),
        'bb_profit_score': int(average_table["bb_profit_score"]),
        'bb_score': int(average_table["bb_score"]),
        'domestic_share': int(average_table["domestic_share"]),
        'international_share': int(average_table["international_share"])

    }

    x = len(ast.literal_eval(movie_info["similar_movies"].values[0]))

    movie_dict['genre_bb'] = genre_table[genre_table.genre ==
                                         movie_dict['movie_genre']].bb_score.values[0]

    return render_template('movie_page.html', movie_data=movie_dict, labels=labels, values=values, x=x)


@app.route('/trending')
def trending():

    current_title_list = in_theateres_table["title"]
    current_poster_list = in_theateres_table["poster_path"]

    upcoming_title_list = upcoming_theateres_table["title"]
    upcoming_poster_list = upcoming_theateres_table["poster_path"]

    popular_title_list = popular_movies_table["title"]
    popular_poster_list = popular_movies_table["poster_path"]

    popular_tv_list = popular_tv_table["title"]
    popular_tv_poster_list = popular_tv_table["poster_path"]

    return render_template('trending.html', current_title_list=current_title_list, current_poster_list=current_poster_list, upcoming_poster_list=upcoming_poster_list, upcoming_title_list=upcoming_title_list, popular_title_list=popular_title_list, popular_poster_list=popular_poster_list, popular_tv_list=popular_tv_list, popular_tv_poster_list=popular_tv_poster_list)


@app.route('/charts')
def charts():

    adjusted_domestic_dict = {
        'movie_name': (all_time_adjusted_domestic["name"].values),
        'movie_year': (all_time_adjusted_domestic["year"].values),
        'movie_d_box': (all_time_adjusted_domestic["domestic_box_office"].values),
        'movie_i_box': (all_time_adjusted_domestic["international_box_office"].values),
        'movie_w_box': (all_time_adjusted_domestic["worldwide_box_office"].values)

    }

    animated_domestic_dict = {
        'movie_name': (all_time_animated_domestic["name"].values),
        'movie_year': (all_time_animated_domestic["year"].values),
        'movie_d_box': (all_time_animated_domestic["domestic_box_office"].values),
        'movie_i_box': (all_time_animated_domestic["international_box_office"].values),
        'movie_w_box': (all_time_animated_domestic["worldwide_box_office"].values)
    }
    animated_international_dict = {
        'movie_name': (all_time_animated_international["name"].values),
        'movie_year': (all_time_animated_international["year"].values),
        'movie_d_box': (all_time_animated_international["domestic_box_office"].values),
        'movie_i_box': (all_time_animated_international["international_box_office"].values),
        'movie_w_box': (all_time_animated_international["worldwide_box_office"].values)

    }
    domestic_dict = {
        'movie_name': (all_time_domestic["name"].values),
        'movie_year': (all_time_domestic["year"].values),
        'movie_d_box': (all_time_domestic["domestic_box_office"].values),
        'movie_i_box': (all_time_domestic["international_box_office"].values),
        'movie_w_box': (all_time_domestic["worldwide_box_office"].values)

    }
    international_dict = {
        'movie_name': (all_time_international["name"].values),
        'movie_year': (all_time_international["year"].values),
        'movie_d_box': (all_time_international["domestic_box_office"].values),
        'movie_i_box': (all_time_international["international_box_office"].values),
        'movie_w_box': (all_time_international["worldwide_box_office"].values)

    }
    worldwide_dict = {
        'movie_name': (all_time_worldwide["name"].values),
        'movie_year': (all_time_worldwide["year"].values),
        'movie_d_box': (all_time_worldwide["domestic_box_office"].values),
        'movie_i_box': (all_time_worldwide["international_box_office"].values),
        'movie_w_box': (all_time_worldwide["worldwide_box_office"].values)

    }
    print(domestic_dict)
    return render_template('charts.html', adjusted_domestic_dict=adjusted_domestic_dict, domestic_dict=domestic_dict, animated_domestic_dict=animated_domestic_dict, animated_international_dict=animated_international_dict, international_dict=international_dict, worldwide_dict=worldwide_dict)


@app.route('/about_us')
def about_us():

    return render_template('about_us.html')


@app.route('/charts/domestic_charts')
def domestic_charts():

    domestic_dict = {
        'movie_name': (all_time_domestic["name"].values),
        'movie_year': (all_time_domestic["year"].values),
        'movie_d_box': (all_time_domestic["domestic_box_office"].values),
        'movie_i_box': (all_time_domestic["international_box_office"].values),
        'movie_w_box': (all_time_domestic["worldwide_box_office"].values)
    }

    return render_template('all_time_domestic.html', domestic_dict=domestic_dict)


@app.route('/charts/domestic_charts_adjusted')
def domestic_charts_adjusted():

    adjusted_domestic_dict = {
        'movie_name': (all_time_adjusted_domestic["name"].values),
        'movie_year': (all_time_adjusted_domestic["year"].values),
        'movie_d_box': (all_time_adjusted_domestic["domestic_box_office"].values),
        'movie_i_box': (all_time_adjusted_domestic["international_box_office"].values),
        'movie_w_box': (all_time_adjusted_domestic["worldwide_box_office"].values)
    }

    return render_template('domestic_adjusted.html', adjusted_domestic_dict=adjusted_domestic_dict)


@app.route('/charts/domestic_charts_animated')
def domestic_charts_animated():

    animated_domestic_dict = {
        'movie_name': (all_time_animated_domestic["name"].values),
        'movie_year': (all_time_animated_domestic["year"].values),
        'movie_d_box': (all_time_animated_domestic["domestic_box_office"].values),
        'movie_i_box': (all_time_animated_domestic["international_box_office"].values),
        'movie_w_box': (all_time_animated_domestic["worldwide_box_office"].values)
    }

    return render_template('domestic_animated.html', animated_domestic_dict=animated_domestic_dict)


@app.route('/charts/international_charts')
def international_charts():

    international_dict = {
        'movie_name': (all_time_international["name"].values),
        'movie_year': (all_time_international["year"].values),
        'movie_d_box': (all_time_international["domestic_box_office"].values),
        'movie_i_box': (all_time_international["international_box_office"].values),
        'movie_w_box': (all_time_international["worldwide_box_office"].values)
    }

    return render_template('all_time_international.html', international_dict=international_dict)


@app.route('/charts/international_charts_animated')
def international_charts_animated():

    animated_international_dict = {
        'movie_name': (all_time_animated_international["name"].values),
        'movie_year': (all_time_animated_international["year"].values),
        'movie_d_box': (all_time_animated_international["domestic_box_office"].values),
        'movie_i_box': (all_time_animated_international["international_box_office"].values),
        'movie_w_box': (all_time_animated_international["worldwide_box_office"].values)
    }

    return render_template('international_animated.html', animated_international_dict=animated_international_dict)


@app.route('/charts/worldwide_charts')
def worldwide_charts():

    worldwide_dict = {
        'movie_name': (all_time_worldwide["name"].values),
        'movie_year': (all_time_worldwide["year"].values),
        'movie_d_box': (all_time_worldwide["domestic_box_office"].values),
        'movie_i_box': (all_time_worldwide["international_box_office"].values),
        'movie_w_box': (all_time_worldwide["worldwide_box_office"].values)
    }

    return render_template('all_time_worldwide.html', worldwide_dict=worldwide_dict)


if __name__ == '__main__':
    app.run(debug=True)
