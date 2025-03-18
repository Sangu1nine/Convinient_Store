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
    try:
        print('MYSQL 데이터베이스에 연결 중...')
        config = read_config()
        conn = MySQLConnection(**config)
    except Error as error:
        print(error)
    return conn

def query_with_fetchall(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    print('총 행(들):', cursor.rowcount)
    for row in rows:
        print(row)
    return rows

def insert_product(conn, product_name, barcode, price, stock_quantity):
    query = '''INSERT INTO products(product_name, barcode, price, stock_quantity)
                VALUES(%s, %s, %s, %s)'''
    args = (product_name, barcode, price, stock_quantity)
    product_id = None
    with conn.cursor() as cursor:
        cursor.execute(query, args)
        product_id = cursor.lastrowid

    conn.commit()
    return product_id

def update_product(conn, product_id, product_name, price, stock_quantity):
    query = """UPDATE products
                SET product_name = %s, price = %s, stock_quantity = %s
                WHERE id = %s"""

    data = (product_name, price, stock_quantity, product_id)
    affected_rows = 0
    with conn.cursor() as cursor:
        cursor.execute(query, data)
        affected_rows = cursor.rowcount

    conn.commit()

def delete_product(conn, product_id):
    query = "DELETE FROM products WHERE id = %s"
    data = (product_id,)
    affected_rows = 0
    with conn.cursor() as cursor:
        cursor.execute(query, data)
        affected_rows = cursor.rowcount
    conn.commit()
    return affected_rows

if __name__ == '__main__':
    print(__name__)
    print(read_config())
    conn = connect()
    product_name = input('상품명을 입력하세요>>>')
    barcode = input('바코드를 입력하세요>>>')
    price = int(input('가격을 입력하세요>>>'))
    stock_quantity = int(input('재고 수량을 입력하세요>>>'))
    insert_product(conn, product_name, barcode, price, stock_quantity)
    affected_rows = update_product(conn, 1, '새로운 상품명', 2000, 50) # id가 1인 상품의 정보를 변경
    print(f'변경된 행 수: {affected_rows}')
    query_with_fetchall(conn)

    conn.close()