import ujson
import json

from dclibs import queuer, logs, rabbitmq_utils, config, rediscache, sfapi, postgres, utils, aws
LOGGER = logs.LOGGER

SERVICE_NAME=''
SERVICE_DESCRIPTION=""
SERVICE_LABEL=""
SERVICE_ATTRIBUTES=[
        {'AttributeName':'', 'AttributeLabel': '', 'AttributeDescription':''}
    ]
SERVICE_STRUCTURE = {'ServiceName':SERVICE_NAME,
    'ServiceLabel':SERVICE_LABEL,
    'ServiceDescription':SERVICE_DESCRIPTION,
    'ServiceAttributes' : SERVICE_ATTRIBUTES,
    'PublishExternally':False,
    'Announce':False}
###



def treatMessage(dictValue):
    # utils.serviceTracesAndNotifies(dictValue, SERVICE_NAME, SERVICE_NAME + ' - Process Started', True)
    # will log
    
    LOGGER.info(dictValue)
    # opportunity object
    if (dictValue['payload']['source']['table'] == 'opportunity'):
        sqlRequest = """
        insert into consolidated.opportunities (sfopportunityid, sfaccountid, 
                                opportunityname, opportunityamount, 
                                opportunitystage, opportunityfiscalyear, opportunityfiscalquarter)
        values (%(sfopportunityid)s, %(sfaccountid)s, 
                                %(opportunityname)s, %(opportunityamount)s, 
                                %(opportunitystage)s, %(opportunityfiscalyear)s, %(opportunityfiscalquarter)s)
        on conflict (sfopportunityid)
        do update set
            sfaccountid = %(sfaccountid)s, 
            opportunityname= %(opportunityname)s, 
            opportunityamount= %(opportunityamount)s, 
            opportunitystage= %(opportunitystage)s, 
            opportunityfiscalyear= %(opportunityfiscalyear)s, 
            opportunityfiscalquarter=%(opportunityfiscalquarter)s
        """

        attributes = {
            'sfopportunityid' : dictValue['payload']['after']['sfid'],
            'sfaccountid' : dictValue['payload']['after']['accountid'],
            'opportunityname': dictValue['payload']['after']['name'],
            'opportunityamount': dictValue['payload']['after']['amount'],
            'opportunitystage': dictValue['payload']['after']['stagename'],
            'opportunityfiscalyear': dictValue['payload']['after']['fiscalyear'],
            'opportunityfiscalquarter': dictValue['payload']['after']['fiscalquarter' ]}
        
        # executes
        postgres.execRequest(sqlRequest, attributes, isInsert=True)
   

# create a function which is called on incoming messages
def genericCallback(ch, method, properties, body):
    try:
        # transforms body into dict
        treatMessage(ujson.loads(body))
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        LOGGER.error(e.__str__())
def announce():
    # sends a message to the proper rabbit mq queue to announce himself
    queuer.∏(SERVICE_STRUCTURE, config.SERVICE_REGISTRATION)    


if __name__ == "__main__":
    queuer.initQueuer()
    if (SERVICE_STRUCTURE['Announce'] == True):
        announce()
    queuer.listenToTopic(config.SUBSCRIBE_CHANNEL, 
    {
        config.QUEUING_KAFKA : treatMessage,
        config.QUEUING_CLOUDAMQP : genericCallback,
    })
