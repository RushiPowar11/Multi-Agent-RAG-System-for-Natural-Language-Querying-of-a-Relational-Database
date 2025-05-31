from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    
    customer_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    country = Column(String(100))
    join_date = Column(Date)
    
    # Relationships
    sales = relationship("Sale", back_populates="customer")

class Employee(Base):
    __tablename__ = "employees"
    
    employee_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    department = Column(String(100))
    hire_date = Column(Date)
    salary = Column(Float)
    
    # Relationships
    sales = relationship("Sale", back_populates="employee")
    project_assignments = relationship("ProjectAssignment", back_populates="employee")

class Project(Base):
    __tablename__ = "projects"
    
    project_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(Float)
    status = Column(String(100))
    
    # Relationships
    assignments = relationship("ProjectAssignment", back_populates="project")

class ProjectAssignment(Base):
    __tablename__ = "project_assignments"
    
    assignment_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    role = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    
    # Relationships
    project = relationship("Project", back_populates="assignments")
    employee = relationship("Employee", back_populates="project_assignments")

class Sale(Base):
    __tablename__ = "sales"
    
    sale_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    sale_date = Column(Date)
    amount = Column(Float)
    product = Column(String(100))
    
    # Relationships
    customer = relationship("Customer", back_populates="sales")
    employee = relationship("Employee", back_populates="sales")