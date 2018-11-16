from ORM.DbConfig import DbConfig
from ORM.User import User
from ORM.Data import Data


def add_data(session):
    new_user = User(login="admin", hashed_password="admin", salt="salt")
    session.add(new_user)
    session.commit()

    new_data = Data(key="key", value="value")
    session.add(new_data)
    session.commit()


if __name__ == "__main__":
    config = DbConfig()
    ses = config.get_session()

    add_data(ses)
    for elem in ses.query(User).all():
        print("User: " + elem.login.__str__())
    for elem in ses.query(Data).all():
        print("City: " + elem.key.__str__() + " cost: " + elem.value.__str__())



