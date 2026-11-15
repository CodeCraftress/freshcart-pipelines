
import pika
import json
import sys

EXCHANGE = "rapido-dispatch"

def main():
    if len(sys.argv) != 3:
        print("Usage: python driver.py NAME PATTERN")
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

    result = channel.queue_declare(
        queue="",
        exclusive=True
    )

    queue_name = result.method.queue

    channel.queue_bind(
        exchange=EXCHANGE,
        queue=queue_name,
        routing_key=pattern
    )

    channel.basic_qos(prefetch_count=1)

    print(f"\nDriver: {name}")
    print(f"Binding pattern: {pattern}")
    print(f"Private queue: {queue_name}")
    print("Waiting for requests...\n")

    def callback(ch, method, properties, body):
        try:
            message = json.loads(body.decode("utf-8"))

            print(
                f"[{name}] Received "
                f"{method.routing_key} | {message}"
            )

            # Acknowledge successfully processed message
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as error:
            print(f"[{name}] Processing error: {error}")
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
        print(f"\nDriver {name} stopped.")

    finally:
        if channel.is_open:
            channel.close()
        connection.close()


if __name__ == "__main__":
    main()