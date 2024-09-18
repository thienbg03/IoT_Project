from flask import Flask, render_template
import datetime

app = Flask(__name__)

led_pin = (17)

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, LOW)

@app.route('/on')
def on():
  GPIO.output(led_pin, HIGH)
  return render_template('on.html')

@app.route('/off')
def off():
  GPIO.output(led_pin, LOW)
  return render_template('off.html')

@app.route('/')

def index():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
      'title' : 'Hello',
      'time': timeString
      }
    return render_template('index.html', **templateData)

#REPPLACE IP Address with ur Pi address
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')