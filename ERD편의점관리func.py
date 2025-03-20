from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser
import datetime

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
    6. 고객 관리
    7. 장부 조회
    8. 종료
    ───────────────────────────────────────
    선택할 메뉴 번호를 입력하세요 (뒤로 가기: 0): '''
    
    choice = input(menu).strip()
    return None if choice == "0" else choice

def add_product(conn):
    """ 새 제품 추가 (중복된 제품이면 수량만 증가) """
    try:
        cursor = conn.cursor()
        print("📦 새 제품 추가 (뒤로 가기: 0 입력)")

        product_name = input("제품명: ").strip()
        if product_name == "0":
            return

        # 1️⃣ 오늘 날짜 확인 및 `Daily_Account` 자동 추가
        cursor.execute("SELECT COUNT(*) FROM Daily_Account WHERE `Date` = CURDATE()")
        date_exists = cursor.fetchone()[0]

        if date_exists == 0:
            cursor.execute("INSERT INTO Daily_Account (`Date`, Sales, Costs, Funds) VALUES (CURDATE(), 0, 0, 1000000)")
            conn.commit()
            print(f"✅ `{datetime.datetime.today().strftime('%Y-%m-%d')}` 날짜를 Daily_Account에 추가했습니다.")

        # 2️⃣ 제품명이 이미 존재하는지 확인
        query_check = "SELECT Product_id, Price, Quantity FROM Products WHERE Product_name = %s"
        cursor.execute(query_check, (product_name,))
        product = cursor.fetchone()

        if product:
            # 기존 제품 존재 → 수량 추가
            product_id, price, existing_quantity = product
            print(f"🔍 기존 제품 발견! (ID: {product_id}, 현재 수량: {existing_quantity}, 가격: {price}원)")

            try:
                add_quantity = int(input("추가할 수량을 입력하세요: ").strip())
                if add_quantity == 0:
                    return
                
                # 제품 수량 업데이트
                query_update = "UPDATE Products SET Quantity = Quantity + %s WHERE Product_id = %s"
                cursor.execute(query_update, (add_quantity, product_id))
                conn.commit()

                print(f"✅ 제품 '{product_name}'의 수량이 {add_quantity}개 추가되었습니다. (총 {existing_quantity + add_quantity}개)")

                # 3️⃣ `Daily_Account` 비용 반영 (기존 제품 수량 추가 비용)
                additional_cost = add_quantity * price
                query_update_costs = """
                UPDATE Daily_Account
                SET Costs = COALESCE(Costs, 0) + %s
                WHERE Date = CURDATE();
                """
                cursor.execute(query_update_costs, (additional_cost,))
                conn.commit()
                print(f"📉 비용이 {additional_cost}원 증가했습니다.")

            except ValueError:
                print("❌ 숫자만 입력하세요!")
            return  # 수량 추가 후 종료

        # 4️⃣ 기존 제품이 없으면 새로 추가
        barcode = input("바코드: ").strip()
        if barcode == "0":
            return

        try:
            price = int(input("가격: ").strip())
            quantity = int(input("수량: ").strip())
        except ValueError:
            print("❌ 숫자만 입력하세요!")
            return

        expiration_date = input("유통기한 (YYYY-MM-DD, 0 입력 시 생략): ").strip()
        if expiration_date == "0":
            expiration_date = None
        else:
            try:
                datetime.datetime.strptime(expiration_date, "%Y-%m-%d")  # 날짜 검증
            except ValueError:
                print("❌ 날짜 형식이 올바르지 않습니다! (예: 2024-12-31)")
                return

        query_insert = """
        INSERT INTO Products (Product_name, Barcode, Price, Quantity, Expiration_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert, (product_name, barcode, price, quantity, expiration_date))
        conn.commit()
        print(f"✅ 제품 '{product_name}' 추가 완료!")

        # 5️⃣ `Daily_Account` 비용 반영 (새 제품 추가 비용)
        new_product_cost = price * quantity
        query_update_costs = """
        UPDATE Daily_Account
        SET Costs = COALESCE(Costs, 0) + %s
        WHERE Date = CURDATE();
        """
        cursor.execute(query_update_costs, (new_product_cost,))
        conn.commit()
        print(f"📉 비용이 {new_product_cost}원 증가했습니다.")

    except mysql.connector.Error as e:
        print(f"❌ 오류 발생: {e}")

    finally:
        update_funds(conn)  # 자본 업데이트
        cursor.close()  # 오류 발생 여부와 상관없이 커서를 닫음

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
    """ 고객이 제품을 주문하면 주문을 처리하는 함수 (재고 관리 포함) """

    cursor = conn.cursor()

    # 1️⃣ 직원 선택
    print("📌 담당 직원 선택:")
    cursor.execute("SELECT Assistant_id, Name FROM Assistant")
    assistants = cursor.fetchall()
    for assistant in assistants:
        print(f"{assistant[0]}: {assistant[1]}")
    
    assistant_id = input("직원 ID 입력 (취소: 0): ").strip()
    if assistant_id == "0":
        print("🚫 주문이 취소되었습니다.")
        return

    # 2️⃣ 고객 선택
    print("\n📌 주문 고객 선택:")
    cursor.execute("SELECT Customer_id, Name FROM Customers")
    customers = cursor.fetchall()
    for customer in customers:
        print(f"{customer[0]}: {customer[1]}")
    
    customer_id = input("고객 ID 입력 (취소: 0): ").strip()
    if customer_id == "0":
        print("🚫 주문이 취소되었습니다.")
        return

    # 3️⃣ 오늘 날짜 확인 및 `Daily_Account` 자동 추가
    cursor.execute("SELECT COUNT(*) FROM Daily_Account WHERE `Date` = CURDATE()")
    date_exists = cursor.fetchone()[0]

    if date_exists == 0:
        cursor.execute("INSERT INTO Daily_Account (`Date`, Sales, Costs, Funds) VALUES (CURDATE(), 0, 0, 1000000)")
        conn.commit()
        print(f"✅ `{cursor.lastrowid}` 날짜를 Daily_Account에 추가했습니다.")

    # 4️⃣ 주문 추가 (Orders 테이블에 추가)
    query_order = """
    INSERT INTO Orders (Customer_id, Assistant_id, Date, Total_Price) 
    VALUES (%s, %s, CURDATE(), 0)"""
    cursor.execute(query_order, (customer_id, assistant_id))
    conn.commit()

    # 5️⃣ 방금 추가된 Order_id 가져오기
    cursor.execute("SELECT LAST_INSERT_ID()")
    order_id = cursor.fetchone()[0]
    print(f"\n✅ 주문이 생성되었습니다. (Order ID: {order_id})")

    # 6️⃣ 제품 선택 및 주문 상세 추가
    total_price = 0
    while True:
        print("\n📌 주문할 제품을 선택하세요:")
        cursor.execute("SELECT Product_id, Product_name, Price, Quantity FROM Products")
        products = cursor.fetchall()
        for product in products:
            print(f"{product[0]}: {product[1]} - {product[2]}원 (재고: {product[3]}개)")

        product_id = input("제품 ID 입력 (완료: 0): ").strip()
        if product_id == "0":
            break
        
        quantity = int(input("수량 입력: ").strip())

        # 제품 정보 가져오기
        cursor.execute("SELECT Price, Quantity FROM Products WHERE Product_id = %s", (product_id,))
        product_data = cursor.fetchone()
        if not product_data:
            print("🚫 존재하지 않는 제품입니다. 다시 입력하세요.")
            continue

        price, stock = product_data

        # 재고 확인
        if quantity > stock:
            print(f"🚫 재고 부족! 현재 {stock}개만 주문 가능합니다.")
            continue

        # `Order_Detail` 테이블에 추가
        query_detail = """
        INSERT INTO Order_Detail (Order_id, Product_id, Price, Quantity)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_detail, (order_id, product_id, price, quantity))
        total_price += price * quantity

        # `Products` 테이블의 재고 차감
        query_update_stock = """
        UPDATE Products SET Quantity = Quantity - %s WHERE Product_id = %s
        """
        cursor.execute(query_update_stock, (quantity, product_id))

        print(f"✅ 제품 {product_id} {quantity}개 추가 완료! (재고 업데이트됨)")

    # 7️⃣ 총 금액을 Orders 테이블에 업데이트
    query_update_total = """
    UPDATE Orders SET Total_Price = %s WHERE Order_id = %s"""
    cursor.execute(query_update_total, (total_price, order_id))
    conn.commit()
    print(f"\n💰 주문 총액: {total_price}원")

    # 8️⃣ Daily_Account 테이블의 매출 반영
    query_update_sales = """
    UPDATE Daily_Account
    SET Sales = COALESCE(Sales, 0) + %s
    WHERE Date = CURDATE();
    """
    cursor.execute(query_update_sales, (total_price,))
    update_funds(conn)  # 자본 업데이트
    conn.commit()
    print("\n📈 매출이 업데이트되었습니다.")

    cursor.close()

def list_orders(conn):
    """ 주문 목록 출력 """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Orders")
    rows = cursor.fetchall()

    print("\n🛒 주문 목록:")
    for row in rows:
        print(f"주문 ID: {row[0]}, 고객 ID: {row[1]}, 가격: {row[2]}, 점원 ID: {row[3]}, 날짜: {row[4]}")

    cursor.close()

def display_assistants(conn):
    """ 직원(점원) 목록을 표시하는 함수 (직책 포함) """
    cursor = conn.cursor()
    
    # 📋 직원 목록 가져오기
    query = "SELECT Assistant_id, Name, `Rank` FROM Assistant"
    cursor.execute(query)
    assistants = cursor.fetchall()

    # 🖥 직원 목록 출력
    print("\n📌 직원 목록")
    print("───────────────────────────────────")
    print(f"{'ID':<5} {'이름':<15} {'직책(Rank)':<15}")
    print("───────────────────────────────────")
    for assistant in assistants:
        print(f"{assistant[0]:<5} {assistant[1]:<15} {assistant[2]:<15}")
    print("───────────────────────────────────")

    cursor.close()

def display_customers(conn):
    """ 고객 목록을 표시하고 등급을 업데이트하는 함수 """
    cursor = conn.cursor()

    # 🔄 등급 업데이트 쿼리 실행 (Costs에 따라 자동 반영)
    cursor.execute("UPDATE Customers SET Grade = 'VIP' WHERE Costs >= 500000;")
    cursor.execute("UPDATE Customers SET Grade = 'Gold' WHERE Costs >= 200000 AND Costs < 500000;")
    cursor.execute("UPDATE Customers SET Grade = 'Silver' WHERE Costs >= 100000 AND Costs < 200000;")
    cursor.execute("UPDATE Customers SET Grade = 'Bronze' WHERE Costs < 100000;")
    conn.commit()
    print("✅ 고객 등급이 최신 상태로 업데이트되었습니다.")

    # 📋 고객 목록 가져오기
    query = "SELECT Customer_id, Name, Phone, Email, Address, Grade, Costs FROM Customers"
    cursor.execute(query)
    customers = cursor.fetchall()

    # 🖥 고객 목록 출력
    print("\n📌 고객 목록")
    print("───────────────────────────────────────────────────────────────")
    print(f"{'ID':<5} {'이름':<10} {'전화번호':<15} {'이메일':<25} {'주소':<15} {'등급':<8} {'구매 금액':<10}")
    print("───────────────────────────────────────────────────────────────")
    for customer in customers:
        print(f"{customer[0]:<5} {customer[1]:<10} {customer[2]:<15} {customer[3]:<25} {customer[4]:<15} {customer[5]:<8} {customer[6]:<10}")
    print("───────────────────────────────────────────────────────────────")

    cursor.close()

def update_funds(conn):
    """ Daily_Account의 Funds(자본)을 날짜별로 누적 업데이트하는 함수 """
    cursor = conn.cursor()

    # 1️⃣ 모든 날짜를 오름차순 정렬하여 가져오기
    cursor.execute("SELECT `Date`, Sales, Costs FROM Daily_Account ORDER BY `Date` ASC")
    daily_records = cursor.fetchall()

    funds = 1000000  # 초기 자본
    for date, sales, costs in daily_records:
        funds += sales - costs  # 매일 자본 계산

        # 2️⃣ 해당 날짜의 `Funds` 업데이트
        cursor.execute("UPDATE Daily_Account SET Funds = %s WHERE `Date` = %s", (funds, date))

    conn.commit()
    cursor.close()
    print("✅ `Funds`가 누적 업데이트되었습니다.")

def display_account(conn):
    """ 장부 조회 """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Daily_Account")
    rows = cursor.fetchall()

    print("\n📈 장부 조회:")
    for row in rows:
        print(f"날짜: {row[0]}, 매출: {row[1]}원, 지출: {row[2]}원, 보유 자금: {row[3]}원")
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
            elif choice == "5":
                display_assistants(conn)
            elif choice == "6":
                display_customers(conn)
            elif choice == "7":
                display_account(conn)
            elif choice == "8":
                print("🔚 프로그램을 종료합니다.")
                conn.close()
                break
            else:
                print("❌ 올바른 메뉴를 선택하세요.")

