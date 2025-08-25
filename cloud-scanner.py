import boto3


def aws_ec2_scan(): #must have aws cli configured, add option to manually input access and secret keys
    client = boto3.client('ec2')

    results = client.describe_instances()
    inst = results['Reservations'][0]['Instances'][0]


    print(inst['InstanceType'])
    print(inst['PlatformDetails'])
    print(inst['State']['Name'])


    print('Private: ' + inst['PrivateIpAddress'])
    #print('Public: ' + inst['PublicIpAddress'])

aws_ec2_scan()