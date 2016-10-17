from src import (
    User,
    Katalk,
    engine,
)
from flask import Flask, render_template, jsonify
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
app = Flask(__name__, template_folder='templates')


@app.route("/user")
def hello():
    return render_template('user_count.html')


@app.route("/api/user")
def api_user():
    s = Session()
    users = s.query(User).all()
    arr = []
    for user in users:
        d = dict(name=user.name, y=s.query(Katalk).filter_by(user=user).count())
        arr.append(d)
    return jsonify(arr)


if __name__ == "__main__":
    import sys

sys.path.append('src')  # for alembic
app.run()
