from app.storage.db import engine, Base
from app.storage import models  # noqa: F401


def main():
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")


if __name__ == "__main__":
    main()