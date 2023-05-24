#!/usr/bin/python3
"""script that starts a Flask web application
"""

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Returns greeting
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Return hbnb
    """
    return 'HBNB'

@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Return C_text
    """
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """Return Python Text
    """
    return 'Python {}'.format(text.replace('_',' '))


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """Returns whether number or not
    """
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def cast_number(n):
    """Returns an html docstring with the number cast onto it
    """
    path = '5-number.html'
    return render_template(path, n=n)

@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def odd_or_even(n):
    """Returns whether a number is odd or even
    """
    path = '6-number_odd_or_even.html'
    if n % 2 == 0:
        result = 'even'
    else:
        result = 'odd'
    return render_template(path, n=n, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
