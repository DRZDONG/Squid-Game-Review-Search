from flask import Flask, render_template, request, app
from flask_bootstrap import Bootstrap
import elastic
import tokenizer

app = Flask(__name__)
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def get():
    queries = []
    if request.method == 'POST':
        query = request.form.get('query')
        choice = request.form['flexRadioDefault']
        if choice == '1':
            result = elastic.search(query)
            print(choice)
        else:
            result = elastic.exact_match_search(query)
            print(choice)
        return render_template('index.html', queries=queries, result=result)
    return render_template('index.html', queries=queries)


if __name__ == '__main__':
    app.run(debug=True)

