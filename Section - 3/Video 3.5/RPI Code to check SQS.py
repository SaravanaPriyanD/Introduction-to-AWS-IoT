import boto3
import os
import time

access_key = "ACCESS_KEY"
access_secret = "ACCESS_SECRET"
region = "REGION"
queue_url = "QUEUE_URL"

def pop_message(client, url):
    response = client.receive_message(QueueUrl = url, MaxNumberOfMessages = 10)

    #last message posted becomes messages
    message = response['Messages'][0]['Body']
    receipt = response['Messages'][0]['ReceiptHandle']
    client.delete_message(QueueUrl = url, ReceiptHandle = receipt)
    return message

client = boto3.client('sqs', aws_access_key_id = access_key, aws_secret_access_key = access_secret, region_name = region)

waittime = 20
client.set_queue_attributes(QueueUrl = queue_url, Attributes = {'ReceiveMessageWaitTimeSeconds': str(waittime)})

time_start = time.time()
while (time.time() - time_start < 60):
        print("Checking...")
        try:
                message = pop_message(client, queue_url)
                print(message)
                if message:
                        os.system("~/on.sh")
                        time.sleep(20)
                        os.system("~/off.sh")
        except:
                pass
