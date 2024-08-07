"""PDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

This module contains an initial version of the feedback_manager_omvs
module.

"""

import asyncio
import json

from httpx import Response

from pyegeria import body_slimmer
# import json
from pyegeria._client import Client, max_paging_size
from pyegeria._globals import enable_ssl_check, default_time_out


def jprint(info, comment=None):
    if comment:
        print(comment)
    print(json.dumps(info, indent=2))


def query_seperator(current_string):
    if current_string == "":
        return "?"
    else:
        return "&"


"params are in the form of [(paramName, value), (param2Name, value)] if the value is not None, it will be added to the query string"


def query_string(params):
    result = ""
    for i in range(len(params)):
        if params[i][1] is not None:
            result = f"{result}{query_seperator(result)}{params[i][0]}={params[i][1]}"
    return result


def base_path(client, view_server: str):
    return f"{client.platform_url}/servers/{view_server}/api/open-metadata/classification-manager"


def extract_relationships_plus(element):
    type_name = element["relatedElement"]["type"]["typeName"]
    guid = element["relationshipHeader"]["guid"]
    properties = element["relationshipProperties"]["propertiesAsStrings"]
    name = element["relatedElement"]["uniqueName"]
    return {"name": name, "typeName": type_name, "guid": guid, "properties": properties}


def extract_related_elements_list(element_list):
    return [extract_relationships_plus(element) for element in element_list]


def related_elements_response(response: dict, detailed_response: bool):
    if detailed_response:
        return response
    else:
        return extract_related_elements_list(response["elements"])


def element_properties_plus(element):
    props_plus = element["properties"]
    props_plus.update({"guid": element["elementHeader"]["guid"]})
    props_plus.update({"versions": element["elementHeader"]["versions"]})
    return props_plus


def element_property_plus_list(element_list):
    return [element_properties_plus(element) for element in element_list]


def element_response(response: dict, element_type: str, detailed_response: bool):
    if detailed_response:
        return response
    else:
        return element_properties_plus(response[element_type])


def elements_response(response: dict, element_type: str, detailed_response: bool):
    if detailed_response:
        return response
    else:
        return element_property_plus_list(response[element_type])


