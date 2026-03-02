from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

TEST_DATABASE_URL = "mysql+pymysql://root:raj1234@localhost/todos_test"
test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_test_database():
    import pymysql
    try:
        connection = pymysql.connect(host='localhost', user='root', password='raj1234')
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS todos_test")
        connection.commit()
        cursor.close()
        connection.close()
        print("Test database 'todos_test' created or already exists.")
    except Exception as e:
        print(f"Error creating test database: {e}")

def setup_test_database():
    create_test_database()
    Base.metadata.create_all(bind=test_engine)
    print("Test database tables created.")

def teardown_test_database():
    Base.metadata.drop_all(bind=test_engine)
    print("Test database tables dropped.")
