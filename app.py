from flask import Flask, render_template, redirect
from function import insert_product, update_product, delete_product, query_with_fetchall

app = Flask(__name__)

@app.route('/')
def index():
    stocks = query_with_fetchall()  # 재고 목록 조회
    return render_template('stock_list.html', stocks=stocks)

@app.route('/insert/<name>/<barcode>')
def insert(name, barcode):
    insert_product(name, barcode)  # 새 재고 추가
    return redirect('/')

@app.route('/update/<int:id>/<name>')
def update(id, name):
    affected_rows = update_product(id, name)  # 재고 정보 수정
    print(f'Number of affected rows: {affected_rows}')
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    affected_rows = delete_product(id)  # 재고 삭제
    print(f'Number of affected rows: {affected_rows}')
    return redirect('/')

if __name__ == '__main__':  
    app.run(debug=True)
