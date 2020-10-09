from aws_cdk import core, aws_eks
from .eks_base import EKSBase
from .eks_manifest import EKSManifest
from .alb_ingress import ALBIngressController


class EKSWorkshop(core.Stack):

    def __init__(self, scope: core.Construct, id: str, 
    eks_version=aws_eks.KubernetesVersion.V1_17, cluster_name=None, 
    capacity_details='small', fargate_enabled=False, bottlerocket_asg=False,
    nodejs_service={}, crystal_service={}, frontend_service={}, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.eks_version = eks_version
        self.cluster_name = cluster_name
        self.capacity_details = capacity_details
        self.fargate_enabled = fargate_enabled
        self.bottlerocket_asg = bottlerocket_asg
        self.nodejs_service = nodejs_service
        self.crystal_service = crystal_service
        self.frontend_service = frontend_service
        
        config_dict = {
            'eks_version': self.eks_version,
            'cluster_name': self.cluster_name,
            'capacity_details': self.capacity_details,
            'fargate_enabled': self.fargate_enabled,
            'bottlerocket_asg': self.bottlerocket_asg
        }
        
        base_cluster = EKSBase(self, "Base", cluster_configuration=config_dict)
        nodejs_service = EKSManifest(self, "NodeJs", cluster=base_cluster.cluster, manifest=self.nodejs_service)
        crystal_service = EKSManifest(self, "CrystalBackend", cluster=base_cluster.cluster, manifest=self.crystal_service)
        alb_ingress = ALBIngressController(self, "ALBIngress", cluster=base_cluster.cluster)
        frontend_service = EKSManifest(self, "FrontendService", cluster=base_cluster.cluster, manifest=self.frontend_service)