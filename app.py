import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, request, url_for, redirect, jsonify
from botocore.config import Config
import psycopg2
import sys
import boto3
import urllib

app = Flask(__name__)

ENDPOINT=os.environ['RDSHOST']
DBNAME=os.environ['DB_DBNAME']
PORT=os.environ['DB_PORT']
USER=os.environ['DB_USERNAME']
#password=os.environ['DB_PASSWORD']
PGPASSWORD=os.environ['PGPASSWORD']
REGION=os.environ['AWS_REGION']

my_config = Config(
    region_name = 'eu-west-1'
)

#session = boto3.Session()
client = boto3.client('rds', config=my_config)

token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

PASSWD= urllib.parse.quote_plus(token)

url = "postgresql://"+USER+":"+PASSWD+"@"+ENDPOINT+"/"+DBNAME+"?sslmode=require"

#url = "postgresql://"+USER+":password@"+ENDPOINT+":"+PORT+"/"+DBNAME
#url = "postgresql://"+user+"@"+host+"/"+dbname

engine = create_engine(url)

db = scoped_session(sessionmaker(bind=engine))



@app.route('/db')
def index():

        books = db.execute('SELECT * FROM books;')

        return render_template('index.html', books=books)



@app.route('/db/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']

        db.execute("INSERT INTO books (title, author, pages_num, review) VALUES (:title, :author, :pages_num, :review)",
                    {"title": title, "author": author, "pages_num": pages_num, "review": review})
        db.commit()

        return redirect(url_for('index'))

    return render_template('create.html')

@app.route("/db/bookDelete/<int:bookid>")
def bookDelete(bookid):

    #create delete query as string

    strSQL="delete from books where id="+str(bookid)
    db.execute(strSQL)
    #commit to database
    db.commit()
    return  render_template('delete.html')


@app.route('/db/API_number_of_books/')
def API_number_of_books():
    result=db.execute('SELECT count(*) FROM books;').scalar()
    number_of_books=str(result)
    return jsonify(number_of_books=number_of_books)
