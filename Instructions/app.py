from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    final_report = mongo.db.final_report.find_one()
    return render_template("index.html", final_report=final_report)


# @app.route("/scrape")
# def scrape():
#     final_report = mongo.db.final_report
#     # mars_data = scrape_mars.scrape()
#     mars_data = scrape_mars.scrape_mars_news()
#     mars_data = scrape_mars.scrape_jpl()
#     mars_data = scrape_mars.scrape_mars_weather()
#     mars_data = scrape_mars.scrape_mars_facts()
#     mars_data = scrape_mars.scrape_mars_hemispheres()
#     final_report.update({}, mars_data, upsert=True)
#     return redirect("/", code=302)


@app.route("/scrape")
def scrape():
    final_report = mongo.db.final_report 
    mars_data = scrape_mars.scrape()
    final_report.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
