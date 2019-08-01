from flask import Flask, escape, request, render_template
import random
import requests
from bs4 import BeautifulSoup
import csv

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')
    # html문서에는 현재 파이썬코드 CSS가 들어있는 HTML파일이 아닌 수준임
    #하지만 render_template가 있으면 이를 우리가 볼 수 있게 변환을 해줌!?

@app.route('/lotto')
def lotto():
    numbers = random.sample(range(1, 46), 6)
    print(numbers)
    return render_template('lotto.html', numbers=numbers)

@app.route('/lunch')
def lunch():
    menus = {
        '중국':'간짜장',
        '양식':'돈가스',
        '한식':'비빔밥',
        '분식':'떡볶이'
    }
    return render_template('lunch.html', menus=menus)
    
@app.route('/opgg')
def opgg():
    return render_template('opgg.html')

@app.route('/search')
def search():
    opgg_url = "https://www.op.gg/summoner/userName="
    summoner = request.args.get('summoner')
    url = opgg_url + summoner

    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    tier = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierRank')
    user_tier = tier.text.strip()

    return render_template('search.html', user_tier=user_tier, summoner=summoner)

@app.route('/nono')
def nono():
    with open('data.csv', 'r' ,encoding='utf-8') as f:
        reader = csv.reader(f)
        products = list(reader)
    return render_template('nono.html', products=products)

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/create')
def create():
    product = request.args.get('product')
    category = request.args.get('category')
    replace = request.args.get('replace')

    with open('data.csv','a+', encoding='utf-8', newline='')as f:
        writer = csv.writer(f)
        product_info = [product, category, replace]
        writer.writerow(product_info)

    return render_template('create.html')

@app.route('/card')
def card():
    with open('data.csv', 'r' ,encoding='utf-8') as f:
        reader = csv.reader(f)
        products = list(reader)
    return render_template('card.html', products=products)

if __name__=="__main__":
    app.run(debug=True)