import boto3
bucketname = 'bucket_name' # replace with your bucket name
filename = 'image.jpg' # replace with your object key
s3 = boto3.resource('s3')
s3.Bucket(bucketname).download_file(filename, 'downloaded_from_aws.jpg')