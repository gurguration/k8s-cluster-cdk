#!/usr/bin/env python3
import os

import aws_cdk as cdk

from k8s_cluster.k8s_cluster_stack import VPCStack
from k8s_cluster.ec2nodes import Ec2NodesStack


app = cdk.App()

vpc = VPCStack(app, "VpcStack")
ec2_nodes = Ec2NodesStack(app, "Ec2WorkerNodes", custom_vpc=vpc.k8s_vpc)
app.synth()
