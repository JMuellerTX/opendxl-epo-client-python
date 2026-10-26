# This sample looks up an ePO query by name with the "core.listQueries" remote
# command and runs it with the "core.executeQuery" remote command via the ePO
# DXL service.
#
# NOTE: Prior to running this sample you must provide values for the following
#       constants in this file:
#
#       EPO_UNIQUE_ID : The unique identifier used to identify the ePO server
#                       on the DXL fabric.
#
#                       If only one ePO server is connected to the DXL fabric
#                       this constant can be set to None (the client will
#                       automatically determine the ePO's unique identifier).
#                       If several ePO servers are connected, set it
#                       explicitly (see EpoClient.lookup_epo_unique_identifiers).
#
#       QUERY_NAME    : The name of the ePO query to run.

from __future__ import absolute_import
from __future__ import print_function
import os
import sys

from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlbootstrap.util import MessageUtils
from dxlepoclient import EpoClient

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# The ePO unique identifier
EPO_UNIQUE_ID = None

# The name of the query to run
QUERY_NAME = "My Query"

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    # Create the ePO client
    epo_client = EpoClient(client, EPO_UNIQUE_ID)

    # List the queries that are defined on the ePO server. The parameters of
    # "core.listQueries" can be checked with the "core.help" command (see the
    # basic_core_help_example.py sample).
    queries = MessageUtils.json_to_dict(
        epo_client.run_command("core.listQueries"))

    # Find the query by name
    query_id = None
    for query in queries:
        if query.get("name") == QUERY_NAME:
            query_id = query.get("id")
            break

    if query_id is None:
        print("Query not found: " + QUERY_NAME)
        sys.exit(1)

    # Run the query
    res = epo_client.run_command("core.executeQuery", {"queryId": query_id})

    # Display the results
    print(MessageUtils.dict_to_json(MessageUtils.json_to_dict(res),
                                    pretty_print=True))
