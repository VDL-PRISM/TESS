#import click
import json
import time
from datetime import datetime
import logging

LOGGER = logging.getLogger()

class Database:
    """
    Manage the influxdb database interaction 
    """

    def __init__(self, username, password, host, port, database, ssl=False):
        from influxdb import InfluxDBClient
        self.client = InfluxDBClient(host=host, port=port, username=username,
                                     password=password, database=database,
                                     ssl=ssl, verify_ssl=ssl)

        self._queue = None

    def setup_queue(self, queue):
        self._queue = queue

    def get_latest(self, type, query):

        result = self.get_data(type, query)

        if len(result) < 1 or len(result) > 1: 
            #Depending on the query statement, the result can become empty. It is also possible that uploader push all data from the local database and the result can become empty
            return datetime.now(), -1
        else:
            result = result[0]

            # We should have a time and some other measurement
            assert len(result) == 2

            time = result.pop('time')
            other = list(result.values())[0]
            return time, other

    def get_data(self, type, query):
        from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError

        try:
            result = self.client.query(query)
        except InfluxDBClientError as e:
            LOGGER.error("Unable to get the latest data from database: %s", e)
            raise DatabaseException(json.loads(e.content)['error'])
        except Exception as e:
            LOGGER.error("Unable to get the latest data from database: %s", e)
            # keep running when some other exceptions happen (ex, http max request errors)
            return datetime.now(), -1

        result = list(result.get_points())
        return result

    def record_event(self, home_id, event, time=None):
        from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError

        if time is None:
            time = datetime.utcnow()
            # following needs to be looked at.
            #if 'UTC' in time.tzname:
            #    time = pytz.timezone('UTC').localize(time)
            #else:
            #    time = pytz.timezone('US/Mountain').localize(time)
            #    time = time.astimezone(pytz.UTC)
        else:
            time = datetime.utcnow()
            hour, minute = (int(x) for x in time.split(":"))
            
            time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            #if 'UTC' in time.tzname:
            #    time = pytz.timezone('UTC').localize(time)
            #else:
            #    time = pytz.timezone('US/Mountain').localize(time)
            #    time = time.astimezone(pytz.UTC)


        try:
            LOGGER.info("Adding {} event at {} to database.".format(event, time))

            data = {
            'measurement': 'ecobee_fan',
            'tags': {
                'home_id': home_id
                },
                'time': time,
                'fields': {
                    'value': '{}'.format(event)
                }
            }

            if self._queue is not None and not self._queue:
                data = [[v for k, v in sorted(data.items())]]
                self._queue.push(data)
            else:
                self.client.write_points([data])

        except (InfluxDBClientError, InfluxDBServerError) as e:
            LOGGER.error("Unable to add an event to database: %s", e)
        except Exception as e:
            LOGGER.error("An exception ocurred!: %s", e)


    def record_event_tags(self, measurement, tags, fields, time=None):
        from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError

        if time is None:
            time = datetime.utcnow()
            #if 'UTC' in time.tzname:
            #    time = pytz.timezone('UTC').localize(time)
            #else:
            #    time = pytz.timezone('US/Mountain').localize(time)
            #    time = time.astimezone(pytz.UTC)
        else:
            time = datetime.utcnow()
            hour, minute = (int(x) for x in time.split(":"))
            
            time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            #if 'UTC' in time.tzname:
            #    time = pytz.timezone('UTC').localize(time)
            #else:
            #    time = pytz.timezone('US/Mountain').localize(time)
            #    time = time.astimezone(pytz.UTC)

        try:
            LOGGER.debug("Adding tags: {}, values: {} at {} to table: {} in database.".format(tags, fields, time, measurement))
            data = {
                'measurement': measurement,
                'tags': tags,
                'time': time,
                'fields': fields
            }

            if self._queue is not None and not self._queue:
                data = [[v for k, v in sorted(data.items())]]
                self._queue.push(data)
            else:
                self.client.write_points([data])

        except (InfluxDBClientError, InfluxDBServerError) as e:
            LOGGER.error("Unable to add an event to database: %s", e)
        except Exception as e:
            LOGGER.error("An exception ocurred!: %s", e)

    def batch_upload(self, data):
        from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError

        try:
            LOGGER.info("Adding tags: {}, values: {} at {} to table: {} in database.".format(tags, fields, time, measurement))

            self.client.write_points(data)
            return True

        except (InfluxDBClientError, InfluxDBServerError) as e:
            LOGGER.error("Unable to add events to database: %s", e)
            raise e
        
        return False

