import json
import logging
from confluent_kafka import Producer
import os

def delivery_report(err, msg):
    if err is not None:
        logging.error(f"Message delivery failed: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def produce_message(topic: str, message):
    logging.info(f"Publishing message to {topic}...")
    p = Producer({'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')})    
    p.produce(topic, json.dumps(message).encode('utf-8'), callback=delivery_report)
    p.flush()
    logging.info(f"Message published to {topic}.")