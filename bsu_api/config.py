# URL configuration ================================================
# other URL's required in routers later on
ROS2_SERVER_PUBLISHER_URL = "http://bsu-ros-server:8003"
ROS2_SERVER_SUBSCRIBER_URL = "http://bsu-ros-server:8003"

# https://medium.com/@akshayjain.developer/connect-redis-with-authentication-using-python-5be3c6af59b9
# => REDIS_URL = 'redis://<username>:<password>@<hostname>:<port>/<db_number>'
REDIS_URL = "redis://:pwdAIteamREDIScontainer@bsu-redis:6379/0"
ARQ_REDIS_URL = "bsu-redis"
ARQ_REDIS_DATABASE = 0
ARQ_REDIS_PASSWORD = "pwdAIteamREDIScontainer"
ARQ_REDIS_PORT = 6379

from arq.connections import RedisSettings
ARQ_REDIS_SETTINGS = RedisSettings(
    host=ARQ_REDIS_URL,
    password=ARQ_REDIS_PASSWORD,
    database=ARQ_REDIS_DATABASE,
    port=ARQ_REDIS_PORT,
)

# for some reasons (i don't know why) each python library that connects to a database
# uses a different URL pattern to connect to a certain database. Here below i provide the ones for a MySQL server
# if using SQLalchemy:
# https://docs.sqlalchemy.org/en/20/dialects/mysql.html
# if using Prisma:
# https://www.prisma.io/docs/orm/overview/databases/mysql
MYSQL_DB_SERVER_URL = "mysql://aiUser:pwdAIteamDB@bsu-db-server:3306/bsu_warehouse_db"
# add the "origins" (the url of the server)
ORIGINS = [
    # bsu-api-server (this server) 
    "http://localhost:8000",        
    "http://127.0.0.1:8000",        
    "http://bsu-api-server:8000",   
    # bsu-website
    "http://bsu-website:80", 
    "http://bsu-website:8002",    
    # bsu-ros-server
    "http://bsu-ros-server",
    "http://bsu-ros-server:8003",
    # bsu-redis
    "http://bsu-redis",
    "http://bsu-redis:6379",
]
# URL configuration ================================================
