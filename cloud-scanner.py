import boto3

'''
ACCESS_KEY = 'AKIAQDKVY2FF2DVI4SE2'
SECRET_KEY = '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'
    aws_access_key_id= ACCESS_KEY,
    aws_secret_access_key= SECRET_KEY,
    region_name= 'ap-southeast-2'
'''
def aws_ec2_scan(): #must have aws cli configured
    client = boto3.client('ec2')

    results = client.describe_instances()
    inst = results['Reservations'][0]['Instances'][0]


    print(inst['InstanceType'])
    print(inst['PlatformDetails'])
    print(inst['State']['Name'])


    print('Private: ' + inst['PrivateIpAddress'])
    #print('Public: ' + inst['PublicIpAddress'])

aws_ec2_scan()