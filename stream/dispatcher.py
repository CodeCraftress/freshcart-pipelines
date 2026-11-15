
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

    print("Dispatcher started. Publishing every 2 seconds...")

    message_count = 0

    try:
        while True:
            city = random.choice(list(CITIES.keys()))
            zone = random.choice(CITIES[city])
            order_type = random.choice(ORDER_TYPES)

            routing_key = f"{city}.{zone}.{order_type}"

            message = {
                "id": str(uuid.uuid4())[:8],
                "city": city,
                "zone": zone,
                "type": order_type,
                "ts": datetime.now(timezone.utc).isoformat()
            }

            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=1
                )
            )

            message_count += 1

            print(
                f"[{message_count}] Published: "
                f"{routing_key} | {message}"
            )

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nDispatcher stopped.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()