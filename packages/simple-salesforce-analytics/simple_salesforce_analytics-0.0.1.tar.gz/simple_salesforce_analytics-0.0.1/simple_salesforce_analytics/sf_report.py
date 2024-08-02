"""A module for handling interactions with Salesforce Reports
    @author: Ryan Dowling <rdowlin3@jh.edu>
"""
########################################################################################
# Gloabl variables & imports
########################################################################################
from simple_salesforce import Salesforce
import json

########################################################################################
# Class Definitions
########################################################################################
class SFReport:
    """Class to represent an instance of a Salesforce Report.
        Configured access data in reportMetaData, reportExtendedMetadata, and reportTypeMetadata as if it was an attribute"""
    #------------------------------------------------------------------------------------
    #Class Variables (Shared by all instances)
    _REPORT_ID_IDENTIFIER = '00O'
    _REPORTS_API_URL = 'analytics/reports/'
    _sf = None
    #------------------------------------------------------------------------------------
    #Public
    #-------
    #Overall Dictionaries
    reportMetadata = {}
    reportExtendedMetadata = {}
    reportTypeMetadata = {}
    #-------
    #------------------------------------------------------------------------------------

    def __init__(self, report_id: str,sf:Salesforce=None):
        """Default constructor. Will create a Report based on a given Report ID."""
        # Check for a valid SF instance from simple-salesforce
        if not isinstance(sf, Salesforce):
            raise Exception("Require a valid Salesforce Object")
        # Check for a valid report ID
        if report_id[:3] != self._REPORT_ID_IDENTIFIER:
            raise Exception("Invalid Report ID.")
        
        self._sf = sf
        self._report_endpoint = self._REPORTS_API_URL + report_id
        try:
            report_data = self._sf.restful(f"{self._report_endpoint}/describe")
        except:
            raise
        self.reportMetadata         = report_data['reportMetadata']
        self.reportExtendedMetadata = report_data['reportExtendedMetadata']
        self.reportTypeMetadata     = report_data['reportTypeMetadata']

    def __getattr__(self, name):
        """Override this method so that we can access the values in the three main dictionaries"""
        if name in self.reportMetadata:
            return self.reportMetadata[name]
        elif name in self.reportExtendedMetadata:
            return self.reportExtendedMetadata[name]
        elif name in self.reportTypeMetadata:
            return self.reportTypeMetadata[name]
        elif name in self.__dict__:
            return self.__dict__[name]
        else:
            raise AttributeError(f"'SFReport' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        """Override this method so that we can access the attributes of the three main dictionaries"""
        if name in self.__dict__:
            self.__dict__[name] = value
        elif name in self.reportMetadata:
            self.reportMetadata[name] = value
        elif name in self.reportExtendedMetadata:
            self.reportExtendedMetadata[name] = value
        elif name in self.reportTypeMetadata:
            self.reportTypeMetadata[name] = value
        else:
            self.__dict__[name] = value

    def _request_data(self):
        """Converts report information into json for API requests"""
        return json.dumps({'reportMetadata':self.reportMetadata,
                'reportExtendedMetadata':self.reportExtendedMetadata,
                'reportTypeMetadata':self.reportTypeMetadata,
                })

    def _valid_request_data(self):
        """Validates basic information on Report before API requests"""
        if len(self.name if self.name else "-") > 40:
            print(f"Max length for a report name is 40 characters. Current report name is {len(self.name)} characters.")
            return False
        if len(self.description if self.description else "-") > 255:
            print(f"Max length for a report description is 255 characters. Current report description is {len(self.description)} characters.")
            return False
        return True

    def save_new_report(self):
        """Sends the report information to sf to save this as a new report"""
        if not self._valid_request_data():
            return None
        try:
            return self._sf.restful(self._REPORTS_API_URL, method='POST', data=self._request_data())
        except Exception as err:
            print(err)
    
    def save_report(self):
        """Sends the report information to sf to edit this report"""
        if not self._valid_request_data():
            return None
        try:
            return self._sf.restful(self._report_endpoint, method='PATCH', data=self._request_data())
        except Exception as err:
            print(err)
    
    def run_report(self):
        """Synchronously executes a report. Typically used when we need to access data in the report"""
        try:
            return self._sf.restful(self._report_endpoint)
        except Exception as err:
            print(err)

#TODO: Create function for exporting a given report to Excel via API.
# try:
#     response_data = sf._call_salesforce("GET",
#                                         sf.base_url  + f"analytics/reports/00OPM000000ZnnR2AS",
#                                         name=f"analytics/reports/00OPM000000ZnnR2AS",
#                                         params = None,
#                                         headers={'Accept':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',},
#                                         stream=True)
# except Exception as err:
#     tb.print_tb(err)

# with open(r"C:\Users\rdowlin3\Downloads\test.xlsx", 'wb') as fd:
#     for chunk in response_data.iter_content(chunk_size=128):
#         fd.write(chunk)
# *****************************************************8
# The sample code above uses _call_salesforce because restful attempts to convert all responses to JSON. 
# The file snippet is based on the requests documentation: https://requests.readthedocs.io/en/latest/user/quickstart/#raw-response-content
# Headers are based on the SF API documentation: https://developer.salesforce.com/docs/atlas.en-us.api_analytics.meta/api_analytics/sforce_analytics_rest_api_download_excel.htm

########################################################################################
# Function Definitions
########################################################################################
def create_reports_from_list(lst:list, sf:Salesforce):
    """creates a list of SFReport objects from a list of report ids"""
    if type(lst) != list:
        raise Exception("Function only accepts arguments of type list")
    report_list = []
    for index, id in enumerate(lst):
        try:
            report_list.append(SFReport(id, sf))
        except Exception as err:
            print(f"{err} when processing report {id} at index {index}.")
            continue
    return report_list

def create_reports_from_folder(folderId:str, sf:Salesforce):
    """Creates a list of SFReport Objects based on reports in a provided folder id"""
    report_query = f"SELECT Id FROM Report WHERE OwnerId = '{folderId}'"
    try:
        response = sf.query(report_query)
    except Exception as err:
        print(f"{err}")
        return None
    if response is None:
        return None
    if response['totalSize'] == 0:
        return None
    return create_reports_from_list([c['Id'] for c in response['records']], sf)
    
def create_reports_from_dashboard(dashboardId:str, sf:Salesforce):
    """Creates a list of SFReport Objects based on reports in a provided dashboard id"""
    dashsboard_api_url = f'analytics/dashboards/{dashboardId}/describe'
    try:
        response = sf.restful(dashsboard_api_url)
    except Exception as err:
        print(f"{err}")
        return None
    if response is None:
        return None
    if 'components' not in response:
        return None
    if response['components'] is None:
        return None
    return create_reports_from_list([c['reportId'] for c in response['components'] if c['type'] == 'Report'],sf)

def create_reports_from_query(queryStr:str, sf:Salesforce, reportIdField:str="Id"):
    """Creates a list of SFReport Objects based on a given query.
        Should specify the report id field if necessary, uses Id as a default."""
    try:
        response = sf.query(queryStr)
    except Exception as err:
        print(f"{err}")
        return None
    if response is None:
        return None
    if response['totalSize'] == 0:
        return None
    return create_reports_from_list([c[reportIdField] for c in response['records']], sf)


########################################################################################
# Main function code
########################################################################################
if __name__ == '__main__':
    print("Module for working with SF Reports")
    example_usage = """
    import sf_report as sfr

    query = "SELECT Id, Name, CreatedDate FROM Report WHERE Owner.Name LIKE 'Whiting Class Of%'"
    report_list = sfr.create_reports_from_query(query, sf)

    for r in report_list:
        r.name = r.name.replace("Homewood","Whiting")
        r.save_report()"""
    print(f"Example Usage:")
    print(example_usage)