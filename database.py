from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql
from orm_models import OrmModel, OrmUser, OrmTask
from config import database_url, database_inf
from p_models import PUser, PTask, PTaskEdit


def create_database():
    try:
        connection = pymysql.connect(host=database_inf["host"], user=database_inf["username"], password=database_inf["password"], port=database_inf["port"])
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_inf["database"]};")
        print("Database created")
    except pymysql.MySQLError as ex:
        print(f"Error creating database: {ex}")
    finally:
        cursor.close()
        connection.close()
        


engine = create_engine(
    url=database_url,
    echo=False
)


session_factory = sessionmaker(
    bind=engine
)


def create_tables():
    OrmModel.metadata.create_all(bind=engine)


def delete_tables():
    OrmModel.metadata.drop_all(bind=engine)


def wipe_tables():
    delete_tables()
    create_tables()


def get_user(id) -> OrmUser:
    with session_factory() as session:
        return session.get(OrmUser, id)
    

def add_user(user: PUser):
    with session_factory() as session:
        session.add(OrmUser(userlogin=user.userlogin, userpassword=user.userpassword))
        session.commit()


def is_exists(userlogin: str):
    with session_factory() as session:
        output = session.query(OrmUser).filter(OrmUser.userlogin == userlogin).first()
        if output == None:
            return False
        return True
    

def login_validation(credentials: PUser):
    with session_factory() as session:
        output = session.query(OrmUser).filter(OrmUser.userlogin == credentials.userlogin, OrmUser.userpassword == credentials.userpassword).first()
        if output == None:
            return None
        return output.id
    

def get_tasks(owner_id):
    with session_factory() as session:
        tasks = session.query(OrmTask).filter(OrmTask.owner_id == owner_id).all()
        return [{"id": task.id, "owner_id": task.owner_id, "title": task.title, "description": task.description, "status": task.status.value} for task in tasks]
    

def add_task(in_owner_id, task: PTask):
    with session_factory() as session:
        session.add(OrmTask(owner_id=in_owner_id, title=task.title, description=task.description, status=task.status))
        session.commit()


def delete_task(in_owner_id, id):
    with session_factory() as session:
        to_delete = session.query(OrmTask).filter(OrmTask.id == id, OrmTask.owner_id == in_owner_id).first()
        if to_delete:
            session.delete(to_delete)
            session.commit()
            return True
        return False
    

def edit_task(in_owner_id, id, values: PTaskEdit):
    with session_factory() as session:
        to_edit = session.query(OrmTask).filter(OrmTask.id == id, OrmTask.owner_id == in_owner_id).first()
        if to_edit:
            if values.title:
                to_edit.title = values.title
            if values.description:
                to_edit.description = values.description
            to_edit.status = values.status
            session.commit()
            return True
        return False