# Convenience Store Management System - Modeling

편의점 시스템은 제품 관리, 주문, 고객 정보, 매출 및 비용 등의 데이터를 효율적으로 관리할 수 있도록 설계되었습니다. 주요 테이블과 관계는 다음과 같습니다.

---

## 1. 주요 테이블 설명

| 테이블명         | 설명                                           |
|-----------------|----------------------------------------------|
| `Products`      | 편의점에서 판매하는 제품 정보를 저장         |
| `Orders`        | 고객이 제품을 구매할 때 발생하는 주문 정보를 저장 |
| `Order_Detail`  | 주문별 세부 제품 정보(제품명, 수량, 가격)를 저장 |
| `Customers`     | 고객의 기본 정보(이름, 연락처, 이메일 등)를 저장 |
| `Assistent`     | 편의점 직원 정보를 저장                        |
| `Daily_Account` | 일별 매출, 비용, 잔고 정보를 저장             |
| `Place_orders`  | 제품 입고 주문 정보를 저장                    |
| `Place_Order_Detail` | 입고된 제품의 상세 정보를 저장           |

---

## 2. 테이블 관계 설명

### ✅ `Products`와 `Order_Detail`
- 하나의 제품은 여러 주문에 포함될 수 있음 → **1:N 관계**
- `Order_Detail`에서 `Product_id`를 **외래키(FK)**로 참조

### ✅ `Orders`와 `Order_Detail`
- 한 번의 주문은 여러 개의 제품을 포함할 수 있음 → **1:N 관계**
- `Order_Detail`에서 `Order_id`를 **외래키(FK)**로 참조

### ✅ `Customers`와 `Orders`
- 한 명의 고객이 여러 주문을 할 수 있음 → **1:N 관계**
- `Orders`에서 `customer_id`를 **외래키(FK)**로 참조

### ✅ `Place_orders`와 `Place_Order_Detail`
- 한 번의 제품 입고 주문(`Place_orders`)이 여러 개의 제품을 포함할 수 있음 → **1:N 관계**
- `Place_Order_Detail`에서 `Place_id`를 **외래키(FK)**로 참조

### ✅ `Products`와 `Place_Order_Detail`
- 하나의 제품이 여러 번 입고될 수 있음 → **1:N 관계**
- `Place_Order_Detail`에서 `Product_id`를 **외래키(FK)**로 참조
