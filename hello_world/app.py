import json
import csv
import boto3

s3 = boto3.client('s3')
bucket = 'fdalist'
key = 'Products.txt'


def read_file():
    file = s3.get_object(Bucket=bucket, Key=key)
    lines = file['Body'].read().decode('utf-8').splitlines(True)
    reader = csv.DictReader(lines, delimiter='\t')
    return reader


def get_medication_info(medication, file):
    medication_list = []
    for row in file:
        active_ingredient = row.get('ActiveIngredient')
        if active_ingredient == medication:
            medication_list.append(row)
    return medication_list


def lambda_handler(event, context):
    file = read_file()
    medication = event["queryStringParameters"]["name"].upper()
    medication_list = get_medication_info(medication, file)

    medication_dict = {'Medication': medication,
                       'Forms': []
                       }

    for med in medication_list:
        response_dict = dict()
        response_dict['Form'] = med.get('Form')  # tipo de aplicacao
        response_dict['Drug Name'] = med.get('DrugName')  # nome comercial
        response_dict['Strength'] = med.get('Strength')  # dosagem
        medication_dict['Forms'].append(response_dict)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": medication_dict
        }),
    }
