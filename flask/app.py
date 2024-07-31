from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tab/<int:tab_id>')
def tab(tab_id):
    return render_template(f'tab{tab_id}.html', title=f'Tab {tab_id}')

if __name__ == '__main__':
    app.run(debug=True)