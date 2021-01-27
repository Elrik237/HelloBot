from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


class DeclarativeBase:
    pass


DeclarativeBase = declarative_base(cls=DeclarativeBase)


class ClickStatistics(DeclarativeBase):
    __tablename__ = 'click_statistics'
    id = Column(Integer, primary_key=True)
    time = Column(String)
    f_name = Column(String)
    user_id = Column(String)
    user_name = Column(String)
    user_fullname = Column(String)

    def __init__(self, time, f_name, user_id, user_name, user_fullname):
        self.time = time
        self.f_name = f_name
        self.user_id = user_id
        self.user_name = user_name
        self.user_fullname = user_fullname

    def __repr__(self):
        return "<User('%s','%s', '%s', '%s', '%s')>" % (
            self.time, self.f_name, self.user_id, self.user_name, self.user_fullname)
