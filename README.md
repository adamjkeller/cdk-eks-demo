## Deploy EKS environment with applications using the aws cdk

### Prerequisites
- aws-cdk 1.66.0
- python 3.6


### Deploy

```bash
$ npm install -g aws-cdk
$ pip install -r requirements.txt    # Best to do this in a virtualenv
$ cdk diff                           # View proposed changes
$ cdk deploy                         # Deploys the CloudFormation template

# Cleanup
$ cdk destroy
```

### Purpose

The purpose of this demo is to show a full end to end deployment experience that includes a cluster and services, all in one cdk application.
I also built this in a way to show how a team could build custom constructs to add their own requirements on top of the cdk constructs.


### Watch the recording

[![Youtube CFTC](http://img.youtube.com/vi/Y0tgevYN-Wo/0.jpg)](http://www.youtube.com/watch?v=Y0tgevYN-Wo "Automate EKS Environments with AWS CDK")
