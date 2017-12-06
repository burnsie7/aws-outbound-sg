import boto3
from botocore.exceptions import ClientError

"""
Boto by default will look for configuration files in the following order:

1. Passing credentials as parameters in the boto.client() method
2. Passing credentials as parameters when creating a Session object
3. Environment variables
4. Shared credential file (~/.aws/credentials)
5. AWS config file (~/.aws/config)
6. Assume Role provider
7. Boto2 config file (/etc/boto.cfg and ~/.boto)
8. Instance metadata service on an Amazon EC2 instance that has an IAM role configured.

To use environment variables set the following before running the script:

export AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY>
export AWS_SECRET_ACCESS_KEY=<YOUR_SECRET_ACCESS_KEY>
export AWS_DEFAULT_REGION=<YOUR_DEFAULT_REGION>
"""

# To use customn aws config files uncomment the lines below.
# AWS_CONFIG_FILE='/path/to/config'
# AWS_SHARED_CREDENTIALS_FILE='/path/to/credentials'

DD_IPS = ["54.210.140.216", "52.22.97.155", "52.201.141.103", "34.226.16.73", "52.55.93.212", "54.173.78.245", "52.87.19.203", "52.7.208.94", "52.71.208.243", "54.210.25.133", "52.1.36.76", "52.206.78.128", "50.17.165.224", "34.231.76.16", "52.20.120.113", "52.2.211.211", "54.173.112.230", "52.71.178.72", "52.0.152.181", "34.230.252.190", "34.206.8.211", "54.236.180.58", "54.210.243.81", "52.73.0.228", "54.165.6.52", "52.200.224.225", "52.44.101.233", "52.200.21.20", "52.3.132.33", "52.0.188.242", "52.45.238.215", "52.55.60.81", "52.44.201.144", "52.7.139.21", "54.84.224.233", "52.72.204.19", "54.165.167.62", "52.2.183.83", "52.207.21.226", "34.231.253.242", "52.4.169.217", "52.22.159.49", "34.192.34.214", "54.173.196.157", "52.0.91.246", "52.22.134.248", "52.202.168.18", "107.23.74.206", "52.71.221.45", "54.152.158.21", "52.73.128.118", "54.210.35.204", "34.235.56.117", "34.233.25.53", "34.234.124.163", "52.72.130.64", "52.3.21.1", "52.1.0.19", "52.0.140.238", "54.210.23.85", "52.0.175.153", "52.72.222.202", "52.22.119.160", "52.73.40.153", "34.226.189.164", "34.207.36.67", "52.45.28.194", "52.7.156.53", "52.86.225.73", "54.210.248.183", "52.200.93.201", "34.204.129.216"]

# len(DD_IPS) == 72 and is going to require 2 security groups

SECURITY_GROUP_ID = '<YOUR_SECURITY_GROUP_ID>'

# TODO: break out exceptions.  resource and security_group are not going to throw ClientError
try:
    ec2 = boto3.resource('ec2')
    security_group = ec2.SecurityGroup(SECURITY_GROUP_ID)
    # REVOKE
    revoke = security_group.revoke_egress(
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 443,
             'ToPort': 443,
             'IpRanges': [{'CidrIp': ip + "/32"} for ip in DD_IPS]},
        ])
    # AUTHORIZE
    authorize = security_group.authorize_egress(
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 443,
             'ToPort': 443,
             'IpRanges': [{'CidrIp': ip + "/32"} for ip in DD_IPS]},
        ])
    print('Egress Successfully Set %s' % data)
except ClientError as e:
    print(e)
