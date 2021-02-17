APPNAME=$1
export PYTHONPATH=.:./libs/:./appsrc/:./pyutils
# logs
export KAFKA_CLIENT_CERT=`heroku config:get KAFKA_CLIENT_CERT --app $APPNAME`
export KAFKA_CLIENT_CERT_KEY=`heroku config:get KAFKA_CLIENT_CERT_KEY --app $APPNAME`
export KAFKA_PREFIX=`heroku config:get KAFKA_PREFIX --app $APPNAME`
export KAFKA_TRUSTED_CERT=`heroku config:get KAFKA_TRUSTED_CERT --app $APPNAME`
export KAFKA_URL=`heroku config:get KAFKA_URL --app $APPNAME`
export KAFKA_USE_GROUP='True'

export QUEUING_SYSTEM='Kafka'
export SUBSCRIBE_CHANNEL='event_push_Notification__e,my-cool-topic,my-cool-topic-2'
export LOG_LEVEL='INFO'


export PYTHONPATH=$PYTHONPATH:/Users/Arieunier/Documents/DEV_SRC/DistributedComputed/libs/dclibs:.:./appsrc; python appsrc/template.py