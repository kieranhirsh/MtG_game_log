from sqlalchemy import create_engine

user = "root"
pwd = "blah"
host = "localhost"
db = "MtG_log"

engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db))
