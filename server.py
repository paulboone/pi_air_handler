from bottle import route, run, template, get, request
from air_handler.utils import switch_air_handler, load_config, parse_runstate, write_runstate

@route('/')
def index():
    return "control template here"

@route('/fan/<turn_on>')
def fan(turn_on):
    state = parse_runstate(turn_on)
    config = load_config()

    if not config['debug_no_GPIO']:
        switch_air_handler(state != 0, config['relay_num'])
    else:
        print("debuging is on; not attempting GPIO switch")

    write_runstate(state)

    return template('<b>Hello {{name}}</b>!', name=turn_on)

run(port=8080)
