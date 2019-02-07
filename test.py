from BLL.UserManager import UserManager
from ORM.Data import Data
from ORM.DbConfig import DbConfig
from ORM.User import User


def delete_data(session):
    [session.delete(x) for x in session.query(User).all()]
    [session.delete(x) for x in session.query(Data).all()]
    session.commit()


if __name__ == "__main__":
    config = DbConfig()
    ses = config.get_session()
    manager = UserManager(ses)

    user = manager.add_user("admin@gmail.com", "admin1")
    data = Data(name="TSP", key=0, value=0, user=user)
    ses.add(data)
    data = Data(name="TSP", key=1, value=20, user=user)
    ses.add(data)
    data = Data(name="TSP", key=2, value=12, user=user)
    ses.add(data)
    data = Data(name="TSP", key=0, value=5, user=user)
    ses.add(data)

    ses.commit()

    user1 = manager.add_user("user@gmail.com", "user1")
    data1 = Data(name="ATSP", key=2, value=0, user=user1)
    ses.add(data1)
    data1 = Data(name="ATSP", key=1, value=17, user=user1)
    ses.add(data1)
    data1 = Data(name="ATSP", key=0, value=40, user=user1)
    ses.add(data1)
    data1 = Data(name="ATSP", key=2, value=4, user=user1)
    ses.add(data1)

    ses.commit()

    for elem in ses.query(User).all():
        print("\n")
        cost = 0
        print("User: " + elem.login.__str__() + ", Password: " + elem.hashed_password.__str__())
        for elem1 in ses.query(Data).filter(Data.user == elem).all():
            cost += elem1.value
            print(elem1.name.__str__() + " city: " + elem1.key.__str__())
        print("Cost of route: " + cost.__str__())


