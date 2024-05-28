from flask import Flask, render_template, request, make_response, redirect, url_for, session, abort

app = Flask(__name__)
app.secret_key = 'loolkeekcheebuureek'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    print(session)
    return render_template('about.html')

@app.route('/contact')
def contact():
    contacts=[{"name":'Batyr', 'number': '8 701 152 52-64'}]
    return render_template('contact.html', contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)