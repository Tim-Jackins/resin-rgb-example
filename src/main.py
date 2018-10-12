from flask import Flask, request, render_template
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

red_pin = 26
blue_pin = 13
green_pin = 19

GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)

red_pwm=GPIO.PWM(red_pin,1000)
blue_pwm=GPIO.PWM(blue_pin,1000)
green_pwm=GPIO.PWM(green_pin,1000)

red_pwm.start(0)
blue_pwm.start(0)
green_pwm.start(0)

red_bright = 100
blue_bright = 100
green_bright = 100

app = Flask(__name__)#, template_folder = 'src/templates')

def hex_to_rgb(h):
    h = h.strip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def ard_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        current_color = request.form.get('led_color')
        red_bright, green_bright, blue_bright = hex_to_rgb(current_color)
        red_pwm.ChangeDutyCycle(ard_map(red_bright, 0, 255, 0.0, 100.0))
        green_pwm.ChangeDutyCycle(ard_map(green_bright, 0, 255, 0.0, 100.0))
        blue_pwm.ChangeDutyCycle(ard_map(blue_bright, 0, 255, 0.0, 100.0))
        #print(current_color)
        return render_template('index.html', current_color=current_color)
    else:
        current_color = '#FFFFFF'
        red_bright, green_bright, blue_bright = hex_to_rgb(current_color)
        red_pwm.ChangeDutyCycle(ard_map(red_bright, 0, 255, 0.0, 100.0))
        green_pwm.ChangeDutyCycle(ard_map(green_bright, 0, 255, 0.0, 100.0))
        blue_pwm.ChangeDutyCycle(ard_map(blue_bright, 0, 255, 0.0, 100.0))
        return render_template('index.html', current_color=current_color)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
