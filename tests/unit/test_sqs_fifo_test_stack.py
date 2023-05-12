import aws_cdk as core
import aws_cdk.assertions as assertions

from sqs_fifo_test.sqs_fifo_test_stack import SqsFifoTestStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sqs_fifo_test/sqs_fifo_test_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SqsFifoTestStack(app, "sqs-fifo-test")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
