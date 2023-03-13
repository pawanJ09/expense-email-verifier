from botocore.exceptions import ClientError
import boto3
import json
import os

ses_client = boto3.client('ses')


def lambda_handler(event, context):
    try:
        print(f'Incoming event: {event}')
        event_http_method = event['requestContext']['http']['method']
        print(f'Incoming API Gateway HTTP Method: {event_http_method}')
        event_path = event['requestContext']['http']['path']
        print(f'Incoming API Gateway Path: {event_path}')
        body = event['body']
        print(f'Incoming API Gateway Body: {body}')
        req = json.loads(body)
        if req['user-email']:
            print(f'Fetching verified identities from SES')
            email_list_response = ses_client.list_verified_email_addresses()
            if req['user-email'] in email_list_response['VerifiedEmailAddresses']:
                print(f'Provided email found in verified identities')
                msg = {"message": "Provided Email verified"}
                return {
                    "statusCode": 200,
                    "headers": {"content-type": "application/json"},
                    "body": json.dumps(msg)
                }
            print(f'Provided email not found in verified identities')
            msg = {"message": "Provided Email not verified"}
            return {
                "statusCode": 404,
                "headers": {"content-type": "application/json"},
                "body": json.dumps(msg)
            }
    except KeyError as ke:
        print(f'Missing user-email in request')
        msg = {"message": "BAD Request - Missing user-email in request."}
        return {
            "statusCode": 400,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(msg)
        }
    except (Exception, ClientError) as e:
        print(f'Exception caught: {e}')
        msg = {"message": str(e)}
        return {
            "statusCode": 500,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(msg)
        }


if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    rel_path = '../events/test-agw-event.json'
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path) as f:
        test_event = json.load(f)
        lambda_handler(test_event, None)