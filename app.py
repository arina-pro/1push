import json
import flask

app = flask.Flask(__name__, static_url_path='', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def get_json():
    return flask.redirect(flask.url_for('test'))


@app.route('/get-event', methods=['GET'])
def get_event():
    frame = int(flask.request.values['frame'])
    with open('response.json') as f:
        db = json.load(f)
    response = []

    for event in db['Events']:
        if event['FrameNumber'] == frame:
            response.append(event)

    return json.dumps(response)


@app.route('/get-response', methods=['GET'])
def get_response():
    with open('response.json') as f:
        db = json.load(f)
    response = dict()
    for i in range(10):
        response[f'player_{i}'] = dict()
        response[f'player_{i}']['X'] = db['PlayersPositions'][i]['X']
        response[f'player_{i}']['Y'] = db['PlayersPositions'][i]['Y']
    response['RoundStartState'] = dict()
    for i in range(10):
        response['RoundStartState'][f'player_{i}'] = db['RoundStartState']['Players'][i]['AdditionalInfo']
        response['RoundStartState'][f'player_{i}']['Money'] = db['RoundStartState']['Players'][i]['Money']

    return response


@app.route('/test', methods=['GET'])
def test():
    return flask.render_template('test.html')


if __name__ == '__main__':
    app.run()
