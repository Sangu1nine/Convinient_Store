# 1. 도서 추가
from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser

def read_config(filename='app.ini', section='mysql'):
    config = ConfigParser()
    config.read(filename)
    data = {}
    if config.has_section(section):
        items = config.items(section)
        for item in items:
            data[item[0]] = item[1]
    else:
        raise Exception(f'{section} section not found in the {filename} file')
    return data

def connect():
    conn = None
    config = read_config()
    try:
        print('MYSQL 데이터베이스에 연결 중...')
        conn = MySQLConnection(**config)
        if conn.is_connected():
            print('Connection is established.')
        else:
            print('Connection is failed.')
    except Error as error:
        print(error)
    return conn

def query_with_fetchall(conn):

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        print('Total Row(s):', cursor.rowcount)

        for row in rows:
            print(row)
        return rows

    except Error as e:
        print(e)

def insert_product(conn, products):
    query1 = '''INSERT INTO products(product_name, barcode, price, quantity, expiration_day)
                VALUES(%s, %s, %s, %s, %s)'''
    query2 = """UPDATE products
            SET quantity = %s
            WHERE product_name = %s"""
    product_id = None    
    try:
        while True :
            product_name = input('상품명을 입력하세요>>>').strip(" ,.:").lower()
            quantity = input('입고 수량을 입력하세요>>>').strip(" ,.:").lower()
            args2 = (quantity, product_name)
            if quantity.isnumeric():  # 숫자인지 확인
                quantity = int(quantity)  # 숫자로 변환
                break
            else :
                print("숫자만 입력해주세요!")  # 숫자가 아니면 다시 입력 요청
        found = False  # 우선적으로 책 검색
        for product in products: # 도서관에 이미 있던 도서명과 일치하면 found = True로 바꾸기
            if product[2] == product_name:
                with conn.cursor() as cursor:
                    cursor.execute(query2, args2 + (product[0],))
                    conn.commit()
                print(f" '{product_name}'의 수량이 {quantity}권 추가되었습니다. 총 {product[4] + quantity}권")
                found = True
                break
        if not found: # 전부 비교를 했는데 겹치는 것이 없으므로 found = False인 상태이므로 돌아가는 코드
            price = input('가격을 입력하세요>>>').strip(" ,.:").lower()
            expiration_day = input('유통기한을 입력하세요>>>').strip(" ,.:").lower()
            barcode = input('바코드를 입력하세요>>>').strip(" ,.:").lower()
            args1 = (product_name, barcode, price, quantity, expiration_day)
            conn = connect()
            with conn.cursor() as cursor:
                cursor.execute(query1, args1)
                product_id = cursor.lastrowid
            conn.commit()
            print(f" 새로운 상품 '{product_name}'이(가) 추가되었습니다. ({quantity}개)")
            return product_id
    except Error as error:
        print(error)

def update_product(products):
    query = """UPDATE products
                SET product_name = %s, barcode = %s, price = %s, quantity = %s, expiration_day = %s
                WHERE id = %s"""
    product_id = None

    try:
        while True :
            product_name = input('상품명을 입력하세요>>>').strip(" ,.:").lower()
            price = input('가격을 입력하세요>>>').strip(" ,.:").lower()
            quantity = input('입고 수량을 입력하세요>>>').strip(" ,.:").lower()
            expiration_day = input('유통기한을 입력하세요>>>').strip(" ,.:").lower()
            barcode = input('바코드를 입력하세요>>>').strip(" ,.:").lower()
            args1 = (product_name, barcode, price, quantity, expiration_day)
            args2 = (quantity, expiration_day, product_name)
            if quantity.isnumeric():  # 숫자인지 확인
                quantity = int(quantity)  # 숫자로 변환
                break
            else :
                print("숫자만 입력해주세요!")  # 숫자가 아니면 다시 입력 요청
        found = False  # 우선적으로 책 검색
        for product in products: # 도서관에 이미 있던 도서명과 일치하면 found = True로 바꾸기
            if product[1] == product_name:
                with conn.cursor() as cursor:
                    cursor.execute(query, args1 + (product[0],))
                    conn.commit()
                print(f" '{product_name}'의 수량이 {quantity}권 추가되었습니다. 총 {product[4] + quantity}권")
                found = True
                break
        if not found: # 전부 비교를 했는데 겹치는 것이 없으므로 found = False인 상태이므로 돌아가는 코드
            with conn.cursor() as cursor:
                cursor.execute(query1, args2)
                product_id = cursor.lastrowid
            conn.commit()
            print(f" 새로운 상품 '{product_name}'이(가) 추가되었습니다. ({quantity}권)")
            return product_id
    except Error as error:
        print(error)

if __name__ == '__main__' :
    read_config()
    conn = connect()
    rows = query_with_fetchall(conn)
    products = []
    for row in rows:
        products.append(row)
