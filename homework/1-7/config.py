
HOST = "localhost"
DBNAME = "postgres"
USER = "postgres"
PASSWD = ""
PORT = 5432


def DB_CONFIG():
    return f'dbname={DBNAME} user={USER} password={PASSWD} host={HOST} port={PORT}'

