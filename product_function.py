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

def insert_product(conn, product_name, barcode, price, quantity, expiration_day):
    query = '''INSERT INTO products(product_name, barcode, price, quantity, expiration_day)
                VALUES(%s, %s, %s, %s, %s)'''
    args = (product_name, barcode, price, quantity, expiration_day)
    product_id = None
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, args)
            product_id = cursor.lastrowid
        conn.commit()
        return product_id
    except Error as error:
        print(error)

def update_product(conn, product_name, barcode, price, quantity, expiration_day,id):
    query = """UPDATE products
                SET product_name = %s, barcode = %s, price = %s, quantity = %s, expiration_day = %s
                WHERE id = %s"""

    data = (product_name, barcode, price, quantity, expiration_day, id)
    affected_rows = 0
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, data)
            affected_rows = cursor.rowcount
        conn.commit()
    except Error as error:
        print(error)
    return affected_rows

def delete_product(conn, id):
    query = "DELETE FROM products WHERE id = %s"
    data = (id,)
    affected_rows = 0
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, data)
            affected_rows = cursor.rowcount
        conn.commit()
    except Error as error:
        print(error)
    return affected_rows

def search_product(conn, product_name):
    query = "SELECT * FROM products WHERE product_name = %s"
    data = (product_name,)
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, data)
            rows = cursor.fetchall()
            print('Total Row(s):', cursor.rowcount)
            for row in rows:
                print(row)
            return rows
    except Error as error:
        print(error)

if __name__ == '__main__':
    print(__name__)
    print(read_config())
    conn = connect()
    # product_name = input('상품명을 입력하세요>>>')
    # barcode = input('바코드를 입력하세요>>>')
    # price = int(input('가격을 입력하세요>>>'))
    # quantity = int(input('재고 수량을 입력하세요>>>'))
    # expiration_day = input('유통기한을 입력하세요>>>')
    # id = int(input('상품 id를 입력하세요>>>'))
    # update_product(conn, product_name, barcode, price, quantity, expiration_day, id)
    # insert_product(conn, product_name, barcode, price, quantity, expiration_day)
    # affected_rows = update_product(conn, 1, '새로운 상품명', 2000, 50) # id가 1인 상품의 정보를 변경
    # print(f'변경된 행 수: {affected_rows}')
    # product = input('검색할 상품명을 입력하세요>>>')
    # search_product(conn, product)
    query_with_fetchall(conn)
    conn.close()