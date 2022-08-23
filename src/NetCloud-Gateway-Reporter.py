import configparser
import os

import pandas as pd
import requests


# Module information.
__author__ = 'Anthony Farina'
__copyright__ = 'Copyright (C) 2022 CC Digital Innovation'
__credits__ = ['Anthony Farina']
__maintainer__ = 'Anthony Farina'
__email__ = 'farinaanthony96@gmail.com'
__license__ = 'MIT'
__version__ = '1.0.0'
__status__ = 'Released'


# Global config file variables for easy referencing.
CONFIG = configparser.ConfigParser()
CONFIG_PATH = '/../configs/NetCloud-Gateway-Reporter-config.ini'
CONFIG.read(os.path.dirname(os.path.realpath(__file__)) + CONFIG_PATH)

# NetCloud global variables.
NC_API_URL = 'https://www.cradlepointecm.com/api/v2/'
NC_CP_API_ID = CONFIG['NetCloud API Info']['cp-api-id']
NC_CP_API_KEY = CONFIG['NetCloud API Info']['cp-api-key']
NC_ECM_API_ID = CONFIG['NetCloud API Info']['ecm-api-id']
NC_ECM_API_KEY = CONFIG['NetCloud API Info']['ecm-api-key']
NC_API_HEADERS = {
    'X-CP-API-ID': NC_CP_API_ID,
    'X-CP-API-KEY': NC_CP_API_KEY,
    'X-ECM-API-ID': NC_ECM_API_ID,
    'X-ECM-API-KEY': NC_ECM_API_KEY,
    'Content-Type': 'application/json'
}

# Other global variables.
EXCEL_FILE_NAME = CONFIG['Output Info']['excel-file-name']
COL_LABELS = [
    'Router Name',
    'Gateway IP'
]


# Generates a report that contains all routers connected to NetCloud
# and their associated gateway IPv4 addresses.
def netcloud_gateway_reporter() -> None:
    # Get all routers from NetCloud and convert the response to JSON.
    nc_routers_resp = requests.get(url=NC_API_URL + 'routers/',
                                   headers=NC_API_HEADERS,
                                   params={
                                       'limit': '500',
                                       'fields': 'name,id'
                                   }
                                   )
    nc_routers_json = nc_routers_resp.json()

    # Go through the first batch of NetCloud routers.
    is_next_batch = True
    nc_routers_dict = dict()
    while is_next_batch:
        # Store all NetCloud routers in this batch to the router dictionary.
        for nc_router in nc_routers_json['data']:
            # Check if this router has not been added to the router dictionary.
            if nc_router['id'] not in nc_routers_dict.keys():
                nc_routers_dict[nc_router['id']] = {
                    'name': nc_router['name']
                }

        # Check if there are no more batches of NetCloud routers.
        if nc_routers_json['meta']['next'] is None:
            is_next_batch = False
        else:
            # Get the next batch of NetCloud routers.
            nc_routers_resp = requests.get(url=nc_routers_json['meta']['next'],
                                           headers=NC_API_HEADERS,
                                           params={
                                               'limit': '500',
                                               'fields': 'name,id'
                                           }
                                           )
            nc_routers_json = nc_routers_resp.json()

    # Get all net devices from NetCloud and convert the response to JSON.
    nc_net_devs_resp = requests.get(url=NC_API_URL + 'net_devices/',
                                    headers=NC_API_HEADERS,
                                    params={
                                        'limit': '500',
                                        'fields': 'name,router,gateway'
                                    }
                                    )
    nc_net_devs_batch = nc_net_devs_resp.json()

    # Go through each batch of network devices to extract their
    # gateway IP addresses.
    next_device_batch = True
    output_list = list()
    while next_device_batch:
        # Go through this batch of network devices.
        for nc_net_device in nc_net_devs_batch['data']:
            # We only want to extract the ethernet-wan gateway IPs.
            if nc_net_device['name'] == 'ethernet-wan':
                # Prepare to make a record.
                record_list = list()

                # Check if this net device's router isn't in our
                # router dictionary.
                router_id = nc_net_device['router'].split('/')[6]
                if router_id not in nc_routers_dict.keys():
                    print('Router not found for this net device: ' +
                          nc_net_device['router'])
                    continue

                # Create and add this record to the output list.
                record_list.append(nc_routers_dict[router_id]['name'])
                record_list.append(str(nc_net_device['gateway']))
                output_list.append(record_list)

        # Check if there is another batch of network devices.
        if nc_net_devs_batch['meta']['next'] is None:
            next_device_batch = False
        else:
            # Extract the next batch of network devices from NetCloud
            # in JSON format.
            nc_next_net_dev_batch_resp = \
                requests.get(url=nc_net_devs_batch['meta']['next'],
                             headers=NC_API_HEADERS)
            nc_net_devs_batch = nc_next_net_dev_batch_resp.json()

    # Make the dataframe of the data, sort it, and export it to an
    # Excel sheet.
    output_df = pd.DataFrame(output_list, columns=COL_LABELS)
    output_df = output_df.sort_values(by=['Router Name'])
    output_df.to_excel(EXCEL_FILE_NAME + '.xlsx', index=None, header=True)


# The main method that runs the script. There are no input parameters.
if __name__ == '__main__':
    # Run the script.
    netcloud_gateway_reporter()
