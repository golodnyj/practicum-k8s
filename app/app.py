from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import socket
import os

app = Flask(__name__, template_folder="templates")

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

db = SQLAlchemy(app, engine_options={'connect_args': {
    'sslmode': 'require',
    'host': os.environ['DATABASE_HOSTS'],
    'port': 6432,
    'target_session_attrs': 'read-write',
}})


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)


UNAVAILABLE = ("unavailable", 503)
LIGHT_MODE = "light"
DARK_MODE = "dark"

# Defines Load Balancer health check result. if False, /alive handler will return 503
alive = True
# Defines Instance Group health check result. if False, /healthy handler will return 503
healthy = True
# Defines color scheme of the app
mode = LIGHT_MODE
if 'COLOR_SCHEME' in os.environ:
    mode = os.environ['COLOR_SCHEME']


# Main page
@app.route('/')
def index():
    if not healthy:
        return UNAVAILABLE

    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()

    return render_template('index.html',
                           incomplete=incomplete, complete=complete, hostname=socket.gethostname(), mode=mode)


# List all incomplete items
@app.route('/list')
def list_incomplete():
    if not healthy:
        return UNAVAILABLE
    incomplete = Todo.query.filter_by(complete=False).all()
    return str([todo.text for todo in incomplete])


# List all completed items
@app.route('/completed')
def list_completed():
    if not healthy:
        return UNAVAILABLE
    completed = Todo.query.filter_by(complete=True).all()
    return str([todo.text for todo in completed])


# Add new item
@app.route('/add', methods=['POST'])
def add():
    if not healthy:
        return UNAVAILABLE
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()

    # Makes to stay on the same home page######
    return redirect(url_for('index'))


# Complete item
@app.route('/complete/<id>')
def complete(id):
    if not healthy:
        return UNAVAILABLE
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    # Makes to stay on the same home page
    return redirect(url_for('index'))


# Load Balancer health check handler
@app.route('/alive')
def hc_alive():
    if alive:
        return "alive", 200
    else:
        return UNAVAILABLE


@app.route('/switch_alive', methods=['POST'])
def switch_alive():
    global alive
    alive = not alive
    return "now alive = {}".format(alive)


# Instance Group health check handler
@app.route('/healthy')
def hc_healthy():
    if healthy:
        return "healthy", 200
    else:
        return UNAVAILABLE


@app.route('/switch_healthy', methods=['POST'])
def switch_healthy():
    global healthy
    healthy = not healthy
    return "now healthy = {}".format(healthy)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=80)
