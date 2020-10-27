from flask import Flask, render_template
app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    # return "<h1>404 Error</h1>", 404
    return render_template('404.html'), 404


@app.route("/")
def hello():                           
    return render_template('index.html')

@app.route('/survey')
def survey():
    return render_template('survey.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080")