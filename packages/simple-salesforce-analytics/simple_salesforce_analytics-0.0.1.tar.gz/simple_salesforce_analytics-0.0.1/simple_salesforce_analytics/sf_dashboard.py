"""A module for handling interactions with Salesforce dashboards
    @author: Ryan Dowling <rdowlin3@jh.edu>
"""
########################################################################################
# Gloabl variables & imports
########################################################################################
from simple_salesforce import Salesforce
import json
from copy import deepcopy

########################################################################################
# Class Definitions
########################################################################################
class SFDashboard:
    """Class to represent an instance of a Salesforce dashboard.
        Configured access data in dashboardMetaData as if it was an attribute"""
    #------------------------------------------------------------------------------------
    #Class Variables (Shared by all instances)
    _DASHBOARD_ID_IDENTIFIER = '01Z'
    _DASHBOARDS_API_URL = 'analytics/dashboards/'
    _sf = None
    #------------------------------------------------------------------------------------
    #Public
    #-------
    #Overall Dictionaries
    dashboardMetadata = {}
    #-------
    #------------------------------------------------------------------------------------

    def __init__(self, dashboard_id: str,sf:Salesforce=None):
        """Default constructor. Will create a dashboard based on a given dashboard ID."""
        # Check for a valid SF instance from simple-salesforce
        if not isinstance(sf, Salesforce):
            raise Exception("Require a valid Salesforce Object")
        # Check for a valid dashboard ID
        if dashboard_id[:3] != self._DASHBOARD_ID_IDENTIFIER:
            raise Exception("Invalid dashboard ID.")
        
        self._sf = sf
        self._dashboard_endpoint = self._DASHBOARDS_API_URL + dashboard_id
        try:
            dashboard_data = self._sf.restful(f"{self._dashboard_endpoint}/describe")
        except:
            raise
        self.dashboardMetadata         = dashboard_data

    def __getattr__(self, name):
        """Override this method so that we can access the values in the three main dictionaries"""
        if name in self.dashboardMetadata:
            return self.dashboardMetadata[name]
        elif name in self.__dict__:
            return self.__dict__[name]
        else:
            raise AttributeError(f"'SFDashboard' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        """Override this method so that we can access the attributes of the three main dictionaries"""
        if name in self.__dict__:
            self.__dict__[name] = value
        elif name in self.dashboardMetadata:
            self.dashboardMetadata[name] = value
        else:
            self.__dict__[name] = value

    def _request_data(self):
        """Converts dashboard information into json for API requests"""
        request_data = deepcopy(self.dashboardMetadata)
        # Special step because SF be annoying. Delete any ID attributes from filters or their options
        for filter in request_data['filters']:
            filter.pop('id')
            for option in filter['options']:
                option.pop('id')
        return json.dumps(request_data,
                )

    def _valid_request_data(self):
        """Validates basic information on dashboard before API requests"""
        if len(self.name if self.name else "-") > 80:
            print(f"Max length for a dashboard name is 80 characters. Current dashboard name is {len(self.name)} characters.")
            return False
        if len(self.description if self.description else "-") > 255:
            print(f"Max length for a dashboard description is 255 characters. Current dashboard description is {len(self.description)} characters.")
            return False
        return True

    def save_new_dashboard(self):
        """Sends the dashboard information to sf to save this as a new dashboard"""
        if not self._valid_request_data():
            return None
        try:
            return self._sf.restful(self._DASHBOARDS_API_URL, method='POST', data=self._request_data())
        except Exception as err:
            print(err)
    
    def save_dashboard(self):
        """Sends the dashboard information to sf to edit this dashboard"""
        if not self._valid_request_data():
            return None
        try:
            return self._sf.restful(self._dashboard_endpoint, method='PATCH', data=self._request_data())
        except Exception as err:
            print(err)
    
    def clone_dashboard(self):
        """Sends the dashboard information to sf to clone the existing dashboard with our changes."""
        if not self._valid_request_data():
            return None
        try:
            return self._sf.restful(f"{self._DASHBOARDS_API_URL}?cloneID={self.id}", method="POST", data=self._request_data())
        except Exception as err:
            print(err)

########################################################################################
# Function Definitions
########################################################################################
def create_dashboards_from_list(lst:list, sf:Salesforce):
    """creates a list of SFDashboard objects from a list of dashboard ids"""
    if type(lst) != list:
        raise Exception("Function only accepts arguments of type list")
    dashboard_list = []
    for index, id in enumerate(lst):
        try:
            dashboard_list.append(SFDashboard(id, sf))
        except Exception as err:
            print(f"{err} when processing dashboard {id} at index {index}.")
            continue
    return dashboard_list

def create_dashboards_from_folder(folderId:str, sf:Salesforce):
    """Creates a list of SFDashboard Objects based on dashboards in a provided folder id"""
    dashboard_query = f"SELECT Id FROM Dashboard WHERE FolderId = '{folderId}'"
    try:
        response = sf.query(dashboard_query)
    except Exception as err:
        print(f"{err}")
        return None
    if response is None:
        return None
    if response['totalSize'] == 0:
        return None
    return create_dashboards_from_list([c['Id'] for c in response['records']], sf)
    
# def create_dashboards_from_dashboard(dashboardId:str, sf:Salesforce):
#     """Creates a list of SFDashboard Objects based on dashboards in a provided dashboard id"""
#     dashsboard_api_url = f'analytics/dashboards/{dashboardId}/describe'
#     try:
#         response = sf.restful(dashsboard_api_url)
#     except Exception as err:
#         print(f"{err}")
#         return None
#     if response is None:
#         return None
#     if 'components' not in response:
#         return None
#     if response['components'] is None:
#         return None
#     return create_dashboards_from_list([c['dashboardId'] for c in response['components'] if c['type'] == 'dashboard'],sf)

def create_dashboards_from_query(queryStr:str, sf:Salesforce, dashboardIdField:str="Id"):
    """Creates a list of SFDashboard Objects based on a given query.
        Should specify the dashboard id field if necessary, uses Id as a default."""
    try:
        response = sf.query(queryStr)
    except Exception as err:
        print(f"{err}")
        return None
    if response is None:
        return None
    if response['totalSize'] == 0:
        return None
    return create_dashboards_from_list([c[dashboardIdField] for c in response['records']], sf)


########################################################################################
# Main function code
########################################################################################
if __name__ == '__main__':
    print("Module for working with SF dashboards")
    example_usage = """
    import sf_dashboard as sfd

    query = "SELECT Id, Name, CreatedDate FROM dashboard WHERE Folder.Name LIKE 'Whiting Class Of%'"
    dashboard_list = sfr.create_dashboards_from_query(query, sf)

    for r in dashboard_list:
        r.name = r.name.replace("Homewood","Whiting")
        r.save_dashboard()"""
    print(f"Example Usage:")
    print(example_usage)