class ClassificationManager(Client):
    """ClassificationManager is a class that extends the Client class. It
    provides methods to CRUD annotations and to query elements and relationships. Async version.

    Attributes:

        server_name: str
            The name of the View Server to connect to.
        platform_url : str
            URL of the server platform to connect to
        user_id : str
            The identity of the user calling the method - this sets a
            default optionally used by the methods when the user
            doesn't pass the user_id on a method call.
         user_pwd: str
            The password associated with the user_id. Defaults to None
        verify_flag: bool
            Flag to indicate if SSL Certificates should be verified in the HTTP
            requests.
            Defaults to False.

    """

    def __init__(self, server_name: str, platform_url: str, token: str = None, user_id: str = None,
            user_pwd: str = None, verify_flag: bool = enable_ssl_check, sync_mode: bool = True, ):
        self.admin_command_root: str
        Client.__init__(self, server_name, platform_url, user_id=user_id, user_pwd=user_pwd, token=token,
            async_mode=sync_mode, )

    #
    #   Get elements
    #
    async def _async_get_elements(self, open_metadata_type_name: str = None, effective_time: str = None,
            for_lineage: bool = None, for_duplicate_processing: bool = None, start_from: int = 0,
            page_size: int = max_paging_size, server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements of the requested type name. If no type name is specified, then any type of element may
        be returned.

        https://egeria-project.org/types/

        Parameters
        ----------
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """
        if server_name is None:
            server_name = self.server_name

        possible_query_params = query_string(
            [("startFrom", start_from), ("pageSize", page_size), ("forLineage", for_lineage),
                ("forDuplicateProcessing", for_duplicate_processing)])

        body = {"class": "FindProperties", "openMetadataTypeName": open_metadata_type_name,
            "effectiveTime": effective_time, }

        url = f"{base_path(self, server_name)}/elements/by-type{possible_query_params}"
        response: Response = await self._async_make_request("POST", url, body_slimmer(body), time_out=time_out)
        elements = response.json().get('elements', 'No elements found')
        if type(elements) is list:
            if len(elements) == 0:
                return "No elements found"
        return elements

    def get_elements(self, open_metadata_type_name: str = None, effective_time: str = None, for_lineage: bool = None,
            for_duplicate_processing: bool = None, start_from: int = 0, page_size: int = max_paging_size,
            server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements of the requested type name. If no type name is specified, then any type of element may
        be returned.

        https://egeria-project.org/types/

        Parameters
        ----------
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_elements(open_metadata_type_name, effective_time, for_lineage, for_duplicate_processing,
                start_from, page_size, server_name, time_out))
        return response

    async def _async_get_elements_by_property_value(self, property_value: str, property_names: [str],
            open_metadata_type_name: str = None, effective_time: str = None, for_lineage: bool = None,
            for_duplicate_processing: bool = None, start_from: int = 0, page_size: int = max_paging_size,
            server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements by a value found in one of the properties specified.  The value must match exactly.
        An open metadata type name may be supplied to restrict the results. Async version.

        https://egeria-project.org/types/

        Parameters
        ----------
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """
        if server_name is None:
            server_name = self.server_name

        possible_query_params = query_string(
            [("startFrom", start_from), ("pageSize", page_size), ("forLineage", for_lineage),
                ("forDuplicateProcessing", for_duplicate_processing)])

        body = {"class": "FindPropertyNamesProperties", "openMetadataTypeName": open_metadata_type_name,
            "propertyValue": property_value, "propertyNames": property_names, "effectiveTime": effective_time, }

        url = f"{base_path(self, server_name)}/elements/by-exact-property-value{possible_query_params}"

        response: Response = await self._async_make_request("POST", url, body_slimmer(body), time_out=time_out)

        elements = response.json().get('elements', 'No elements found')
        if type(elements) is list:
            if len(elements) == 0:
                return "No elements found"
        return elements

    def get_elements_by_property_value(self, property_value: str, property_names: [str],
            open_metadata_type_name: str = None, effective_time: str = None, for_lineage: bool = None,
            for_duplicate_processing: bool = None, start_from: int = 0, page_size: int = max_paging_size,
            server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements by a value found in one of the properties specified.  The value must match exactly.
        An open metadata type name may be supplied to restrict the results.

        https://egeria-project.org/types/

        Parameters
        ----------
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_elements_by_property_value(property_value, property_names, open_metadata_type_name,
                effective_time, for_lineage, for_duplicate_processing, start_from, page_size, server_name, time_out))
        return response

    async def _async_find_elements_by_property_value(self, property_value: str, property_names: [str],
            open_metadata_type_name: str = None, effective_time: str = None, for_lineage: bool = None,
            for_duplicate_processing: bool = None, start_from: int = 0, page_size: int = max_paging_size,
            server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements by a value found in one of the properties specified.  The value must be contained in the
        properties rather than needing to be an exact match. An open metadata type name may be supplied to restrict
        the results. Async version.

        https://egeria-project.org/types/

        Parameters
        ----------
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """
        if server_name is None:
            server_name = self.server_name

        possible_query_params = query_string(
            [("startFrom", start_from), ("pageSize", page_size), ("forLineage", for_lineage),
                ("forDuplicateProcessing", for_duplicate_processing)])

        body = {"class": "FindPropertyNamesProperties", "openMetadataTypeName": open_metadata_type_name,
            "propertyValue": property_value, "propertyNames": property_names, "effectiveTime": effective_time, }

        url = f"{base_path(self, server_name)}/elements/by-property-value-search{possible_query_params}"
        response: Response = await self._async_make_request("POST", url, body_slimmer(body), time_out=time_out)
        elements = response.json().get('elements', 'No elements found')
        if type(elements) is list:
            if len(elements) == 0:
                return "No elements found"
        return elements

    def find_elements_by_property_value(self, property_value: str, property_names: [str],
            open_metadata_type_name: str = None, effective_time: str = None, for_lineage: bool = None,
            for_duplicate_processing: bool = None, start_from: int = 0, page_size: int = max_paging_size,
            server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements by a value found in one of the properties specified.  The value must be contained in the
        properties rather than needing to be an exact match. An open metadata type name may be supplied to restrict
        the results.

        https://egeria-project.org/types/

        Parameters
        ----------
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_find_elements_by_property_value(property_value, property_names, open_metadata_type_name,
                effective_time, for_lineage, for_duplicate_processing, start_from, page_size, server_name, time_out))
        return response

    #
    # Elements by classification
    #
    async def _async_get_elements_by_classification(self, classification_name: str, open_metadata_type_name: str = None,
            effective_time: str = None, for_lineage: bool = None, for_duplicate_processing: bool = None,
            start_from: int = 0, page_size: int = max_paging_size, server_name: str = None,
            time_out: int = default_time_out) -> list | str:
        """
         Retrieve elements with the requested classification name. It is also possible to limit the results
        by specifying a type name for the elements that should be returned. If no type name is specified then
        any type of element may be returned. Async version.

        https://egeria-project.org/types/

        Parameters
        ----------
        classification_name: str
            - the classification name to retrieve elements for.
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        effective_time: str, default = None
            - Time format is "YYYY-MM-DD THH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """
        if server_name is None:
            server_name = self.server_name

        possible_query_params = query_string(
            [("startFrom", start_from), ("pageSize", page_size), ("forLineage", for_lineage),
                ("forDuplicateProcessing", for_duplicate_processing)])

        body = {"class": "FindProperties", "openMetadataTypeName": open_metadata_type_name,
            "effectiveTime": effective_time, }

        url = (f"{base_path(self, server_name)}/elements/by-classification/{classification_name}"
               f"{possible_query_params}")
        response = await self._async_make_request("POST", url, body_slimmer(body), time_out=time_out)
        elements = response.json().get('elements', 'No elements found')
        if type(elements) is list:
            if len(elements) == 0:
                return "No elements found"
        return elements

    def get_elements_by_classification(self, classification_name: str, open_metadata_type_name: str = None,
            effective_time: str = None, for_lineage: bool = None, for_duplicate_processing: bool = None,
            start_from: int = 0, page_size: int = max_paging_size, server_name: str = None,
            time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements with the requested classification name. It is also possible to limit the results
        by specifying a type name for the elements that should be returned. If no type name is specified then
        any type of element may be returned.

        https://egeria-project.org/types/

        Parameters
        ----------
        classification_name: str
            - the classification name to retrieve elements for.
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_elements_by_classification(classification_name, open_metadata_type_name, effective_time,
                for_lineage, for_duplicate_processing, start_from, page_size, server_name, time_out))
        return response

    async def _async_get_elements_by_classification_with_property_value(self, classification_name: str,
            property_value: str, property_names: [str], open_metadata_type_name: str = None, effective_time: str = None,
            for_lineage: bool = None, for_duplicate_processing: bool = None, start_from: int = 0,
            page_size: int = max_paging_size, server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
       Retrieve elements with the requested classification name and with the requested a value found in one of the
       classification's properties specified.  The value must match exactly. An open metadata type name may be supplied
       to restrict the types of elements returned. Async version.

        https://egeria-project.org/types/

        Parameters
        ----------
        classification_name: str
            - the classification name to retrieve elements for.
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """
        if server_name is None:
            server_name = self.server_name

        possible_query_params = query_string(
            [("startFrom", start_from), ("pageSize", page_size), ("forLineage", for_lineage),
                ("forDuplicateProcessing", for_duplicate_processing)])

        body = {"class": "FindPropertyNamesProperties", "openMetadataTypeName": open_metadata_type_name,
            "propertyValue": property_value, "propertyNames": property_names, "effectiveTime": effective_time, }

        url = (f"{base_path(self, server_name)}/elements/by-classification/{classification_name}/"
               f"with-exact-property-value{possible_query_params}")
        response = await self._async_make_request("POST", url, body_slimmer(body), time_out=time_out)
        elements = response.json().get('elements', 'No elements found')
        if type(elements) is list:
            if len(elements) == 0:
                return "No elements found"
        return elements

    def get_elements_by_classification_with_property_value(self, classification_name: str, property_value: str,
            property_names: [str], open_metadata_type_name: str = None, effective_time: str = None,
            for_lineage: bool = None, for_duplicate_processing: bool = None, start_from: int = 0,
            page_size: int = max_paging_size, server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements by a value found in one of the properties specified.  The value must match exactly.
        An open metadata type name may be supplied to restrict the results.

        https://egeria-project.org/types/

        Parameters
        ----------
        classification_name: str
            - the classification name to retrieve elements for.
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_elements_by_classification_with_property_value(classification_name, property_value,
                property_names, open_metadata_type_name, effective_time, for_lineage, for_duplicate_processing,
                start_from, page_size, server_name, time_out))
        return response

    async def _async_find_elements_by_classification_with_property_value(self, classification_name: str,
            property_value: str, property_names: [str], open_metadata_type_name: str = None, effective_time: str = None,
            for_lineage: bool = None, for_duplicate_processing: bool = None, start_from: int = 0,
            page_size: int = max_paging_size, server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements with the requested classification name and with the requested value found in
        one of the classification's properties specified.  The value must only be contained in the
        properties rather than needing to be an exact match.
        An open metadata type name may be supplied to restrict the results. Async version.

        https://egeria-project.org/types/

        Parameters
        ----------
        classification_name: str
            - the classification name to retrieve elements for.
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """
        if server_name is None:
            server_name = self.server_name

        possible_query_params = query_string(
            [("startFrom", start_from), ("pageSize", page_size), ("forLineage", for_lineage),
                ("forDuplicateProcessing", for_duplicate_processing)])

        body = {"class": "FindPropertyNamesProperties", "openMetadataTypeName": open_metadata_type_name,
            "propertyValue": property_value, "propertyNames": property_names, "effectiveTime": effective_time, }

        url = (f"{base_path(self, server_name)}/elements/by-classification/{classification_name}/"
               f"with-property-value-search{possible_query_params}")
        response = await self._async_make_request("POST", url, body_slimmer(body), time_out=time_out)
        elements = response.json().get('elements', 'No elements found')
        if type(elements) is list:
            if len(elements) == 0:
                return "No elements found"
        return elements

    def find_elements_by_classification_with_property_value(self, classification_name: str, property_value: str,
            property_names: [str], open_metadata_type_name: str = None, effective_time: str = None,
            for_lineage: bool = None, for_duplicate_processing: bool = None, start_from: int = 0,
            page_size: int = max_paging_size, server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements with the requested classification name and with the requested a value found in
        one of the classification's properties specified.  The value must only be contained in the
        properties rather than needing to be an exact match.
        An open metadata type name may be supplied to restrict the results.

        https://egeria-project.org/types/

        Parameters
        ----------
        classification_name: str
            - the classification name to retrieve elements for.
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_find_elements_by_classification_with_property_value(classification_name, property_value,
                property_names, open_metadata_type_name, effective_time, for_lineage, for_duplicate_processing,
                start_from, page_size, server_name, time_out))
        return response

    #
    #   related elements
    #
    async def _async_get_all_related_elements(self, element_guid: str, open_metadata_type_name: str = None,
            start_at_end: int = 1, effective_time: str = None, for_lineage: bool = None,
            for_duplicate_processing: bool = None, start_from: int = 0, page_size: int = max_paging_size,
            server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements linked any relationship type name. It is also possible to limit the results by
        specifying a type name for the elements that should be returned. If no type name is specified then any type of
        element may be returned. Async version.

        https://egeria-project.org/types/

        Parameters
        ----------
        element_guid: str
            - the base element to get related elements for
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        start_at_end: int, default = 1
            - The end of the relationship to start from - typically End1
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """
        if server_name is None:
            server_name = self.server_name

        possible_query_params = query_string(
            [("startFrom", start_from), ("pageSize", page_size), ("forLineage", for_lineage),
                ("forDuplicateProcessing", for_duplicate_processing), ("startAtEnd", start_at_end)])

        body = {"class": "FindProperties", "openMetadataTypeName": open_metadata_type_name,
            "effectiveTime": effective_time, }

        url = (f"{base_path(self, server_name)}/elements/{element_guid}/by-relationship"
               f"{possible_query_params}")
        response: Response = await self._async_make_request("POST", url, body_slimmer(body), time_out=time_out)
        elements = response.json().get('elements', 'No elements found')
        if type(elements) is list:
            if len(elements) == 0:
                return "No elements found"
        return elements

    def get_all_related_elements(self, element_guid: str, open_metadata_type_name: str = None, start_at_end: int = 1,
            effective_time: str = None, for_lineage: bool = None, for_duplicate_processing: bool = None,
            start_from: int = 0, page_size: int = max_paging_size, server_name: str = None,
            time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements linked via any relationship type name. It is also possible to limit the results by
        specifying a type name for the elements that should be returned. If no type name is specified then any type of
        element may be returned.

        https://egeria-project.org/types/

        Parameters
        ----------
        element_guid: str
            - the base element to get related elements for
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        start_at_end: int, default = 1
            - The end of the relationship to start from - typically End1
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_all_related_elements(element_guid, open_metadata_type_name, start_at_end, effective_time,
                for_lineage, for_duplicate_processing, start_from, page_size, server_name, time_out))
        return response

    async def _async_get_related_elements(self, element_guid: str, relationship_type: str,
            open_metadata_type_name: str = None, start_at_end: int = 1, effective_time: str = None,
            for_lineage: bool = None, for_duplicate_processing: bool = None, start_from: int = 0,
            page_size: int = max_paging_size, server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements linked any relationship type name. It is also possible to limit the results by
        specifying a type name for the elements that should be returned. If no type name is specified then any type of
        element may be returned. Async version.

        https://egeria-project.org/types/

        Parameters
        ----------
        element_guid: str
            - the base element to get related elements for
        relationship_type: str
            - the type of relationship to navigate to related elements
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        start_at_end: int, default = 1
            - The end of the relationship to start from - typically End1
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """
        if server_name is None:
            server_name = self.server_name

        possible_query_params = query_string(
            [("startFrom", start_from), ("pageSize", page_size), ("forLineage", for_lineage),
                ("forDuplicateProcessing", for_duplicate_processing), ("startAtEnd", start_at_end)])

        body = {"class": "FindProperties", "openMetadataTypeName": open_metadata_type_name,
            "effectiveTime": effective_time, }

        url = (f"{base_path(self, server_name)}/elements/{element_guid}/by-relationship/"
               f"{relationship_type}{possible_query_params}")
        response: Response = await self._async_make_request("POST", url, body_slimmer(body), time_out=time_out)
        elements = response.json().get('elements', 'No elements found')
        if type(elements) is list:
            if len(elements) == 0:
                return "No elements found"
        return elements

    def get_related_elements(self, element_guid: str, relationship_type: str, open_metadata_type_name: str = None,
            start_at_end: int = 1, effective_time: str = None, for_lineage: bool = None,
            for_duplicate_processing: bool = None, start_from: int = 0, page_size: int = max_paging_size,
            server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements linked via any relationship type name. It is also possible to limit the results by
        specifying a type name for the elements that should be returned. If no type name is specified then any type of
        element may be returned.

        https://egeria-project.org/types/

        Parameters
        ----------
        element_guid: str
            - the base element to get related elements for
        relationship_type: str
            - the type of relationship to navigate to related elements
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        start_at_end: int, default = 1
            - The end of the relationship to start from - typically End1
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_related_elements(element_guid, relationship_type, open_metadata_type_name, start_at_end,
                effective_time, for_lineage, for_duplicate_processing, start_from, page_size, server_name, time_out))
        return response

    async def _async_get_related_elements_with_property_value(self, element_guid: str, relationship_type: str,
            property_value: str, property_names: [str], open_metadata_type_name: str = None, start_at_end: int = 1,
            effective_time: str = None, for_lineage: bool = None, for_duplicate_processing: bool = None,
            start_from: int = 0, page_size: int = max_paging_size, server_name: str = None,
            time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements linked via the requested relationship type name and with the requested a value found in one of
        the classification's properties specified.  The value must match exactly. An open metadata type name may be
        supplied to restrict the types of elements returned. Async version.

        https://egeria-project.org/types/

        Parameters
        ----------
        element_guid: str
            - the base element to get related elements for
        relationship_type: str
            - the type of relationship to navigate to related elements
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        open_metadata_type_name : str, default = None
            - restrict search to elements of this open metadata type
        start_at_end: int, default = 1
            - The end of the relationship to start from - typically End1
            - open metadata type to be used to restrict the search
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """
        if server_name is None:
            server_name = self.server_name

        possible_query_params = query_string(
            [("startFrom", start_from), ("pageSize", page_size), ("forLineage", for_lineage),
                ("forDuplicateProcessing", for_duplicate_processing), ("startAtEnd", start_at_end)])

        body = {"class": "FindPropertyNamesProperties", "openMetadataTypeName": open_metadata_type_name,
            "propertyValue": property_value, "propertyNames": property_names, "effectiveTime": effective_time, }

        url = (f"{base_path(self, server_name)}/elements/{element_guid}/by-relationship/"
               f"{relationship_type}/with-exact-property-value{possible_query_params}")

        response: Response = await self._async_make_request("POST", url, body_slimmer(body), time_out=time_out)
        elements = response.json().get('elements', 'No elements found')
        if type(elements) is list:
            if len(elements) == 0:
                return "No elements found"
        return elements

    def get_related_elements_with_property_value(self, element_guid: str, relationship_type: str, property_value: str,
            property_names: [str], open_metadata_type_name: str = None, start_at_end: int = 1,
            effective_time: str = None, for_lineage: bool = None, for_duplicate_processing: bool = None,
            start_from: int = 0, page_size: int = max_paging_size, server_name: str = None,
            time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements linked via the requested relationship type name and with the requested a value found in one of
        the classification's properties specified.  The value must match exactly. An open metadata type name may be
        supplied to restrict the types of elements returned.

        https://egeria-project.org/types/

        Parameters
        ----------
        element_guid: str
            - the base element to get related elements for
        relationship_type: str
            - the type of relationship to navigate to related elements
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        start_at_end: int, default = 1
            - The end of the relationship to start from - typically End1
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_related_elements_with_property_value(element_guid, relationship_type, property_value,
                property_names, open_metadata_type_name, start_at_end, effective_time, for_lineage,
                for_duplicate_processing, start_from, page_size, server_name, time_out))
        return response

    async def _async_find_related_elements_with_property_value(self, element_guid: str, relationship_type: str,
            property_value: str, property_names: [str], open_metadata_type_name: str = None, start_at_end: int = 1,
            effective_time: str = None, for_lineage: bool = None, for_duplicate_processing: bool = None,
            start_from: int = 0, page_size: int = max_paging_size, server_name: str = None,
            time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements linked via the requested relationship type name and with the requested a value found in one of
        the classification's properties specified.  The value must only be contained in the properties rather than
        needing to be an exact match An open metadata type name may be supplied to restrict the types of elements
        returned. Async version.

        https://egeria-project.org/types/

        Parameters
        ----------
        element_guid: str
            - the base element to get related elements for
        relationship_type: str
            - the type of relationship to navigate to related elements
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        open_metadata_type_name : str, default = None
            - restrict search to elements of this open metadata type
        start_at_end: int, default = 1
            - The end of the relationship to start from - typically End1
            - open metadata type to be used to restrict the search
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """
        if server_name is None:
            server_name = self.server_name

        possible_query_params = query_string(
            [("startFrom", start_from), ("pageSize", page_size), ("forLineage", for_lineage),
                ("forDuplicateProcessing", for_duplicate_processing), ("startAtEnd", start_at_end)])

        body = {"class": "FindPropertyNamesProperties", "openMetadataTypeName": open_metadata_type_name,
            "propertyValue": property_value, "propertyNames": property_names, "effectiveTime": effective_time, }

        url = (f"{base_path(self, server_name)}/elements/{element_guid}/by-relationship/"
               f"{relationship_type}/with-property-value-search{possible_query_params}")

        response: Response = await self._async_make_request("POST", url, body_slimmer(body), time_out=time_out)

        elements = response.json().get('elements', 'No elements found')
        if type(elements) is list:
            if len(elements) == 0:
                return "No elements found"
        return elements

    def find_related_elements_with_property_value(self, element_guid: str, relationship_type: str, property_value: str,
            property_names: [str], open_metadata_type_name: str = None, start_at_end: int = 1,
            effective_time: str = None, for_lineage: bool = None, for_duplicate_processing: bool = None,
            start_from: int = 0, page_size: int = max_paging_size, server_name: str = None,
            time_out: int = default_time_out) -> list | str:
        """
        Retrieve elements linked via the requested relationship type name and with the requested a value found in one of
        the classification's properties specified.  The value must only be contained in the properties rather than
        needing to be an exact match An open metadata type name may be supplied to restrict the types of elements
        returned.

        https://egeria-project.org/types/

        Parameters
        ----------
        element_guid: str
            - the base element to get related elements for
        relationship_type: str
            - the type of relationship to navigate to related elements
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        open_metadata_type_name : str, default = None
            - open metadata type to be used to restrict the search
        start_at_end: int, default = 1
            - The end of the relationship to start from - typically End1
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_find_related_elements_with_property_value(element_guid, relationship_type, property_value,
                property_names, open_metadata_type_name, start_at_end, effective_time, for_lineage,
                for_duplicate_processing, start_from, page_size, server_name, time_out))
        return response

    #
    #   relationships

    async def _async_get_relationships(self, relationship_type: str, effective_time: str = None,
            for_lineage: bool = None, for_duplicate_processing: bool = None, start_from: int = 0,
            page_size: int = max_paging_size, server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve relationships of the requested relationship type name. Async version.

        Parameters
        ----------
        relationship_type: str
            - the type of relationship to navigate to related elements
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """
        if server_name is None:
            server_name = self.server_name

        possible_query_params = query_string(
            [("startFrom", start_from), ("pageSize", page_size), ("forLineage", for_lineage),
                ("forDuplicateProcessing", for_duplicate_processing)])

        body = {"class": "FindProperties", "effectiveTime": effective_time}

        url = (f"{base_path(self, server_name)}/relationships/{relationship_type}"
               f"{possible_query_params}")

        response: Response = await self._async_make_request("POST", url, body_slimmer(body), time_out=time_out)
        rels = response.json().get('relationships', 'No relationships found')

        if type(rels) is list:
            if len(rels) == 0:
                return "No elements found"
        return rels

    def get_relationships(self, relationship_type: str, effective_time: str = None, for_lineage: bool = None,
            for_duplicate_processing: bool = None, start_from: int = 0, page_size: int = max_paging_size,
            server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve relationships of the requested relationship type name.

        Parameters
        ----------
        relationship_type: str
            - the type of relationship to navigate to related elements
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_relationships(relationship_type, effective_time, for_lineage, for_duplicate_processing,
                start_from, page_size, server_name, time_out))
        return response

    async def _async_get_relationships_with_property_value(self, relationship_type: str, property_value: str,
            property_names: [str], effective_time: str = None, for_lineage: bool = None,
            for_duplicate_processing: bool = None, start_from: int = 0, page_size: int = max_paging_size,
            server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve relationships of the requested relationship type name and with the requested a value found in
        one of the relationship's properties specified.  The value must match exactly. Async version.

        https://egeria-project.org/types/

        Parameters
        ----------
        relationship_type: str
            - the type of relationship to navigate to related elements
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """
        if server_name is None:
            server_name = self.server_name

        possible_query_params = query_string(
            [("startFrom", start_from), ("pageSize", page_size), ("forLineage", for_lineage),
                ("forDuplicateProcessing", for_duplicate_processing)])

        body = {"class": "FindPropertyNamesProperties", "propertyValue": property_value,
            "propertyNames": property_names, "effectiveTime": effective_time, }

        url = (f"{base_path(self, server_name)}/relationships/{relationship_type}/"
               f"with-exact-property-value{possible_query_params}")

        response: Response = await self._async_make_request("POST", url, body_slimmer(body), time_out=time_out)
        rels = response.json().get('relationships', 'No elements found')
        if type(rels) is list:
            if len(rels) == 0:
                return "No elements found"
        return rels

    def get_relationships_with_property_value(self, relationship_type: str, property_value: str, property_names: [str],
            effective_time: str = None, for_lineage: bool = None, for_duplicate_processing: bool = None,
            start_from: int = 0, page_size: int = max_paging_size, server_name: str = None,
            time_out: int = default_time_out) -> list | str:
        """
        Retrieve relationships of the requested relationship type name and with the requested a value found in
        one of the relationship's properties specified.  The value must match exactly.

        Parameters
        ----------
        relationship_type: str
            - the type of relationship to navigate to related elements
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_get_relationships_with_property_value(relationship_type, property_value, property_names,
                effective_time, for_lineage, for_duplicate_processing, start_from, page_size, server_name, time_out))
        return response

    async def _async_find_relationships_with_property_value(self, relationship_type: str, property_value: str,
            property_names: [str], effective_time: str = None, for_lineage: bool = None,
            for_duplicate_processing: bool = None, start_from: int = 0, page_size: int = max_paging_size,
            server_name: str = None, time_out: int = default_time_out) -> list | str:
        """
        Retrieve relationships of the requested relationship type name and with the requested a value found in one of
        the relationship's properties specified.  The value must only be contained in the properties rather than
        needing to be an exact match. Async version.

        Parameters
        ----------
        relationship_type: str
            - the type of relationship to navigate to related elements
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """
        if server_name is None:
            server_name = self.server_name

        possible_query_params = query_string(
            [("startFrom", start_from), ("pageSize", page_size), ("forLineage", for_lineage),
                ("forDuplicateProcessing", for_duplicate_processing)])

        body = {"class": "FindPropertyNamesProperties", "propertyValue": property_value,
            "propertyNames": property_names, "effectiveTime": effective_time, }

        url = (f"{base_path(self, server_name)}/relationships/"
               f"{relationship_type}/with-property-value-search{possible_query_params}")

        response: Response = await self._async_make_request("POST", url, body_slimmer(body), time_out=time_out)

        rels = response.json().get('relationships', 'No elements found')
        if type(rels) is list:
            if len(rels) == 0:
                return "No elements found"
        return rels

    def find_relationships_with_property_value(self, relationship_type: str, property_value: str, property_names: [str],
            effective_time: str = None, for_lineage: bool = None, for_duplicate_processing: bool = None,
            start_from: int = 0, page_size: int = max_paging_size, server_name: str = None,
            time_out: int = default_time_out) -> list | str:
        """
        Retrieve relationships of the requested relationship type name and with the requested a value found in one of
        the relationship's properties specified.  The value must only be contained in the properties rather than
        needing to be an exact match..

        https://egeria-project.org/types/

        Parameters
        ----------
        relationship_type: str
            - the type of relationship to navigate to related elements
        property_value: str
            - property value to be searched.
        property_names: [str]
            - property names to search in.
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        start_from: int, default = 0
            - index of the list to start from (0 for start).
        page_size
            - maximum number of elements to return.
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_find_relationships_with_property_value(relationship_type, property_value, property_names,
                effective_time, for_lineage, for_duplicate_processing, start_from, page_size, server_name, time_out))
        return response

    #
    #  guid
    #

    async def _async_retrieve_instance_for_guid(self, guid: str, effective_time: str = None, for_lineage: bool = None,
            for_duplicate_processing: bool = None, server_name: str = None,
            time_out: int = default_time_out) -> list | str:
        """
         Retrieve the header for the instance identified by the supplied unique identifier.
         It may be an element (entity) or a relationship between elements. Async version.

        Parameters
        ----------
        guid: str
            - the identity of the instance to retrieve
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """
        if server_name is None:
            server_name = self.server_name

        possible_query_params = query_string(
            [("forLineage", for_lineage), ("forDuplicateProcessing", for_duplicate_processing)])

        body = {"class": "FindProperties", "effectiveTime": effective_time, }

        url = f"{base_path(self, server_name)}/guids/{guid}{possible_query_params}"
        response: Response = await self._async_make_request("POST", url, body_slimmer(body), time_out=time_out)
        element = response.json().get('element', 'No elements found')
        return element



    def retrieve_instance_for_guid(self, guid: str, effective_time: str = None, for_lineage: bool = None,
            for_duplicate_processing: bool = None, server_name: str = None,
            time_out: int = default_time_out) -> list | str:
        """
         Retrieve the header for the instance identified by the supplied unique identifier.
         It may be an element (entity) or a relationship between elements.

        Parameters
        ----------
        guid: str
            - the identity of the instance to retrieve
        effective_time: str, default = None
            - Time format is "YYYY-MM-DDTHH:MM:SS" (ISO 8601)
        for_lineage: bool, default is set by server
            - determines if elements classified as Memento should be returned - normally false
        for_duplicate_processing: bool, default is set by server
            - Normally false. Set true when the caller is part of a deduplication function
        server_name: str, default = None
            - name of the server instances for this request.
        time_out: int, default = default_time_out
            - http request timeout for this request

        Returns
        -------
        [dict] | str
            Returns a string if no elements found and a list of dict of elements with the results.

        Raises
        ------
        InvalidParameterException
            one of the parameters is null or invalid or
        PropertyServerException
            There is a problem adding the element properties to the metadata repository or
        UserNotAuthorizedException
            the requesting user is not authorized to issue this request.
        """

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self._async_retrieve_instance_for_guid(guid, effective_time, for_lineage, for_duplicate_processing,
                server_name, time_out))
        return response


