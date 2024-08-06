import pytz


UTC = pytz.utc
# Get the timezone for India
IST = pytz.timezone("Asia/Kolkata")


"""ALERTS HANDLER"""

MAIL_URL = "http://{domain}/ds/internal/messenger/send-mail"
TEAMS_URL = "http://{domain}/ds/internal/messenger/teamsAlerts"


"""MQTT HANDLER"""

MAX_CHUNK_SIZE = 1000
SLEEP_TIME = 1

"""DATA ACCESS"""

GET_USER_INFO_URL = "{protocol}://{data_url}/api/metaData/user"
GET_DEVICE_DETAILS_URL = "{protocol}://{data_url}/api/metaData/allDevices"
GET_DEVICE_METADATA_URL = "{protocol}://{data_url}/api/metaData/device/{device_id}"
GET_DP_URL = "{protocol}://{data_url}/api/apiLayer/getLimitedDataMultipleSensors/"
GET_FIRST_DP = "{protocol}://{data_url}/api/apiLayer/getMultipleSensorsDPAfter"
INFLUXDB_URL = "{protocol}://{data_url}/api/apiLayer/getAllData"
CONSUMPTION_URL = "{protocol}://{data_url}/api/apiLayer/getStartEndDPV2"
MAX_RETRIES = 15
RETRY_DELAY = [2, 4]


"""EVENTS HANDLER"""

PUBLISH_EVENT_URL = "{protocol}://{third_party_server}/api/eventTag/publishEvent"
GET_EVENTS_IN_TIMESLOT_URL = "{protocol}://{third_party_server}/api/eventTag/fetchEvents/timeslot"
GET_EVENT_DATA_COUNT_URL = "{protocol}://{third_party_server}/api/eventTag/fetchEvents/count"
GET_EVENT_CATEGORIES_URL = "{protocol}://{third_party_server}/api/eventTag"
GET_DETAILED_EVENT_URL = "{protocol}://{third_party_server}/api/eventTag/eventLogger"