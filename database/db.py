from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.orm import declarative_base
from urllib.parse import quote_plus


DATABASE_URL = (
    "postgresql://neondb_owner:npg_QBh9Jg3srpPi@ep-plain-glitter-aoz7upu7-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)
print(DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    echo = True
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

Base = declarative_base()

