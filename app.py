from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list', methods=["GET", "POST"])
def list():
    if request.method == "POST":
        return "POST on /list"
    else:
        return "GET on /list"

@app.route('/list/<id>', methods=["GET", "PUT", "DELETE"])
def list_id(id):
    if request.method == "PUT":
        return f"PUT on /list/{id}"
    elif request.method == "DELETE":
        return f"DELETE on /list/{id}"
    else:
        return f"GET on /list/{id}"

if __name__ == '__main__':
    app.run(host='localhost',
            port=5000,
            debug=True)
