from PIL import Image
import boto3
bucketname = 'bucket_name' 
s3 = boto3.resource('s3')
for i in range(5):
    try:
        s3.Bucket(bucketname).download_file('%s.jpg'  % i, 'downloaded_from_aws%s.jpg'  % i)
        img = Image.open('downloaded_from_aws%s.jpg'  % i)
        img.show()
    except:
        continue