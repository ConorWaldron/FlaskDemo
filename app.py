from flask import Flask, render_template

app = Flask(__name__)

# dummy data to demonstrate Jinja in HTML templates
title_string = "Conor's Flask App"
example_blogs = [
    {'author': "Conor Waldron",
     'title': 'How to build a tennis dash app',
     'content': 'dash is really useful to make web apps that you can deploy with docker on AWS...',
     'date_posted': '20th Nov 2023'},
    {'author': "Leo Kavanagh",
     'title': 'Functional Programming',
     'content': 'Functional Programming is like making a tirimisu...',
     'date_posted': '16th Feb 2022'},
]

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', posts=example_blogs, title=title_string)

@app.route('/about')
def about_page():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)