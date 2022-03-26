import boto3



def create_cluster_instance(cluster_id):
    client = boto3.client('docdb')



    response = client.create_db_instance(
                DBInstanceIdentifier='cs6620-bug-tracking-db2-instance2',
                DBInstanceClass='db.t3.medium',
                Engine='docdb',
                #AvailabilityZone='string',
                #PreferredMaintenanceWindow='string',
                #AutoMinorVersionUpgrade=True|False,
                #Tags=[
                #     {
                #       'Key': 'string',
                #       'Value': 'string'
                #     },
                #     ],
                DBClusterIdentifier=cluster_id,
                #PromotionTier=123
                )

    print(response)


