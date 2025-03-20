import test as pf
from test import read_config, connect, query_with_fetchall, insert_product #update_product, delete_product, search_product

display = '''
┌====================================================================┐
   1. 상품추가 2. 상품검색 3. 상품변경 4. 상품제거 5. 상품목록 6. 종료
└====================================================================┘
메뉴 번호를 선택해주세요 >>> '''

# 빈 리스트 선언 (도서 목록)
read_config()
conn = connect()
rows = query_with_fetchall(conn)
products = []
for row in rows:
    products.append(row)


while True:
    menu = input(display).strip()

    # 1. 상품 추가
    if menu == '1':
        products = pf.insert_product(products)

    # # 2. 상품 검색
    # elif menu == '2':
    #     products = pf.search_product(products)

    # # 3. 상품 변경
    # elif menu == '3':
    #     products = pf.update_product(products)

    # # 4. 상품 제거
    # elif menu == '4':
    #     products = pf.delete_product(products)

    # # 4. 전체 상품 목록
    # elif menu == "5":
    #     products = pf.query_with_fetchall(products)

    # # 5. 종료
    # elif menu == "6":
    #     print(" 편의점 시스템을 종료합니다.")
    #     break

    # # 6. 잘못된 명령어 처리
    # else:
    #     print(" 메뉴를 1~6사이의 숫자로 입력해주세요. ")