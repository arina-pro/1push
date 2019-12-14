import json
import flask

app = flask.Flask(__name__, static_url_path='', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def get_json():
    return 'Empty'


@app.route('/get-response', methods=['GET'])
def get_response():
    with open('response.json') as f:
        db = json.load(f)
    response = dict()
    for i in range(len(db['PlayersPositions'])):
        response[f'player_{i}'] = dict()
        response[f'player_{i}']['X'] = db['PlayersPositions'][i]['X']
        response[f'player_{i}']['Y'] = db['PlayersPositions'][i]['Y']

    return response


@app.route('/test', methods=['GET'])
def test():
    return flask.render_template('test.html')


if __name__ == '__main__':
    app.run()
