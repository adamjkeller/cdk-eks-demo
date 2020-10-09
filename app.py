#!/usr/bin/env python3

from aws_cdk import core
from eks_cluster.eks_stack import EKSWorkshop

nodejs_service_details = {
    "service_name": "ecsdemo-nodejs",
    "replicas": 3,
    "labels": {
        "app": "ecsdemo-nodejs"
    },
    "image": "brentley/ecsdemo-nodejs:latest",
    "port": 3000,
    "service_type": "backend"
}

crystal_service_details = {
    "service_name": "ecsdemo-crystal",
    "replicas": 3,
    "labels": {
        "app": "ecsdemo-crystal",
    },
    "image": "brentley/ecsdemo-crystal:latest",
    "port": 3000,
    "service_type": "backend"
}

frontend_service_details = {
    "service_name": "ecsdemo-frontend",
    "replicas": 3,
    "labels": {
        "app": "ecsdemo-frontend",
    },
    "image": "brentley/ecsdemo-frontend:latest",
    "port": 3000,
    "service_type": "frontend",
    "env": [
        {"name": "CRYSTAL_URL", "value": "http://ecsdemo-crystal.default.svc.cluster.local/crystal"},
        {"name": "NODEJS_URL", "value": "http://ecsdemo-nodejs.default.svc.cluster.local/"},
    ]
}

# Cluster name: If none, will autogenerate
cluster_name = None 
# Capacity details: Cluster size of small/med/large
capacity_details = "large"
# Fargate enabled: Create a fargate profile on the cluster
fargate_enabled = True
# Bottlerocket ASG: Create a self managed node group of Bottlerocket nodes
bottlerocket_asg = False


app = core.App()

EKSWorkshop(app, "cftc-demo", fargate_enabled=fargate_enabled, 
capacity_details=capacity_details, bottlerocket_asg=bottlerocket_asg,
nodejs_service=nodejs_service_details, crystal_service=crystal_service_details,
frontend_service=frontend_service_details)

app.synth()
