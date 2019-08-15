from flask import Flask, render_template, url_for

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def home():
    context = {
        'posts': []
    }
    return render_template('home.html', **context)


@app.route('/about')
def about():
    return render_template('about.html')
