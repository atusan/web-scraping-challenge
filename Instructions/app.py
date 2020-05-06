from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars_app = mongo.db.collection.find_one()
    return render_template("index.html",mars_app=mars_app)


@app.route("/scrape")
def scrape():
    mars_app = mongo.db.mars_app
    data = scrape_mars.getData()
    mars_app.update({}, data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
