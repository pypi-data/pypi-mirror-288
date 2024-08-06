import json
import logging
from confluent_kafka import Consumer
import os

def consume_message(topics_with_priority, group_id: str, as_json: bool = False, wait_time: float = 10.0):
    logging.info(f"Consuming messages from topics...")
    c = Consumer({
        'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True,       # Enable auto-commit
        'auto.commit.interval.ms': 5000   # Auto-commit interval in milliseconds
    })
    
    if isinstance(topics_with_priority, str):
        topic_names = [topics_with_priority]
    else:
        # Sort topics by priority (assuming lower number means higher priority)
        sorted_topics = sorted(topics_with_priority, key=lambda x: x['priority'])
        topic_names = [topic['name'] for topic in sorted_topics]

    # lets subscribe to each topic one by one
    for topic_name in topic_names:
        logging.info(f"Subscribing to topic: {topic_name}")
        
        c.subscribe([topic_name])

        logging.info(f"Polling messages from topic: {topic_name}")
        message = c.poll(wait_time)

        if message is None:
            logging.info(f"No messages found in topic: {topic_name}")
            continue

        if message.error():
            logging.error(f"Consumer error: {message.error()}")
            continue

        message_value = message.value().decode('utf-8')
        topic_name = message.topic()
        logging.info(f"Consumed message from topic: {topic_name}")
        
        # commit offset
        logging.info(f"Committing offset for topic: {topic_name}")
        c.commit()
        logging.info(f"Offset committed for topic: {topic_name}")
        
        if as_json:
            try:
                return json.loads(message_value)
            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error: {e}")
                return None
        else:
            return message_value

    c.close()
