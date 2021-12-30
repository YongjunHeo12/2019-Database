import sqlite3

from flask import Flask, render_template, g
from flask.globals import request

DEBUG = False
DATABASE = 'Youtube.db'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()
    
def teardown_request(exception):
    g.db.close()

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/main')
def main():
   
    return render_template("main.html")

@app.route('/Table')
def Table():
     
    if request.method == 'GET':
        category = request.args.get('category')
    
    tag_list_1 = []
    tag_list_10 = []
    tag_list_20 = []
    
    top5_list_1 = []
    top5_list_10 = []
    top5_list_20 = []
    
    cur1 = g.db.execute('select tag1 from top20_tag1_cnt limit 20')
    cur10 = g.db.execute('select tag10 from top20_tag10_cnt limit 20')
    cur20 = g.db.execute('select tag20 from top20_tag20_cnt limit 20')
    
    for i in cur1.fetchall():
        tag_list_1.append(i[0])
        
    for j in cur10.fetchall():   
        tag_list_10.append(j[0])
        
    for k in cur20.fetchall():   
        tag_list_20.append(k[0])
    
    
    
    
    top5_1 = g.db.execute('select title, channel_title, views, likes, dislikes from top5_1')
    top5_10 = g.db.execute('select title, channel_title, views, likes, dislikes from top5_10')
    top5_20 = g.db.execute('select title, channel_title, views, likes, dislikes from top5_20')
    
 
    for a in top5_1.fetchall():
        buf_list =[]
        buf_list.append(a[0]) #title
        buf_list.append(a[1]) #channel_title
        buf_list.append(a[2]) #views
        buf_list.append(a[3]) #likes
        buf_list.append(a[4]) #dislikes
        top5_list_1.append(buf_list)

    for b in top5_10.fetchall():
        buf_list =[]
        buf_list.append(b[0]) #title
        buf_list.append(b[1]) #channel_title
        buf_list.append(b[2]) #views
        buf_list.append(b[3]) #likes
        buf_list.append(b[4]) #dislikes
        top5_list_10.append(buf_list)
        
    for c in top5_20.fetchall():
        buf_list =[]
        buf_list.append(c[0]) #title
        buf_list.append(c[1]) #channel_title
        buf_list.append(c[2]) #views
        buf_list.append(c[3]) #likes
        buf_list.append(c[4]) #dislikes
        top5_list_20.append(buf_list)        
        


    print(tag_list_1[0])
    return render_template("Table.html", top5_list_1= top5_list_1, top5_list_10= top5_list_10,top5_list_20= top5_list_20,category = category,  tag_list_1 = tag_list_1,tag_list_10 = tag_list_10, tag_list_20 = tag_list_20)

@app.route('/info')
def info():
    
    if request.method =='GET':
        publish_time= request.args.get('publish_time')
        tag = request.args.get('tag')
        category = request.args.get('category')
    
    tag_cnt_1 =[]
    tag_cnt_10=[]
    tag_cnt_20=[]
    cur1_cnt = g.db.execute('select tag_cnt from top20_tag1_cnt limit 20')
    cur10_cnt = g.db.execute('select tag_cnt from top20_tag10_cnt limit 20')
    cur20_cnt = g.db.execute('select tag_cnt from top20_tag20_cnt limit 20')
    
    for a in cur1_cnt.fetchall():
        tag_cnt_1.append(a[0])
        
    for b in cur10_cnt.fetchall():   
        tag_cnt_10.append(b[0])
        
    for c in cur20_cnt.fetchall():   
        tag_cnt_20.append(c[0])
    return render_template("info.html", publish_time = publish_time, tag = tag, category=category, tag_cnt_1 = tag_cnt_1,tag_cnt_10 = tag_cnt_10,tag_cnt_20 = tag_cnt_20)


      
if __name__ == '__main__':
    app.run()
