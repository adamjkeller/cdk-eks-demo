from aws_cdk import core, aws_eks, aws_ec2, aws_iam

class Prometheus(core.Construct):

    def __init__(self, scope: core.Construct, id: str, cluster, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.cluster = cluster
        
        prom_stack = aws_eks.HelmChart(
            self, "PromHelmChart",
            cluster=self.cluster,
            release="prometheus",
            chart="kube-prometheus-stack",
            create_namespace=True,
            namespace="prometheus",
            repository="https://prometheus-community.github.io/helm-charts",
            values={
                "alertmanager.persistentVolume.storageClass": "gp2",
                "server.persistentVolume.storageClass": "gp2"
            }
        )