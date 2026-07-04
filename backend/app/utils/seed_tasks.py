import random

from app.db.database import SessionLocal
from app.db.models import Task


def seed_tasks(count: int = 10000):
    db = SessionLocal()

    try:
        for i in range(1, count + 1):
            task = Task(
                title=f"Performance Task {i}",
                description=f"This task is used for search and performance testing number {i}",
                completed=random.choice([True, False]),
                completion_time=random.randint(5, 180)
            )

            db.add(task)

            if i % 500 == 0:
                db.commit()
                print(f"{i} tasks inserted...")

        db.commit()
        print("Seeding completed successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_tasks()