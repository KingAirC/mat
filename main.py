from matrix_resolve import MatrixResolver
from flask import Flask, jsonify
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/row_simple', methods=['POST'])
def row_simple():
    s = request.form.get('mat')

    mat = eval(s)

    result = MatrixResolver(mat).result

    print(result)

    return jsonify(str(result))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)
