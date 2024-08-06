__all__ = [
    's3_upload_file', 's3_save_and_upload_file', 's3_save_and_upload_csv', 's3_save_and_upload_json',
    's3_download_file', 's3_download_and_read_file', 's3_download_and_read_csv', 's3_download_and_read_json',
    's3_list_folder_contents', 's3_check_file_exists', 's3_download_folder_contents',
    's3_delete_file', 's3_sql_query_csv']

from ._imports import *
from ._config import config


class AmazonS3:
    clients = {}

    @classmethod
    def get_client(cls, env):
        if env not in cls.clients:
            if config.has_option(f'aws_{env}','aws_session_token'):
                cls.clients[env] = boto3.client(
                    service_name            = 's3',
                    region_name             = config[f'aws_{env}']['region'], 
                    aws_access_key_id       = config[f'aws_{env}']['aws_access_key_id'],
                    aws_secret_access_key   = config[f'aws_{env}']['aws_secret_access_key'],
                    aws_session_token       = config[f'aws_{env}']['aws_session_token']
                )
            else:
                #aws_access_key_id, aws_secret_access_key  = get_credential_both_method(f'aws_{env}')
                cls.clients[env] = boto3.client(
                    service_name            = 's3',
                    region_name             = config[f'aws_{env}']['region'], 
                    aws_access_key_id       = config[f'aws_{env}']['aws_access_key_id'],
                    aws_secret_access_key   = config[f'aws_{env}']['aws_secret_access_key']
                    #aws_access_key_id = aws_access_key_id, 
                    #aws_secret_access_key = aws_secret_access_key 
                )

        return cls.clients[env]

def client(env):
    return AmazonS3.get_client(env)

@atexit.register
def s3_close():
    for client in AmazonS3.clients.values():
        client.close()

def s3_upload_file(local_file_path, s3_file_path=None, overwrite=False, env='dev'):
    if s3_file_path == None:
        s3_file_path  = os.path.basename(local_file_path)
    if not overwrite and s3_file_path in s3_list_folder_contents(os.path.dirname(s3_file_path), env=env):
        raise Exception('File Already Exists')
    else:
        client(env).upload_file(local_file_path, config[f'aws_{env}']['bucket'], s3_file_path)

def s3_save_and_upload_file(data, s3_file_path, local_file_name='output', overwrite=False, save_file_kwargs={}, env='dev'):
    _, s3_file_extension = os.path.splitext(s3_file_path)
    local_folder_path    = config['local']['local_folder']
    local_file_name      = os.path.basename(local_file_name) + '.' + s3_file_extension
    local_file_path      = os.path.join(local_folder_path, local_file_name)
    if s3_file_extension == '.csv':
        data.to_csv(local_file_path, index=False, **save_file_kwargs)
    elif s3_file_extension == '.parquet':
        data.to_parquet(local_file_path, index=False, **save_file_kwargs)
    elif s3_file_extension == '.json':
        with open(local_file_path, 'w') as f:
            json.dump(data, f, indent=4, **save_file_kwargs)
    elif s3_file_extension == '.pkl':
        with open(local_file_path, 'wb') as f:
            pickle.dump(data, f)
    s3_upload_file(local_file_path, s3_file_path, overwrite=overwrite, env=env)
    os.remove(local_file_path)

def s3_save_and_upload_csv(df, local_file_name='output.csv', s3_file_path=None, overwrite=False, env='dev'):
    local_folder_path = config['local']['local_folder']
    local_file_name = os.path.basename(local_file_name)
    local_file_path = os.path.join(local_folder_path, local_file_name)
    df.to_csv(local_file_path, index=False)
    s3_upload_file(local_file_path, s3_file_path, overwrite=overwrite, env=env)
    os.remove(local_file_path)

def s3_save_and_upload_json(data, local_file_name='output.json', s3_file_path=None, overwrite=False, env='dev'):
    local_folder_path = config['local']['local_folder']
    local_file_name = os.path.basename(local_file_name)
    local_file_path = os.path.join(local_folder_path, local_file_name)
    with open(local_file_path, 'w') as f:
        json.dump(data, f, indent=4)
    s3_upload_file(local_file_path, s3_file_path, overwrite=overwrite, env=env)
    os.remove(local_file_path)
    
def s3_download_file(s3_file_path, local_file_path, s3_bucket=None, env='dev'):
    if s3_bucket is None:
        s3_bucket = config[f'aws_{env}']['bucket']
    try:
        client(env).download_file(s3_bucket, s3_file_path, local_file_path)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            raise Exception('File Does Not Exist')
        else:
            raise

