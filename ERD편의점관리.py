from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser

def read_config(filename='app.ini', section='mysql'):
    """ app.ini 파일에서 MySQL 설정을 읽어옴 """
    config = ConfigParser()
    config.read(filename)
    db_config = {}

    if config.has_section(section):
        items = config.items(section)
        for item in items:
            db_config[item[0]] = item[1]
    else:
        raise Exception(f"{section} 섹션을 {filename}에서 찾을 수 없습니다.")
    
    return db_config

def connect():
    """ MySQL 데이터베이스 연결 """
    config = read_config()
    try:
        conn = MySQLConnection(**config)
        if conn.is_connected():
            print("✅ MySQL에 성공적으로 연결되었습니다.")
            return conn
    except Error as e:
        print(f"❌ 오류 발생: {e}")
        return None

def display():
    """ 터미널에 메뉴 화면 출력 """
    menu = '''
    ┌───────────────────────────────────────┐
       📌 편의점 관리 시스템
    └───────────────────────────────────────┘
    1. 제품 발주
    2. 고객 주문
    3. 제품 목록
    4. 주문 목록
    5. 직원 관리
    6. 매출 조회
    7. 종료
    ───────────────────────────────────────
    선택할 메뉴 번호를 입력하세요 (뒤로 가기: 0): '''
    
    choice = input(menu).strip()
    if choice == "0":
        return None  # 뒤로가기 시 None 반환
    return choice


def add_product(conn):
    """ 새 제품 추가 (중복된 제품이면 수량만 증가) """
    cursor = conn.cursor()
    print("📦 새 제품 추가 (뒤로 가기: 0 입력)")
    
    product_name = input("제품명: ").strip()
    if product_name == "0":
        return

    # 제품명이 이미 존재하는지 확인
    query_check = "SELECT Product_id, Quantity FROM Products WHERE Product_name = %s"
    cursor.execute(query_check, (product_name,))
    product = cursor.fetchone()

    found = False  # 기존 제품이 존재하는지 여부
    if product:
        found = True  # 기존 제품이 존재함
        product_id = product[0]
        existing_quantity = product[1]
        print(f"🔍 기존 제품 발견! (ID: {product_id}, 현재 수량: {existing_quantity})")
        
        # 수량만 추가
        try:
            add_quantity = int(input("추가할 수량을 입력하세요: ").strip())
            if add_quantity == 0:
                return
            
            query_update = "UPDATE Products SET Quantity = Quantity + %s WHERE Product_id = %s"
            cursor.execute(query_update, (add_quantity, product_id))
            conn.commit()
            print(f"✅ 제품 '{product_name}'의 수량이 {add_quantity}개 추가되었습니다. (총 {existing_quantity + add_quantity}개)")
        except ValueError:
            print("❌ 숫자만 입력하세요!")
        finally:
            cursor.close()
        return

    # 기존 제품이 없으면 새로 추가
    barcode = input("바코드: ").strip()
    if barcode == "0":
        return
    
    try:
        price = int(input("가격: ").strip())
        if price == 0:
            return
    except ValueError:
        print("❌ 숫자만 입력하세요!")
        return
    
    try:
        quantity = int(input("수량: ").strip())
        if quantity == 0:
            return
    except ValueError:
        print("❌ 숫자만 입력하세요!")
        return

    expiration_date = input("유통기한 (YYYY-MM-DD, 0 입력 시 생략): ").strip()
    if expiration_date == "0":
        expiration_date = None  # 유통기한 없이 입력 가능하도록 처리

    query_insert = """
    INSERT INTO Products (Product_name, Barcode, Price, Quantity, Expiration_date)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query_insert, (product_name, barcode, price, quantity, expiration_date))
        conn.commit()
        print(f"✅ 제품 '{product_name}' 추가 완료!")
    except Error as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        cursor.close()


def list_products(conn):
    """ 제품 목록 출력 """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    rows = cursor.fetchall()
    
    print("\n📦 제품 목록:")
    for row in rows:
        print(f"ID: {row[0]}, 이름: {row[2]}, 가격: {row[3]}, 재고: {row[4]}")
    
    cursor.close()

def add_order(conn):
    """ 새 주문 추가 """
    cursor = conn.cursor()
    print("🛒 새 주문 추가 (뒤로 가기: 0 입력)")
    
    try:
        customer_id = input("고객 ID: ").strip()
        if customer_id == "0":
            return
        
        assistant_id = input("점원 ID: ").strip()
        if assistant_id == "0":
            return

        # 새로운 주문 생성
        query_order = """
        INSERT INTO Orders (Customer_id, Assistant_id, Date)
        VALUES (%s, %s, NOW())
        """
        cursor.execute(query_order, (customer_id, assistant_id))
        order_id = cursor.lastrowid  # 생성된 주문 ID 가져오기
        conn.commit()
        print(f"✅ 주문 생성 완료! 주문 ID: {order_id}")

        while True:
            product_id = input("추가할 제품 ID (뒤로 가기: 0 입력): ").strip()
            if product_id == "0":
                break

            quantity = input("수량 입력: ").strip()
            if quantity == "0":
                break

            # 제품 가격 조회
            cursor.execute("SELECT Price FROM Products WHERE Product_id = %s", (product_id,))
            product = cursor.fetchone()
            if not product:
                print("❌ 존재하지 않는 제품입니다.")
                continue

            price = product[0]
            total_price = int(price) * int(quantity)

            # 주문 상세 추가
            query_order_detail = """
            INSERT INTO Order_Detail (Order_id, Product_id, Quantity, Price)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_order_detail, (order_id, product_id, quantity, total_price))
            conn.commit()
            print(f"✅ 제품 {product_id} {quantity}개 추가 완료!")

    except Error as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        cursor.close()

def list_orders(conn):
    """ 주문 목록 출력 """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Orders")
    rows = cursor.fetchall()

    print("\n🛒 주문 목록:")
    for row in rows:
        print(f"주문 ID: {row[0]}, 고객 ID: {row[1]}, 점원 ID: {row[2]}, 날짜: {row[3]}")

    cursor.close()

if __name__ == "__main__":
    conn = connect()
    if conn:
        while True:
            choice = display()
            if choice is None:
                continue  # 뒤로가기 기능
            elif choice == "1":
                add_product(conn)
            elif choice == "2":
                add_order(conn)
            elif choice == "3":
                list_products(conn)
            elif choice == "4":
                list_orders(conn)
            elif choice == "7":
                print("🔚 프로그램을 종료합니다.")
                conn.close()
                break
            else:
                print("❌ 올바른 메뉴를 선택하세요.")
