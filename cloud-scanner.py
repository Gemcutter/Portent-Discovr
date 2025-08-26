import boto3


def aws_ec2_scan(): #must have aws cli configured, add option to manually input access and secret keys
    client = boto3.client('ec2')

    results = client.describe_instances()

    for reservation in results['Reservations']:
        for inst in reservation['Instances']:

            print(inst['InstanceType'])
            print(inst['State']['Name'])
            print(inst['InstanceId'])        

            print(inst['PlatformDetails'] + " " + inst['Architecture'])
            print(inst['Tags'])

            print(inst['PrivateDnsName'])
            print(inst['PublicDnsName'])
            print(inst['SecurityGroups'])
            print(inst['SubnetId'])
            print(inst['VpcId'])

            print(inst['LaunchTime'])

            print('Private: ' + inst['PrivateIpAddress'])
            try:
                print('Public: ' + inst['PublicIpAddress'])
            except KeyError:
                print('Public: ' + 'N.A.')

            print("")
        print(len(results['Reservations']))



aws_ec2_scan()