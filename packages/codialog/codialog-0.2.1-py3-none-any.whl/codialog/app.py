from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route('/api/data')
def get_data():
    data = {
        "message": "Hello from Flask!"
    }
    return jsonify(data)



def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('index.html')

    return app

def run():
    app = create_app()
    app.run(host='0.0.0.0', port=8081, debug=True)

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8081, debug=True)


