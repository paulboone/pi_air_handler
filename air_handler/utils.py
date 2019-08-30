import yaml

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
