from aws_cdk import (
    aws_ec2 as ec2, aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elb,
    Stack, Tags
)
with open("./user_data/user_data.sh") as f:
    user_data = f.read()
    
ec2_type = "t2.micro"
key_name = "myEC2Key"
linux_ami = ec2.AmazonLinuxImage(edition=ec2.AmazonLinuxEdition.STANDARD,
                                 cpu_type=ec2.AmazonLinuxCpuType.X86_64,
                                 generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
                                 virtualization=ec2.AmazonLinuxVirt.HVM)

class Ec2NodesStack(Stack):
    def __init__(self, scope, id, custom_vpc=None, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.asg = autoscaling.AutoScalingGroup(self, "K8S_ASG",
                                                vpc=custom_vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                                                machine_image=linux_ami,
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                desired_capacity=2,
                                                ssm_session_permissions=True,
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                max_capacity=2,
                                                min_capacity=2,
                                                update_policy=autoscaling.UpdatePolicy.replacing_update())
        
        external_alb = elb.ApplicationLoadBalancer(self, "K8sExternalALB",
                                               vpc=custom_vpc,
                                               internet_facing=True,
                                               load_balancer_name="K8sExternalALB")
        
        listener = external_alb.add_listener("Listener", 
                                             port=80,
                                             open=True)
        listener.add_targets("k8sNodes",
                            port=80,
                            targets=[self.asg])
    
        Tags.of(self).add("k8s_stack", "nodes and alb resources")
        
        
                                              