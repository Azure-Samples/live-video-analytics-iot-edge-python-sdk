import urllib3
import json
from datetime import datetime, timezone
import dateutil.parser
from dateutil.relativedelta import relativedelta
import adal
from msrestazure.azure_active_directory import AdalAuthentication
from msrestazure.azure_cloud import AZURE_PUBLIC_CLOUD
from azure.mgmt.media import AzureMediaServices
from azure.mgmt.media.models import StreamingLocator
from config import Config
import pandas as pd


class AmsHelper(object):

    def __init__(self):
        self.media_service_client = None
        self.__create_media_service_client()

    def __create_media_service_client(self):
        LOGIN_ENDPOINT = AZURE_PUBLIC_CLOUD.endpoints.active_directory
        RESOURCE = AZURE_PUBLIC_CLOUD.endpoints.active_directory_resource_id

        context = adal.AuthenticationContext(
            LOGIN_ENDPOINT + '/' + Config.AAD_TENANT_ID
        )
        credentials = AdalAuthentication(
            context.acquire_token_with_client_credentials,
            RESOURCE,
            Config.AAD_CLIENT_ID,
            Config.AAD_SECRET
        )

        self.media_service_client = AzureMediaServices(
            credentials,
            Config.SUBSCRIPTION_ID
        )

    def __create_streaming_locator(self, locator: str, asset: str):
        return self.media_service_client.streaming_locators.create(
            Config.RESOURCE_GROUP,
            Config.ACCOUNT_ID,
            locator,
            StreamingLocator(
                asset_name=asset,
                streaming_policy_name='Predefined_DownloadAndClearStreaming'
            )
        )

    def __get_default_streaming_endpoint(self):
        streaming_endpoints = self.media_service_client.streaming_endpoints \
            .list(
                Config.RESOURCE_GROUP,
                Config.ACCOUNT_ID
            )

        streaming_endpoint = next(
            (x for x in streaming_endpoints if x.name == 'default')
            , None
        )

        return streaming_endpoint

    def get_streaming_locator(self, asset: str):
        try:
            locators = self.media_service_client.assets \
                .list_streaming_locators(
                    Config.RESOURCE_GROUP,
                    Config.ACCOUNT_ID,
                    asset
                )

            if locators:
                locator = self.media_service_client.streaming_locators.get(
                    Config.RESOURCE_GROUP,
                    Config.ACCOUNT_ID,
                    locators.streaming_locators[0].name
                )

                return locator
        except Exception:
            pass

    def get_streaming_url(self, asset):
        try:
            streaming_locator = self.get_streaming_locator(asset)

            if not streaming_locator:
                s_time = datetime(
                    1970, 1, 1, 0, 0, 0, 0, timezone.utc
                )

                epoch = (datetime.now - s_time).second()
                locator_name = 'locator_' + epoch

                streaming_locator = self.__create_streaming_locator(
                    locator_name,
                    asset
                )

            streaming_endpoint = self.__get_default_streaming_endpoint()
            url = 'https://' + streaming_endpoint.host_name + '/' + streaming_locator.streaming_locator_id + '/content.ism/manifest'

            return url

        except Exception:
            pass

    def get_available_media_timeranges(self, asset: str, precision: str, start_time: str, end_time: str):
        try:
            streaming_locator = self.get_streaming_locator(asset)
            streaming_endpoint = self.__get_default_streaming_endpoint()

            available_timeranges_url = 'https://' + streaming_endpoint.host_name + '/' + streaming_locator.streaming_locator_id + '/content.ism/availableMedia?precision=' + precision + '&startTime=' + start_time + '&endTime=' + end_time

            return AmsHelper.download_from_url(available_timeranges_url)
        except Exception:
            pass

    @staticmethod
    def download_from_url(url: str):
        http = urllib3.PoolManager()

        r = http.request('GET', url)
        if r.status == 200:
            return r.data.decode('utf-8')
    
    @staticmethod
    def get_available_mediatime(available_timeranges_text: str, precision: str):
        
        obj_time = []

        available_timeranges = json.loads(available_timeranges_text)

        for time_range in available_timeranges['timeRanges']:
            start_time = time_range['start']
            end_time = time_range['end']

            dt_start = datetime.now()
            dt_end = datetime.now()

            if precision == 'year':
                dt_start = pd.to_datetime(start_time)
                dt_end = pd.to_datetime(end_time)
            elif precision == 'month':
                dt_start = pd.to_datetime(start_time)
                dt_end = pd.to_datetime(end_time)
            elif precision == 'day':
                dt_start = pd.to_datetime(start_time)
                dt_end = pd.to_datetime(end_time)
            elif precision == 'full':
                dt_start = dateutil.parser.parse(start_time)
                dt_end = dateutil.parser.parse(end_time)

            while True:
                t_obj = dict()

                if precision == 'year':
                    t_obj['id'] = dt_start.strftime('%Y')
                    t_obj['value'] = t_obj['id']
                    dt_start = dt_start + relativedelta(years=1)
                elif precision == 'month':
                    t_obj['id'] = dt_start.strftime('%Y-%m')
                    t_obj['value'] = dt_start.strftime('%b')
                    dt_start = dt_start + relativedelta(months=1)
                elif precision == 'day':
                    t_obj['id'] = dt_start.strftime('%Y-%m-%d')
                    t_obj['value'] = dt_start.strftime('%d')
                    dt_start = dt_start + relativedelta(days=1)
                elif precision == 'full':
                    t_obj['id'] = dt_start.strftime('%Y-%m-%d-%H:%M:%S')
                    t_obj['value'] = dt_start.strftime('%H:%M:%S') + ' to ' + dt_end.strftime('%H:%M:%S')
                    dt_start = dt_end + relativedelta(seconds=1)

                obj_time.append(t_obj)

                if dt_start > dt_end:
                    break

        return json.dumps(obj_time, ensure_ascii=False)
