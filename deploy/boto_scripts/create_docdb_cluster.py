import boto3


def create_cluster():
    client = boto3.client('docdb')
    cluster_id = 'cs6620-bug-tracking-db-cluster'
    response = client.create_db_cluster(
                #AvailabilityZones=[
                #            'string',
                #                ],
                BackupRetentionPeriod=1,
                DBClusterIdentifier=cluster_id,
               # DBClusterParameterGroupName='string',
               # VpcSecurityGroupIds=['string',],
               # DBSubnetGroupName='string',
                Engine='docdb',
                EngineVersion='4.0.0',
                Port=27017,
               MasterUsername='admin1',
               MasterUserPassword='password',
               # PreferredBackupWindow='string',
               # PreferredMaintenanceWindow='string',
               # Tags=[{'Key': 'string',
               #        'Value': 'string'
               #        },],
               # StorageEncrypted=True|False,
               # KmsKeyId='string',
               # EnableCloudwatchLogsExports=['string', ],
                DeletionProtection=False,
               #GlobalClusterIdentifier='bug-tracker-cs6620-db-cluster123',
               # SourceRegion='string'
               #DBInstanceClass='db.t3.medium'
                )
    print(response)
    # Return mongodb endpoint for cluster
    return response.get('DBCluster').get('ReaderEndpoint'), cluster_id






