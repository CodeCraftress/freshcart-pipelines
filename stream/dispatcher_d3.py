import pika
import json
import time
import random
import uuid
from datetime import datetime, timezone

EXCHANGE = "rapido-dispatch"

CITIES = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "adyar", "velachery"]
}

ORDER_TYPES = ["ride", "food"]

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="topic",
        durable=True
    )

    print("D3 Dispatcher started. Publishing every 2 seconds...", flush=True)

    count = 0

    try:
        while True:
            count += 1

            city = random.choice(list(CITIES.keys()))
            zone = random.choice(CITIES[city])
            order_type = random.choice(ORDER_TYPES)

            routing_key = f"{city}.{zone}.{order_type}"

            # Build a normal message first.
            message = {
                "id": str(uuid.uuid4())[:8],
                "city": city,
                "zone": zone,
                "type": order_type,
                "ts": datetime.now(timezone.utc).isoformat()
            }

            # Every 10th message is deliberately malformed:
            # remove the required "zone" field from the message body.
            if count % 10 == 0:
                del message["zone"]
                status = "MALFORMED - zone missing"
            else:
                status = "VALID"

            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=1
                )
            )

            print(
                f"[{count}] {status} | Routing key: {routing_key} | "
                f"Message: {message}",
                flush=True
            )

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nD3 Dispatcher stopped.", flush=True)

    finally:
        connection.close()


if __name__ == "__main__":
    main()