from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def main():
    app.run(debug=True, port=1234, host="0.0.0.0")


if __name__ == '__main__':
    main()
