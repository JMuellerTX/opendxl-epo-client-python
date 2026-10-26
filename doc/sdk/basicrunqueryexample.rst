Basic Run Query Example
=======================

This sample looks up an ePO query by name with the "core.listQueries" remote command and runs it with the
"core.executeQuery" remote command via the ePO DXL service. The results of the query are displayed in JSON format.

Prerequisites
*************

* The samples configuration step has been completed (see :doc:`sampleconfig`)
* An ePO DXL service is running and available on the fabric. If version 5.0
  or later of the DXL ePO extensions are installed on your ePO server, an
  ePO DXL service should already be running on the fabric. If you are using an
  earlier version of the DXL ePO extensions, you can use the
  `ePO DXL Python Service <https://github.com/opendxl/opendxl-epo-service-python>`_.
* The client is authorized to invoke the ePO DXL Service, and the user that is
  connecting to the ePO server (within the ePO DXL service) has permission to
  execute the "core.listQueries" and "core.executeQuery" remote commands (see :doc:`authorization`).
* A query with the name given in ``QUERY_NAME`` exists on the ePO server.

Setup
*****

Modify the example to include the name of the query to run:

    .. code-block:: python

        QUERY_NAME = "My Query"

The `unique identifier` of the ePO server is left at ``None`` by default. The client then determines it by querying
the DXL service registry. This only works if exactly one ePO server is connected to the fabric. If several ePO
servers are connected, set ``EPO_UNIQUE_ID`` explicitly. The identifiers that are currently on the fabric can be
listed with :func:`dxlepoclient.client.EpoClient.lookup_epo_unique_identifiers`. Do not hard-code the identifier in
a request topic: it changes when the ePO server is migrated, and requests to the old topic are then never answered.

Running
*******

To run this sample execute the ``sample/basic/basic_run_query_example.py`` script as follows:

    .. parsed-literal::

        python sample/basic/basic_run_query_example.py

The output is the JSON result of the query. If no query with the given name exists, the sample prints
``Query not found: <name>`` and exits with a non-zero exit code.

Details
*******

The majority of the sample code is shown below:

    .. code-block:: python

        # Create the ePO client
        epo_client = EpoClient(client, EPO_UNIQUE_ID)

        queries = MessageUtils.json_to_dict(
            epo_client.run_command("core.listQueries"))

        query_id = None
        for query in queries:
            if query.get("name") == QUERY_NAME:
                query_id = query.get("id")
                break

        if query_id is None:
            print("Query not found: " + QUERY_NAME)
            sys.exit(1)

        res = epo_client.run_command("core.executeQuery", {"queryId": query_id})
        print(MessageUtils.dict_to_json(MessageUtils.json_to_dict(res),
                                        pretty_print=True))

:func:`dxlepoclient.client.EpoClient.run_command` returns the response as a string, which
:func:`dxlbootstrap.util.MessageUtils.json_to_dict` converts to Python objects. The query is found by name; if it is
missing, the sample stops with a clear message instead of continuing with an undefined query identifier.

The parameters of "core.listQueries" and "core.executeQuery" depend on the ePO version. Check them with the
"core.help" command (see :doc:`basiccorehelpexample`) before relying on a parameter such as a query filter.
