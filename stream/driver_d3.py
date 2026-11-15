import pika
import json
import sys

EXCHANGE = "rapido-dispatch"

def main():
    if len(sys.argv) != 3:
        print("Usage: python driver_d3.py NAME PATTERN")
        sys.exit(1)

    name = sys.argv[1]
    pattern = sys.argv[2]

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="topic",
        durable=True
    )

    # Each driver receives messages through its own private queue.
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange=EXCHANGE,
        queue=queue_name,
        routing_key=pattern
    )

    channel.basic_qos(prefetch_count=1)

    print(f"\nD3 Driver: {name}", flush=True)
    print(f"Binding pattern: {pattern}", flush=True)
    print(f"Private queue: {queue_name}", flush=True)
    print("Waiting for messages...\n", flush=True)

    def callback(ch, method, properties, body):
        try:
            message = json.loads(body.decode("utf-8"))

            # Assignment requirement: reject messages missing "zone".
            if "zone" not in message:
                print(
                    f"[{name}] REJECTED | {method.routing_key} | "
                    f"Missing required field: zone | NACK requeue=False",
                    flush=True
                )
                ch.basic_nack(
                    delivery_tag=method.delivery_tag,
                    requeue=False
                )
                return

            print(
                f"[{name}] PROCESSED | {method.routing_key} | "
                f"Message: {message} | ACK",
                flush=True
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as error:
            print(
                f"[{name}] REJECTED | Processing error: {error} | "
                f"NACK requeue=False",
                flush=True
            )
            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False
            )

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False
    )

    try:
        channel.start_consuming()

    except KeyboardInterrupt:
        print(f"\nDriver {name} stopped.", flush=True)

    finally:
        if channel.is_open:
            channel.close()
        connection.close()


if __name__ == "__main__":
    main()