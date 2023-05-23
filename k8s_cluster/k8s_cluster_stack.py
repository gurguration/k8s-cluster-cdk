from aws_cdk import (
    aws_ec2 as ec2,
    Stack,
    Tags,
)
from constructs import Construct

class VPCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.k8s_vpc = ec2.Vpc(self, "k8s_VPC", 
                          ip_addresses=ec2.IpAddresses.cidr("10.0.1.0/26"),
                          nat_gateways=1,
                          max_azs=2,
                          )
        Tags.of(self.k8s_vpc).add("belongsTo","k8s-vpc-cdk-vpc-stack")
        
