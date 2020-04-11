from app import app
from flask import render_template, url_for

@app.route('/')
@app.route('/index/')
def index():
     
    return render_template('index.html')


@app.route('/movie_list')
def movie_list():

    complete_movie_list = ["Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame","Joker", "Frozen 2", "Avengers: Endgame"]

    return render_template('movie_list.html', complete_movie_list = complete_movie_list)


@app.route('/movie_page')
def movie_page():

    movie_dict = {

    'movie_score' : 92,
    'movie_mpaa_rating' : 'R',
    'movie_runtime' : '2h 2min',
    'movie_title' : 'Joker',
    'movie_year' : '(2019)',
    'movie_opening_weekend': '$96,202,337',
    'movie_domestic_gross' : '$332,224,446',
    'movie_international_gross': '$738,792,258',
    'movie_worldwide_gross' : '$1,055,824,446',
    'movie_budget' : '$62,500,000',
    'movie_synopsis' : 'During the 1980s, a failed stand-up comedian is driven insane and turns to a life of crime and chaos in Gotham City while becoming an infamous psychopathic crime figure.'
    

    }


    return render_template('movie_page.html', movie_data = movie_dict)   



if __name__ == '__main__':
   app.run(debug = True)
