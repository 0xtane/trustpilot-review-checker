from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def check_review_exists(website_url, target_review, author_name):
    base_url = "https://www.trustpilot.com/review/"
    target_url = base_url + website_url

    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    reviews = soup.find_all('article', {'class': 'paper_paper__1PY90'})

    for review in reviews:
        review_text = review.find('p', {'class': 'typography_body-l__KUYFJ'}).text
        name = review.find('span', {'class': 'typography_heading-xxs__QKBS8'}).text
        

        if target_review in review_text and author_name == name:
            return True

    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    form_data = {'url': 'gumroad.com', 'target_review': 'The seller here takes the code from pirated code sharing sites and sells it, scam.', 'target_author': 'Kaovodich'}

    if request.method == 'POST':
        form_data['url'] = request.form.get('url')
        form_data['target_review'] = request.form.get('target_review')
        form_data['target_author'] = request.form.get('target_author')

        result = check_review_exists(form_data['url'], form_data['target_review'], form_data['target_author'])

    return render_template('index.html', result=result, form_data=form_data)


if __name__ == '__main__':
    app.run(debug=True)
