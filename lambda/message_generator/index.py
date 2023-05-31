import boto3
import threading
import os

sqs = boto3.client("sqs")
queue_url = os.environ.get('QUEUE_URL')


def send_batch(queue_url, entries):
    response = sqs.send_message_batch(
        QueueUrl=queue_url,
        Entries=entries
    )
    print(f"Sent batch: {response}")


def handler(event, context):
    thread_pool = []
    batches = []
    for k in range(3):
        for n in range(2000):
            messages = []
            for i in range(10): # send_message_batch only allows 10 messages per batch
                messages.append({
                    'Id': f"message_{k}_{n}_{i}",
                    'MessageBody': f"Hello World: message_{k}_{n}_{i}",
                    'MessageGroupId': f"company_{k}"
                })
            batches.append(messages)
            
    for i in range(0, len(batches)):
        batch_entries = batches[i]
        thread = threading.Thread(target=send_batch, args=(queue_url, batch_entries))
        thread_pool.append(thread)
        thread.start()
        
    for thread in thread_pool:
        thread.join()

    return {
        'statusCode': 200,
        'body': 'Data loading completed'
    }