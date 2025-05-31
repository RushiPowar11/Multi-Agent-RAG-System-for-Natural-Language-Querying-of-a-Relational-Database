from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from faker import Faker
from datetime import datetime, timedelta
import random
from model import Base, Customer, Employee, Project, ProjectAssignment, Sale
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup with error handling
try:
    logger.info(f"Attempting to connect to database with URL: {settings.DATABASE_URL}")
    engine = create_engine(settings.DATABASE_URL, echo=True)
    
    # Test the connection
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        logger.info("Database connection test successful!")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except SQLAlchemyError as e:
    logger.error(f"Database connection error: {str(e)}")
    raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        db.close()

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully!")
    except SQLAlchemyError as e:
        logger.error(f"Error creating tables: {str(e)}")
        raise

def generate_synthetic_data():
    fake = Faker()
    db = SessionLocal()
    try:
        # Generate Customers (200 records)
        customers = []
        for _ in range(200):
            customer = Customer(
                name=fake.name(),
                email=fake.email(),
                country=fake.country(),
                join_date=fake.date_between(start_date='-3y', end_date='today')
            )
            customers.append(customer)
        db.add_all(customers)
        logger.info("Added customer records")
        
        # Generate Employees (50 records)
        departments = ['Sales', 'Marketing', 'Engineering', 'Support', 'HR']
        employees = []
        for _ in range(50):
            employee = Employee(
                name=fake.name(),
                department=random.choice(departments),
                hire_date=fake.date_between(start_date='-5y', end_date='today'),
                salary=random.uniform(50000, 150000)
            )
            employees.append(employee)
        db.add_all(employees)
        logger.info("Added employee records")
        
        # Generate Projects (30 records)
        statuses = ['Planning', 'In Progress', 'Completed', 'On Hold']
        projects = []
        for _ in range(30):
            start_date = fake.date_between(start_date='-2y', end_date='today')
            end_date = fake.date_between(start_date=start_date, end_date=start_date + timedelta(days=365))
            project = Project(
                name=fake.catch_phrase(),
                start_date=start_date,
                end_date=end_date,
                budget=random.uniform(10000, 500000),
                status=random.choice(statuses)
            )
            projects.append(project)
        db.add_all(projects)
        logger.info("Added project records")
        
        # Commit to get IDs
        db.commit()
        
        # Generate Project Assignments (150 records)
        roles = ['Project Manager', 'Developer', 'Designer', 'Analyst', 'Tester']
        assignments = []
        for _ in range(150):
            project = random.choice(projects)
            assignment = ProjectAssignment(
                project_id=project.project_id,
                employee_id=random.choice(employees).employee_id,
                role=random.choice(roles),
                start_date=project.start_date,
                end_date=project.end_date
            )
            assignments.append(assignment)
        db.add_all(assignments)
        logger.info("Added project assignment records")
        
        # Generate Sales (500 records)
        products = ['Product A', 'Product B', 'Product C', 'Service X', 'Service Y']
        sales = []
        for _ in range(500):
            sale = Sale(
                customer_id=random.choice(customers).customer_id,
                employee_id=random.choice(employees).employee_id,
                sale_date=fake.date_between(start_date='-2y', end_date='today'),
                amount=random.uniform(100, 10000),
                product=random.choice(products)
            )
            sales.append(sale)
        db.add_all(sales)
        logger.info("Added sales records")
        
        db.commit()
        logger.info("All synthetic data committed successfully!")
    except SQLAlchemyError as e:
        logger.error(f"Error generating synthetic data: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    try:
        logger.info("Starting database initialization...")
        create_tables()
        logger.info("Starting synthetic data generation...")
        generate_synthetic_data()
        logger.info("Database setup completed successfully!")
    except Exception as e:
        logger.error(f"Setup failed: {str(e)}")
        raise