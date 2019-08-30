from bottle import route, run, template, get, request
from air_handler.utils import switch_air_handler, load_config

@route('/')
def index():
    return "control template here"

@route('/fan/<turn_on>')
def fan(turn_on):
    turn_on = turn_on in ["1", "on"]

    config = load_config()
    if not config['debug_no_GPIO']:
        switch_air_handler(turn_on, config['relay_num'])
    else:
        print("debuging is on; not attempting GPIO switch")

    return template('<b>Hello {{name}}</b>!', name=turn_on)

run(host='localhost', port=8080)
