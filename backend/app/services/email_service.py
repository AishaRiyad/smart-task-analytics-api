import asyncio
import time


def send_fake_email_sync(task_title: str):
    time.sleep(3)
    print(f"Fake email sent synchronously for task: {task_title}")


async def send_fake_email_background(task_title: str):
    await asyncio.sleep(3)
    print(f"Fake email sent in background for task: {task_title}")