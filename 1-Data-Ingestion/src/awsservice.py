# @author Hongwei
import boto3
from botocore import exceptions


def upload_data(ACCESS_KEY, SECRET_KEY, region, bucketName, fileName, logger):
    s3Session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=region
    )
    s3 = s3Session.resource('s3')

    # Create Bucket in S3
    bucket = create_bucket(s3, bucketName, logger, region)
    if bucket is None:
        logger.warning("Skip: Clean Data Upload Failed.")
        print("Skip: Clean Data Upload Failed. Find Details in logs.")
        return

    # Upload File to S3
    upload_to_s3(s3, bucket, fileName, logger)


def create_bucket(s3, bucketName, logger, region):
    # Create a Bucket (Name should not be uppercase)
    # Check Whether the bucket has been created
    bucket = None
    isCreated = False
    try:
        for bucket in s3.buckets.all():
            if bucket.name == bucketName:
                isCreated = True
                print('Skip: ' + 'Bucket(' + bucketName + ')' + ' Already Created.')
                logger.warning('Bucket(' + bucketName + ')' + ' Already Created.')
                break
        if not isCreated:
            bucket = s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={
                'LocationConstraint': region})
            logger.info('Bucket(' + bucketName + ')' + 'Created')
            bucket.Acl().put(ACL='public-read')
            logger.info('Bucket Set to Public')
        return bucket
    except exceptions.EndpointConnectionError or exceptions.ClientError as e:
        print("Warning: " + str(e))
        logger.error(e)
        return None
    except Exception as e:
        print("Warning: " + str(e))
        logger.error(e)
        return None


def check_file(curr_bucket, filename):
    for key in curr_bucket.objects.all():
        if key.key == filename:
            print('Skip: ' + 'File(' + filename + ')' + ' Already Exists.')
            return True


def upload_to_s3(s3, bucket, fileName, logger):
    # Check Whether File Exists
    logger.info('Checking Whether File Exists on S3...')
    isExist = check_file(bucket, fileName)
    if not isExist:
        # Upload data to S3
        logger.info('Starting Upload Data to S3')
        s3.Object(bucket.name, fileName).put(Body=open(fileName, 'rb'))
        s3.Object(bucket.name, fileName).Acl().put(ACL='public-read')
        print('Upload: Success')
        logger.info('Data Upload Succeed')
    else:
        logger.warning('File(' + fileName + ')' + ' Already Exists on S3.')
