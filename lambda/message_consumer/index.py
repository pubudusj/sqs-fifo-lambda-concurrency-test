def handler(event, context):
    for record in event['Records']:
        # Only for testing purposes. Don't use sleep in production!!!
        print(record['body'])
        
    return
