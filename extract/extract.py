import json
from datetime import date
from google.cloud import storage, bigquery, secretmanager
from reed import ReedExtractor


def get_secret(client, project, secretname):
    '''
    Get GCP Secrets Manager Secret.
    Args:
    ----
    client      : google.cloud.secretmanager.SecretManagerServiceClient
    project     : str -> GCP Project Name
    secretname  : str -> GCP Secret Name

    Returns:
    --------
    secret      : str -> Secret string
    '''
    response = client.access_secret_version(
        request={
            'name': f'projects/{project}/secrets/{secretname}/versions/latest'
            }
    )
    secret = eval(response.payload.data.decode('utf-8'))
    return secret


def get_current_listings(client):
    '''
    Get current listing jobIds from bigquery.

    Args:
    ----
    client      : google.cloud.bigquery.Client

    Returns:
    --------
    id_list     : List[int] -> List of jobIds
    '''

    query = '''SELECT jobId
        FROM `datapay.stg_listings`
        WHERE DATE(_PARTITIONTIME) < CURRENT_DATE()
        '''
    query_results = client.query(query).to_dataframe()
    id_list = list(query_results['jobId'])
    return id_list


def write_json_to_gcs(client, bucket, filepath, data):
    '''
    Write JSON record data to GCS as newline delimited JSON.

    Args:
    -----
    client      : google.cloud.storage.Client
    bucket      : str -> GCS Bucket name
    filepath    : str -> GCS filepath
    data        : List[Dict]

    Returns:
    --------
    None
    '''

    data_json = ""
    for item in data:
        data_json += json.dumps(item) + '\n'
    bucket = client.get_bucket(bucket)
    blob = bucket.blob(filepath)
    blob.upload_from_string(data_json, content_type='application/json')


def main(search_string):
    '''
    Run extract for Reed API and save results to GCS.
    Steps:
        1. Set up Google clients and declare variables
        2. Get API key and current listings
        3. Initialise extractor and run get_listings
        4. Write listings to GCS then filter for details
        5. Run get details and write to GCS
    Args:
    -----
    search_string       : str -> space seperated
                                keywords for Reed job search

    Returns:
    --------
    None
    '''

    storage_client = storage.Client()
    secret_client = secretmanager.SecretManagerServiceClient()
    bigquery_client = bigquery.Client(location='EU')

    FILE_SUFFIX = date.today().strftime('%Y%m%d')
    PROJECT = 'jacobhp-personal'
    BUCKET = 'datapay'
    DETAILS_PATH = f'reed/reed_details_{FILE_SUFFIX}.json'
    LISTINGS_PATH = f'reed/reed_listings_{FILE_SUFFIX}.json'

    api_key = get_secret(secret_client, PROJECT, 'reed_api_key')
    id_list = get_current_listings(bigquery_client)
    extractor = ReedExtractor(api_key)
    extractor.get_listings(search_string)
    write_json_to_gcs(storage_client,
                      BUCKET,
                      LISTINGS_PATH,
                      extractor.listings)
    print('Listings written to GCS')
    extractor.listings = [job for job in extractor.listings
                          if job['jobId'] not in id_list]
    print('Details to pull', len(extractor.listings))
    extractor.get_details()
    write_json_to_gcs(storage_client, BUCKET, DETAILS_PATH, extractor.details)
    print('Details written to GCS')


if __name__ == '__main__':

    main('data engineer')
