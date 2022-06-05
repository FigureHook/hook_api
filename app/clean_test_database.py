import os

os.environ['ENV'] = "test"


def main():
    from app.db.base import Model
    from app.db.session import pgsql_db
    Model.metadata.drop_all(bind=pgsql_db.engine)


if __name__ == '__main__':
    main()
