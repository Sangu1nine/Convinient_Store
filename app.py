from flask import Flask, render_template, redirect
from fetchall import fetch_all_stocks
from insertData import insert_stock
from updateData import update_stock
from deleteData import delete_stock

app = Flask(__name__)

@app.route('/')
def index():
    stocks = fetch_all_stocks()  # 재고 목록 조회
    return render_template('stock_list.html', stocks=stocks)

@app.route('/insert/<name>/<barcode>')
def insert(name, barcode):
    insert_stock(name, barcode)  # 새 재고 추가
    return redirect('/')

@app.route('/update/<int:id>/<name>')
def update(id, name):
    affected_rows = update_stock(id, name)  # 재고 정보 수정
    print(f'Number of affected rows: {affected_rows}')
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    affected_rows = delete_stock(id)  # 재고 삭제
    print(f'Number of affected rows: {affected_rows}')
    return redirect('/')

if __name__ == '__main__':  
    app.run(debug=True)
