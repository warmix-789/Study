from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String, default="Сотрудник")
    schedule = Column(String, default="Д Д Н Н В В В Д Д Н Н В В В Д Д Н Н В В В Д Д Н Н В В В Д Д") 
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    
    # Заменили ставку за смену на почасовую ставку (по умолчанию 300 руб/час)
    hourly_rate = Column(Integer, default=300)

    leave_requests = relationship("LeaveRequest", back_populates="employee")
    notifications = relationship("Notification", back_populates="employee")

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    day_index = Column(Integer)
    status = Column(String, default="Ожидает")
    employee = relationship("Employee", back_populates="leave_requests")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    message = Column(String)
    is_read = Column(Boolean, default=False)
    employee = relationship("Employee", back_populates="notifications")