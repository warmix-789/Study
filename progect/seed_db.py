import openpyxl
from database import engine, SessionLocal
import models
from models import Employee
import hashlib

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

# Функция для шифрования паролей (такая же, как в main.py)
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def load_excel_to_db(filename="company_schedule.xlsx"):
    db = SessionLocal()
    wb = openpyxl.load_workbook(filename)
    sheet = wb.active
    
    print("Начинаем чтение файла и создание аккаунтов...")
    # Единый стартовый пароль для всех из Excel
    default_password = hash_password("1234")
    
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not row[0]: 
            break
            
        emp_id = int(row[0])
        emp_name = row[1]
        emp_role = row[2]
        emp_schedule = " ".join([str(cell) for cell in row[3:10]])
        
        # Генерируем корпоративный логин на основе ID (например: user1, user5)
        emp_username = f"user{emp_id}"
        
        existing_emp = db.query(Employee).filter(Employee.id == emp_id).first()
        if not existing_emp:
            new_emp = Employee(
                id=emp_id, 
                name=emp_name, 
                role=emp_role, 
                schedule=emp_schedule,
                username=emp_username,
                password_hash=default_password
            )
            db.add(new_emp)
            print(f"Добавлен: {emp_name} | Логин: {emp_username} | Пароль: 1234")
            
    db.commit()
    db.close()
    print("Готово! Все сотрудники получили аккаунты.")

if __name__ == "__main__":
    load_excel_to_db()