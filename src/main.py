from flask import Flask, request, render_template
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

red_pin = 26
green_pin = 19
blue_pin = 13

GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)

red_pwm=GPIO.PWM(red_pin,1000)
blue_pwm=GPIO.PWM(blue_pin,1000)
green_pwm=GPIO.PWM(green_pin,1000)

red_pwm.start(0)
blue_pwm.start(0)
green_pwm.start(0)

current_color = '#FFFFFF'

app = Flask(__name__)

def hex_to_rgb(h):
    h = h.strip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def ard_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setLED(h):
    rgb_vals = hex_to_rgb(h)
    red_pwm.ChangeDutyCycle(ard_map(rgb_vals[0], 0, 255, 0, 100))
    green_pwm.ChangeDutyCycle(ard_map(rgb_vals[1], 0, 255, 0, 100))
    blue_pwm.ChangeDutyCycle(ard_map(rgb_vals[2], 0, 255, 0, 100.0))

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_color
    if request.method == 'POST':
        current_color = request.form.get('led_color')
        setLED(current_color)
        return render_template('index.html', current_color=current_color)
    else:
        return render_template('index.html', current_color=current_color)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
