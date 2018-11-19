from flask import Flask, render_template, jsonify, redirect
import pymongo
from pymongo import MongoClient
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

client = pymongo.MongoClient(conn)
collection = db.mars

@app.route("/")
def home(): 

    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape(): 

    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_mars()
    mars_data = scrape_mars.scrape_img()
    mars_data = scrape_mars.weather()
    mars_data = scrape_mars.scrape_facts()
    mars_data = scrape_mars.scrape_hemi()
    mars.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)