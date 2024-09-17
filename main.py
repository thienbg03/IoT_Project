from flask import Flask, render_template
import datetime

app = Flask(__name__)

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
    app.run(host='IP Address', port='8000')