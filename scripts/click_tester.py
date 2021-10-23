import click
import requests
import json
from datetime import datetime
import webbrowser
from six.moves import urllib


@click.command()
@click.option('--number', '-n', default=.05405007, help='Number of selected currency (btc by default).')
@click.option('--pct/--no-pct', default=False, help="Show gain in percent")
def btc(number, pct):
    url = "https://data.messari.io/api/v1/assets"
    btc = requests.get(url)
    btc_json = btc.json()
    data = btc_json['data'][0]['metrics']['market_data']['price_usd']
    my_btc = number
    my_value = int(data * my_btc)
    verbage = "lost"
    change = int(1000 - my_value)
    verbage2 = " dollars"
    if my_value > 1000:
        change = int(my_value - 1000)
        verbage = "gained"
    if pct:
        verbage2 = " percent"
        if my_value > 1000:
            verbage = "gained"
            change = int(my_value - 1000) / 1000 * 100
        if my_value < 1000:
            verbage = "lost"
            change = int(1000 - my_value) / 1000 * 100

    if number != .05405007:
        print(str(number) + " bitcoins are currently valued at " +
              str(int(my_value)))
        exit()
    print(str(number) + " bitcoins are currently valued at " + str(int(my_value)
                                                                   ) + ". You have " + verbage + " " + str((change)) + verbage2 + ".")


if __name__ == '__main__':
    btc()