def s3_download_and_read_file(s3_file_path, local_file_path=None, s3_bucket=None, read_file_kwargs={}, env='dev'):
    _, s3_file_extension = os.path.splitext(s3_file_path)
    if local_file_path is None:
        local_folder_path = config['local']['local_folder']
        local_file_name = os.path.basename(s3_file_path)
        local_file_path = os.path.join(local_folder_path, local_file_name)
    s3_download_file(s3_file_path, local_file_path, s3_bucket=s3_bucket, env=env)
    if s3_file_extension == '.csv':
        d = pd.read_csv(local_file_path, **read_file_kwargs)
    elif s3_file_extension == '.xlsx':
        d = pd.read_excel(local_file_path, **read_file_kwargs)
    elif s3_file_extension == '.json':
        with open(local_file_path) as f:
            d = json.load(f)
    os.remove(local_file_path)
    return d

def s3_download_and_read_csv(s3_file_path, local_file_path=None, s3_bucket=None, read_csv_kwargs={}, env='dev'):
    if local_file_path is None:
        local_folder_path = config['local']['local_folder']
        local_file_name = os.path.basename(s3_file_path)
        local_file_path = os.path.join(local_folder_path, local_file_name)
    s3_download_file(s3_file_path, local_file_path, s3_bucket=s3_bucket, env=env)
    df = pd.read_csv(local_file_path, **read_csv_kwargs)
    os.remove(local_file_path)
    return df

def s3_download_and_read_json(s3_file_path, local_file_path=None, s3_bucket=None, env='dev'):
    if local_file_path is None:
        local_folder_path = config['local']['local_folder']
        local_file_name = os.path.basename(s3_file_path)
        local_file_path = os.path.join(local_folder_path, local_file_name)
    s3_download_file(s3_file_path, local_file_path, s3_bucket=s3_bucket, env=env)
    with open(local_file_path) as f:
        d = json.load(f)
    os.remove(local_file_path)
    return d

def s3_list_folder_contents(s3_folder_path, s3_bucket=None, pattern=r'^.*$', env='dev'):
    if s3_bucket is None:
        s3_bucket = config[f'aws_{env}']['bucket']
    contents = []
    for item in client(env).list_objects(Bucket=s3_bucket, Prefix=s3_folder_path)['Contents']:
        if re.match(pattern, item['Key']):
            contents.append(item['Key'])
    return contents

def s3_check_file_exists(s3_file_path, env='dev'):
    s3_folder_path = os.path.dirname(s3_file_path)
    if s3_file_path in s3_list_folder_contents(s3_folder_path, env=env):
        return True
    return False

def s3_download_folder_contents(s3_folder_path, local_folder_path=None, s3_bucket=None, pattern=r'^.*\.csv$', env='dev'):
    if local_folder_path is None:
        local_folder_path = config['local']['local_folder']
    for s3_file_path in s3_list_folder_contents(s3_folder_path, s3_bucket=s3_bucket, pattern=pattern, env=env):
        s3_file_name = os.path.basename(s3_file_path)
        local_file_path = os.path.join(local_folder_path, s3_file_name)
        s3_download_file(s3_file_path, local_file_path, s3_bucket=s3_bucket, env=env)

def s3_delete_file(s3_file_path, s3_bucket=None, env='dev'):
    if s3_bucket is None:
        s3_bucket = config[f'aws_{env}']['bucket']
    try:
        client(env).delete_object(Bucket=s3_bucket, Key=s3_file_path)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            raise Exception('File Does Not Exist')
        else:
            raise

def s3_sql_query_csv(s3_file_path, s3_query='select * from s3object', s3_bucket=None, env='dev'):
    if s3_bucket is None:
        s3_bucket = config[f'aws_{env}']['bucket']
    resp = client(env).select_object_content(
        Bucket = s3_bucket,
        Key = s3_file_path,
        Expression=s3_query,
        ExpressionType='SQL',    
        InputSerialization={
            "CSV": {
                'FileHeaderInfo': 'USE',
                'AllowQuotedRecordDelimiter': True,
            },
        },
        OutputSerialization={
            'CSV': {}
        },
    )

    records = []
    for event in resp['Payload']:
        if 'Records' in event:
            records.append(event['Records']['Payload'])
        elif 'Stats' in event:
            stats = event['Stats']['Details']

    file_str = ''.join(r.decode('utf-8') for r in records)
    df = pd.read_csv(io.StringIO(file_str),  header=None)
    return df

