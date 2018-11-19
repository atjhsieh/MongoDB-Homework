
# coding: utf-8

# In[ ]:


from flask import Flask, render_template
import pymongo
from scrape_mars import scrape


# In[ ]:


mars = scrape()


# In[ ]:


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dblist = myclient.list_database_names()
if "mydatabase" in dblist:
    mydb = myclient["AHsieh_Database"]
else:
    mydb = myclient["mydatabase"]
mycol = mydb["Mars"]
x = mycol.insert_one({"data":mars})


# In[ ]:


app = Flask(__name__)

@app.route("/scrapes")
def scrapes():
    return mars

@app.route("/")
def rootfcn():
    x = mycol.update_one("data",mars)
    return render_template('index.html', x)

if __name__ == "__main__":
    app.run(debug=True)

