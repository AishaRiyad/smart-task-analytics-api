from redis import Redis
from testcontainers.redis import RedisContainer


def test_redis_container_set_get_delete():
    with RedisContainer("redis:7") as redis_container:
        host = redis_container.get_container_host_ip()
        port = redis_container.get_exposed_port(6379)

        redis_client = Redis(
            host=host,
            port=int(port),
            decode_responses=True
        )

        redis_client.set("task", "done")
        assert redis_client.get("task") == "done"

        redis_client.delete("task")
        assert redis_client.get("task") is None