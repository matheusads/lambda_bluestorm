import json

import pytest

from hello_world import app


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""
    return {
        "resource": "/medication",
        "path": "/medication",
        "httpMethod": "GET",
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-us",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Host": "",
            "origin": "",
            "Referer": "",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Via": "2.0 fake.cloudfront.net (CloudFront)"
        },
        "queryStringParameters": {
            "name": "Ibuprofen",
            "page": "1"
        },
        "pathParameters": "null",
        "stageVariables": "null",
        "requestContext": {
            "resourceId": "fake",
            "resourcePath": "/medication",
            "httpMethod": "GET",
            "extendedRequestId": "U2F6OH5uvHcFnUg=",
            "requestTime": "23/Oct/2020:00:00:00 +0000",
            "path": "/v1/medication",
            "accountId": "123456789",
            "protocol": "HTTP/1.1",
            "stage": "v1",
            "domainPrefix": "fake-api-gw",
            "requestTimeEpoch": 1603424321320,
            "requestId": "150e20c5-81ae-4f85-9d1c-a2ae2c189db4 ",
            "identity": {
                "cognitoIdentityPoolId": "null",
                "cognitoIdentityId": "null",
                "vpceId": "null",
                "principalOrgId": "null",
                "cognitoAuthenticationType": "null",
                "userArn": "null",
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
                "accountId": "null",
                "caller": "null",
                "sourceIp": "10.1.0.137",
                "accessKey": "null",
                "vpcId": "null",
                "cognitoAuthenticationProvider": "null",
                "user": "null"
            },
            "domainName": "fakeurl.apigateway.com",
            "apiId": "fake-api-gw"
        },
        "body": "null",
        "isBase64Encoded": "false"
    }


def test_lambda_handler(apigw_event):
    expected = {'Medication': 'IBUPROFEN',
                'Forms': [{'Form': '', 'Drug Name': '', 'Strength': ''}]
                }

    expected_medication = 'IBUPROFEN'
    expected_qty = 242

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"]["Medication"] == expected_medication
    assert len(data["message"]["Forms"]) == expected_qty
