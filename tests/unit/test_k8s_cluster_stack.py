import aws_cdk as core
import aws_cdk.assertions as assertions

from k8s_cluster.k8s_cluster_stack import K8SClusterStack

# example tests. To run these tests, uncomment this file along with the example
# resource in k8s_cluster/k8s_cluster_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = K8SClusterStack(app, "k8s-cluster")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
