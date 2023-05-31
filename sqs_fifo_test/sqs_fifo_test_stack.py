from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_lambda_event_sources as event_soruces,
    aws_sqs as sqs,
)
from constructs import Construct

class SqsFifoTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "SqsFifoQueue",
            fifo=True,
            content_based_deduplication=True,
        )

        sqs_message_generator_function = _lambda.Function(
            self, "SqsMessageGeneratorFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda/message_generator"),
            timeout=Duration.seconds(120),
            memory_size=2048,
            handler='index.handler',
            environment={
                "QUEUE_URL": queue.queue_url
            },
        )

        # Use queue as source to lamda function
        queue.grant_send_messages(sqs_message_generator_function)

        sqs_message_consumer_function = _lambda.Function(
            self, "SqsMessageConsumerFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda/message_consumer"),
            timeout=Duration.seconds(120),
            memory_size=1024,
            handler='index.handler',
        )

        sqs_message_consumer_function.add_event_source(
            event_soruces.SqsEventSource(
                queue,
                batch_size=10,
                enabled=False,
            )
        )
