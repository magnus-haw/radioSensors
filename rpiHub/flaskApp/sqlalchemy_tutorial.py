### import ORM module 
import sqlalchemy

### Create primary engine
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

### Load Base models class
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base() #basic model object

class User(Base): # inherit base model
    __tablename__ = 'users'               #required param
    id = Column(Integer,primary_key=True) #required param for all normal cases
    name = Column(String)              #other params ...
    fullname = Column(String)
    nickname = Column(String)
    addresses = relationship("Address", order_by='Address.id', back_populates="user")
    # define the object representation (e.g. when printed to terminal)
    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>"%(self.name,self.fullname,self.nickname)

### Add a second class with a many-to-one relationship
class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

### Create all tables
Base.metadata.create_all(engine)

### Adding table rows
ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
print(ed_user)



### Creating a session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine) #session class hook
session = Session() # instansiate a session

### Using session to track changes
session.add_all([ ed_user,
     User(name='wendy', fullname='Wendy Williams', nickname='windy'),
     User(name='mary', fullname='Mary Contrary', nickname='mary'),
     User(name='fred', fullname='Fred Flintstone', nickname='freddy')])
ed_user.nickname = 'eddie'

### Untracked modifications
print("Untracked modifications: ", session.dirty)

### Tracked changes
print("Changes staged for commit: ", session.new)

### Save session changes
session.commit() # changes are only added when commited



################### RELATIONSHIPS #####################

jack = User(name='jack', fullname='Jack Bean', nickname='gjffdd')
jack.addresses = [
        Address(email_address='jack@google.com'),
        Address(email_address='j25@yahoo.com')]

session.add(jack)
session.commit()


#################### QUERIES ###########################

# query from a class
filterby = session.query(User).filter_by(name='ed').all()
filter_ = session.query(User).filter(User.name=='ed').all()

# query with multiple classes, returns tuples
multi = session.query(User, Address).\
        filter(Address.email_address=='jack@google.com').\
        filter(User.id==Address.user_id).\
        all()

# query using orm-enabled descriptors
user_names = session.query(User.name, User.fullname).all()




