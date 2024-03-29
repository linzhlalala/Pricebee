from CrlEntry import MainSearchItem 
from flask import Flask, render_template, request 

#import csv

app = Flask(__name__) 

@app.route('/') 
def entry_page() -> 'html': 
    return render_template('entry.html',the_title='Welcome to PriceBee!') 

@app.route('/compare', methods=['POST']) 

def search_products() -> str:
    word = request.form['word']
    title = 'Search result' 
    titles = ('Product', 'Price', 'Discount', 'Unit Price', 'At') 
    results = MainSearchItem(word) 

    return render_template('results.html',
        the_word=word,
        the_title=title,
        the_row_titles=titles,
        the_data=results) 




