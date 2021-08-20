import boto3

def lambda_handler(event, context):
    client = boto3.resources('dynamodb')
    table = client.Table('')
    
    # where the dict of data to put into the database goes
    input = {}
    
    # add a try and response handeler here
    response = table.put_item(Item=input)