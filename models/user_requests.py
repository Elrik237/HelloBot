from sqlalchemy import Column, Integer, String

from models import DeclarativeBase


class UserRequests(DeclarativeBase):
    __tablename__ = 'user_requests'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    user_name = Column(String)
    user_fullname = Column(String)
    data = Column(String)

    def __init__(self, user_id, user_name, user_fullname, data):
        self.user_id = user_id
        self.user_name = user_name
        self.user_fullname = user_fullname
        self.data = data

    def __repr__(self):
        return "<User('%s','%s', '%s', '%s')>" % (
            self.user_id, self.user_name, self.user_fullname, self.data)
