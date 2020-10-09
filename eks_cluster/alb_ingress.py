from aws_cdk import core, aws_eks, aws_ec2, aws_iam
from json import load, loads

class ALBIngressController(core.Construct):

    def __init__(self, scope: core.Construct, id: str, cluster, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.cluster = cluster
        
        iam_policy = aws_iam.PolicyStatement(
            actions=[
                "acm:DescribeCertificate",
                "acm:ListCertificates",
                "acm:GetCertificate",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:CreateSecurityGroup",
                "ec2:CreateTags",
                "ec2:DeleteTags",
                "ec2:DeleteSecurityGroup",
                "ec2:DescribeAccountAttributes",
                "ec2:DescribeAddresses",
                "ec2:DescribeInstances",
                "ec2:DescribeInstanceStatus",
                "ec2:DescribeInternetGateways",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeTags",
                "ec2:DescribeVpcs",
                "ec2:ModifyInstanceAttribute",
                "ec2:ModifyNetworkInterfaceAttribute",
                "ec2:RevokeSecurityGroupIngress",
                "elasticloadbalancing:AddListenerCertificates",
                "elasticloadbalancing:AddTags",
                "elasticloadbalancing:CreateListener",
                "elasticloadbalancing:CreateLoadBalancer",
                "elasticloadbalancing:CreateRule",
                "elasticloadbalancing:CreateTargetGroup",
                "elasticloadbalancing:DeleteListener",
                "elasticloadbalancing:DeleteLoadBalancer",
                "elasticloadbalancing:DeleteRule",
                "elasticloadbalancing:DeleteTargetGroup",
                "elasticloadbalancing:DeregisterTargets",
                "elasticloadbalancing:DescribeListenerCertificates",
                "elasticloadbalancing:DescribeListeners",
                "elasticloadbalancing:DescribeLoadBalancers",
                "elasticloadbalancing:DescribeLoadBalancerAttributes",
                "elasticloadbalancing:DescribeRules",
                "elasticloadbalancing:DescribeSSLPolicies",
                "elasticloadbalancing:DescribeTags",
                "elasticloadbalancing:DescribeTargetGroups",
                "elasticloadbalancing:DescribeTargetGroupAttributes",
                "elasticloadbalancing:DescribeTargetHealth",
                "elasticloadbalancing:ModifyListener",
                "elasticloadbalancing:ModifyLoadBalancerAttributes",
                "elasticloadbalancing:ModifyRule",
                "elasticloadbalancing:ModifyTargetGroup",
                "elasticloadbalancing:ModifyTargetGroupAttributes",
                "elasticloadbalancing:RegisterTargets",
                "elasticloadbalancing:RemoveListenerCertificates",
                "elasticloadbalancing:RemoveTags",
                "elasticloadbalancing:SetIpAddressType",
                "elasticloadbalancing:SetSecurityGroups",
                "elasticloadbalancing:SetSubnets",
                "elasticloadbalancing:SetWebAcl",
                "iam:CreateServiceLinkedRole",
                "iam:GetServerCertificate",
                "iam:ListServerCertificates",
                "cognito-idp:DescribeUserPoolClient",
                "waf-regional:GetWebACLForResource",
                "waf-regional:GetWebACL",
                "waf-regional:AssociateWebACL",
                "waf-regional:DisassociateWebACL",
                "tag:GetResources",
                "tag:TagResources",
                "waf:GetWebACL",
                "wafv2:GetWebACL",
                "wafv2:GetWebACLForResource",
                "wafv2:AssociateWebACL",
                "wafv2:DisassociateWebACL",
                "shield:DescribeProtection",
                "shield:GetSubscriptionState",
                "shield:DeleteProtection",
                "shield:CreateProtection",
                "shield:DescribeSubscription",
                "shield:ListProtections"
            ],
            resources=['*'],
        )    
            
        cluster_role_manifest = {
                "apiVersion": "rbac.authorization.k8s.io/v1",
                "kind": "ClusterRole",
                "metadata": {
                    "name": "alb-ingress-controller",
                    "labels": {
                        "app.kubernetes.io/name": "alb-ingress-controller"
                    }
                },
                "rules": [{
                    "apiGroups": [
                        "",
                        "extensions"
                    ],
                    "resources": [
                        "configmaps",
                        "endpoints",
                        "events",
                        "ingresses",
                        "ingresses/status",
                        "services",
                        "pods/status",
                        "nodes",
                        "pods",
                        "secrets",
                        "services",
                        "namespaces"
                    ],
                    "verbs": [
                        "create",
                        "get",
                        "list",
                        "update",
                        "watch",
                        "patch"
                    ]
                }]
            }
            
        cluster_role_binding_manifest = {
                "apiVersion": "rbac.authorization.k8s.io/v1",
                "kind": "ClusterRoleBinding",
                "metadata": {
                    "name": "alb-ingress-controller",
                    "labels": {
                        "app.kubernetes.io/name": "alb-ingress-controller"
                    }
                },
                "roleRef": {
                    "apiGroup": "rbac.authorization.k8s.io",
                    "kind": "ClusterRole",
                    "name": "alb-ingress-controller"
                },
                "subjects": [
                    {
                        "kind": "ServiceAccount",
                        "name": "alb-ingress-controller",
                        "namespace": "kube-system"
                    }
                ]
            }
            
        service_account_manifest = {
                "apiVersion": "v1",
                "kind": "ServiceAccount",
                "metadata": {
                    "name": "alb-ingress-controller",
                    "labels": {
                        "app.kubernetes.io/name": "alb-ingress-controller"
                    },
                    "namespace": "kube-system"
                }
            }

        deployment_manifest = {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": {
                    "name": "alb-ingress-controller",
                    "labels": {
                        "app.kubernetes.io/name": "alb-ingress-controller"
                    },
                    "namespace": "kube-system"
                },
                "spec": {
                    "selector": {"matchLabels": {"app.kubernetes.io/name": "alb-ingress-controller"}},
                    "template": {
                        "metadata": {"labels": {"app.kubernetes.io/name": "alb-ingress-controller"}},
                        "spec": {
                            "containers": [{
                                "name":  "alb-ingress-controller",
                                "args": [
                                    "--ingress-class=alb",
                                    "--cluster-name={}".format(self.cluster.cluster_name),
                                    "--aws-vpc-id={}".format(self.cluster.vpc.vpc_id)
                                ],
                                "image": "docker.io/amazon/aws-alb-ingress-controller:v1.1.8",
                            }
                            ],
                            "serviceAccountName": "alb-ingress-controller"
                        }
                    }
                }   
        }
        
        service_acct = aws_eks.ServiceAccount(
            self, "ALBIngressSA",
            cluster=self.cluster,
        )
        
        service_acct.add_to_principal_policy(statement=iam_policy)
        
        alb_ingress_access_manifests = aws_eks.KubernetesManifest(self, "ClusterRoleALB", cluster=self.cluster, manifest=[cluster_role_manifest, cluster_role_binding_manifest, service_account_manifest])
        
        alb_ingress_deployment = aws_eks.KubernetesManifest(self, "ALBIngressDeployment", cluster=self.cluster, manifest=[deployment_manifest])

