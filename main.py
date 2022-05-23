# -----------------------------------------------------------
# Demonstrates the application, which loads any csv file and
# this file should contain address column in it, according to that,
# program will generate new csv file with latitude and longitude of that address
# This web app has been developed using flask.
#
# email dhruvdave61@gmail.com
# ----------------------------------------------------------

import geopy
from flask import Flask, render_template, request, send_file
from geopy.geocoders import Nominatim
import pandas as pd

app = Flask(__name__)


# loads initial index page of the app
@app.route("/")
def index():
    return render_template("index.html")


# success page generates new csv file with 2 new columns
@app.route("/success", methods=['POST'])
def success():
    # global variable to store new file in it
    global filename
    if request.method == 'POST':
        file = request.files["file"]
        try:
            df = pd.read_csv(file)
            geopy.geocoders.options.default_user_agent = "main"
            gc = Nominatim()
            # check the address column is there in the csv file or not
            df['location'] = df['Address'].apply(gc.geocode)

            # adding latitude and longitude column according to the address
            df['Latitude'] = df['location'].apply(lambda x: x.latitude if x != None else None)
            df['Longitude'] = df["location"].apply(lambda x: x.longitude if x != None else None)

            df = df.drop("location", 1)
            filename = "data.csv"

            # generates updated file with two new columns
            df.to_csv(filename, index=None)
            return render_template("index.html", text=df.to_html(), btn='download.html')
        except:
            return render_template("index.html", text="please enter the valid file")

# with download page we can download that updated file
@app.route("/download")
def download():
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.debug = True
    app.run()
