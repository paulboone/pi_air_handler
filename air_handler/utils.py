import yaml
import os

def switch_air_handler(air_handler_on, relay_num):
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_num, GPIO.OUT)

    if air_handler_on:
        GPIO.output(relay_num, GPIO.HIGH)
    else:
        GPIO.output(relay_num, GPIO.LOW)


def load_config(file_name="config.yaml"):
    with open(file_name) as config_file:
         config = yaml.load(config_file)

    return config

def parse_runstate(turn_on):
    if turn_on in ["2", "auto"]:
        state = 2
    elif turn_on in ["1", "on"]:
        state = 1
    elif turn_on in ["0", "off"]:
        state = 0
    else:
        raise("bad runstate")
    return state

def human_runstate(state):
    if state == 2:
        return "AUTO"
    elif state == 1:
        return "ON"
    elif state == 0:
        return "OFF"
    else:
        return "UNKNOWN"

def write_runstate(state, filename="runstate.txt"):
    with open(filename, 'w') as f:
        f.write(str(state))

def load_runstate(filename="runstate.txt"):
    if not os.path.isfile(filename):
        return 2 # AUTO

    with open(filename, 'r') as f:
        state = int(f.read())

    return state
