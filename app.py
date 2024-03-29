from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    mars_info = scrape_mars.scrape_mars_news()
    mars_info = scrape_mars.scrape_mars_image()
    mars_info = scrape_mars.scrape_mars_weather()
    mars_info = scrape_mars.scrape_mars_facts()
    mars_data.update({}, mars_info, upsert=True)

    return redirect("/", code=302)

if __name__=="__main__":
    app.run(debug=True)
