from ORM.DbConfig import DbConfig
from ORM.User import User
from ORM.Data import Data


def add_data(session):
    new_user = User(login="admin", hashed_password="admin", salt="salt")
    session.add(new_user)

    new_user1 = User(login="admingunwo", hashed_password="admin", salt="salt")
    session.add(new_user1)

    new_data = Data(name="TSP-GREEDY", key="Warszawa", value="value", user=new_user)
    session.add(new_data)

    new_data1 = Data(name="TSP-GUNWO", key="Kurwidol", value="value", user=new_user1)
    session.add(new_data1)

    session.commit()


def delete_data(session):
    [session.delete(x) for x in session.query(User).all()]
    [session.delete(x) for x in session.query(Data).all()]
    session.commit()


if __name__ == "__main__":
    config = DbConfig()
    ses = config.get_session()

    add_data(ses)
    for elem in ses.query(User).all():
        print("User: " + elem.login.__str__())
        for elem1 in ses.query(Data).filter(Data.user == elem).all():
            print("TSP: " + elem1.name.__str__() + " city: " + elem1.key)

    delete_data(ses)

    for elem in ses.query(User).all():
        print("User: " + elem.login.__str__())
        for elem1 in ses.query(Data).filter(Data.user == elem).all():
            print("TSP: " + elem1.name.__str__() + " city: " + elem1.key)
