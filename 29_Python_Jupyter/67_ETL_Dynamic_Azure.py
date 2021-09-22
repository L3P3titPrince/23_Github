class HyperParamters(object):
    """
    This class will be used to transmit hyperparameters between class.parameters
    Most of class can inherit this class and its hyperparameters

    ########################__Rules__##################################
    class file name = class + _ + number of sequence + function name
    class name = ClassType (Camel-Case)
    function name = function_name
    variable name = attribute_type_describe (Hungarian notation) # sometime I don't use attribute
    constant = UPPERCASE
    ###########################################################################


    ########################__Notation__############################################
    1. We might need split data into two place NJ and PA, but we also can try to merge two location into one,
    because they are not far away
    2. clean data, transform date format, join by date, Coeffience anaylsis
    3. Check kaggle format
    4. Check journals
    5. Traditional way is to find relationship between total running time with other weather features
    6. But we need to consider equipment service lift or depreciation will affect running time
    7. Sometimes, we don't use running time itself, we can use the statiscal version of this data
    For example, runing time - avg , variance of each running time data point
    8.
    #############################################################################

    1. change url
    2. change Authorization bearer token
    """

    def __init__(self, auth_bear_token):
        """
        Args:
        -------
        auth_bear_token: str
            authorization bearer token, this token will change by time, you need get it from dynamic portal
            developer.ci.ai.dynamics.com/api-details#api=CustomerInsights&operation=Get-entities-with-OData-path 
            If other 
        """
        self.TEST = 1

        # generate by time
        self.AUTH = auth_bear_token
        
        # API headers, key is not change, but bearer token seems change by time
        # other parameters will stay same, only Authorization will change by time
        # next step we need find the authorization mechnizsm
        self.HEADERS = {
        # Request headers
        'Cache-Control': 'no-cache',
        'Authorization': 'bearer' + ' ' + self.AUTH, 
        'Ocp-Apim-Subscription-Key': 'fa46ff92d1334d189634151dfc8aea44',
        }
        # test for 
        print(self.HEADERS)
        
        # InstanceID is Enviroment ID (Admin -> System -> About)
        self.INSTANCEID = 'c910b061-1008-4397-95f6-4e7b443b924a'
        
        # relative path for EntityData request
        self.RELATIVEPATH = 'RetailDemoData_RetailSystem_Contacts'
        
        # database connection seting
        self.SERVER = 'server-test-04.database.windows.net'
        self.DATABASE = 'db-sqlserver-test-04' 
        self.USERNAME = 'azureadmin' 
        self.PASSWORD = '00W@sabi00' 
        
        # you can change this root path in this class and import_data() function will search from this root dictionary
        self.ROOTPATH = 'D:\\OneDrive\\03_Academic\\23_Github\\20_Stevens\\66-MGT-809-A\\03_data'




# requests is valid in runbook
import requests
# we use pandas to compelete json sql-table convert
import pandas as pd
# we use pyodbc to control sql server
import pyodbc
# use command line input to detect parameters input situation
import sys
# get command line input parameters
import getopt

class CustomerInsightsAPI(HyperParamters):
    """
    
    This class will inheriate paramters in class HyperParamters()
    """
    def __init__(self, auth_bear_token):
        """
        Args:
        ------
        instance_id:string
            not required, but we remain this
            
            
        class_name.__init(self)
        super(class_name, self).__init__()
        https://docs.python.org/2/library/functions.html#super
        """
        # find father of class CustomerInsights, which is HyperParameters
        # and then inherient class from Hyperparameters and become class of CustomersInsighsAPI
        # super(CustomerInsightsAPI, self).__init__()
        super().__init__(auth_bear_token)
        # they are similar 
        # HyperParamters.__init__(self)
        

            
    def get_entity_data(self, instance_id = None):
        """
        This function only used to extract data from API GetEntityByDataQuery of Customer Insights (Dynamic 365)
        I want to reserve parameter space in here. If we want to call this function outside, we can insert some parameters
        
        
        Returns:
        -----
        """
        # Typically, this url is better, becuase we can insert parameters into url in a proper way
        # original url is 'https://api.ci.ai.dynamics.com/v1/instances/{instanceId}/data/{relativePath}[?forceSearch][&proxy]'
        # but we don't need optional parameters, so we delete them from full url
        url_original = 'https://api.ci.ai.dynamics.com/v1/instances/{instanceId}/data/{relativePath}'
        # it seems {} only part of python sting format, so we only use string.format(value1, value2,..) to replace it 
        url_parse = url_original.format(instanceId = self.INSTANCEID, relativePath = self.RELATIVEPATH)
        # it seems sometimes url with parameters not working, so we provide a fulfuiled url 
        url_full = 'https://api.ci.ai.dynamics.com/v1/instances/c910b061-1008-4397-95f6-4e7b443b924a/data/RetailDemoData_RetailSystem_Contacts'
        
        # send get request with 
        response = requests.get(url_parse, headers=self.HEADERS)
        # r2 = requests.get(url_full, headers=self.HEADERS)
        print(response)
        # for record in r3.json():
        #     print(json.dumps(record))
        # according to json file structore, our data contain in ['value']
        # response.json()['value']
        # for row in r3.json()['value']:
        #     print(json.dumps(row))
        # we can try to storage data into a local directory,
        # these only work for local python script, not on AZURE  runbook
        # with open('03_data/32_entity.json', 'w') as outfile:
        #    json.dump(r3.json()['value'], outfile)

        return response.json()['value']

    
    def load_to_sql(self, json_data):
        """
        Loading data into Azure SQL Server
        
        Args:
        -----
        json_data:json
            response from api and already extrat the pure data part
            
        Returns:
        -------
        df
        """
        # convert json data type to dataframe type, more like row/column table format
        df = pd.json_normalize(json_data)
        print(df.head(2))
        # build connection 
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+ \
                              self.SERVER +';DATABASE='+ \
                              self.DATABASE +';UID='+ \
                              self.USERNAME +';PWD='+ \
                              self.PASSWORD)
        cursor = conn.cursor()
        # add a test 
        #cursor.execute("SELECT TOP 1 pc.Name FROM SalesLT.ProductCategory pc")
        cursor.execute("CREATE TABLE Table_test_02(\
                        [Name] varchar(50) ,\
                        [Address] varchar(50),\
                        [City] varchar(50),\
                        [State] VARCHAR(50),\
                        [PostalCode] INT,\
                        [Country] VARCHAR(50),\
                        [PreferredStore] VARCHAR(50),\
                        [RewardPoints] INT,\
                        [CustomerRetailID] VARCHAR(50),\
                        [DOB] datetime,\
                        [Gender] VARCHAR(10)\
                        )")
        cursor.commit()
        cursor.close()
        
        cursor = conn.cursor()
        # Insert Dataframe into SQL Server:
        for index, row in df.iterrows():
            cursor.execute("INSERT INTO Table_test_02 (Name, Address, City, State,\
                            PostalCode, Country, PreferredStore, RewardPoints,\
                            CustomerRetailID, DOB, Gender) values(?,?,?,?,?,?,?,?,?,?,?)", 
                           row.Name, row.Address, row.City, row.State,
                           row.PostalCode, row.Country, row.PreferredStore, row.RewardsPoints,
                           row.CustomerRetailID, row.DOB, row.Gender)
        conn.commit()
        cursor.close()
        # conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}')
        
        return None
        
        
    def get_automation_runas_credential(runas_connection):
        """ 
         Tutorial to show how to authenticate against Azure resource manager resources
    
        Returns credentials to authenticate against Azure resoruce manager 
        """
        from OpenSSL import crypto
        from msrestazure import azure_active_directory
        import adal
        # for authorization


        # Get the Azure Automation RunAs service principal certificate
        cert = automationassets.get_automation_certificate("AzureRunAsCertificate")
        pks12_cert = crypto.load_pkcs12(cert)
        pem_pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, pks12_cert.get_privatekey())

        # Get run as connection information for the Azure Automation service principal
        application_id = runas_connection["ApplicationId"]
        thumbprint = runas_connection["CertificateThumbprint"]
        tenant_id = runas_connection["TenantId"]

        # Authenticate with service principal certificate
        resource = "https://management.core.windows.net/"
        authority_url = ("https://login.microsoftonline.com/" + tenant_id)
        context = adal.AuthenticationContext(authority_url)
        return azure_active_directory.AdalAuthentication(
            lambda: context.acquire_token_with_client_certificate(
                resource,
                application_id,
                pem_pkey,
                thumbprint)
        )

    def auth(self):
        """
        """
        import azure.mgmt.resource
        import automationassets
        # Authenticate to Azure using the Azure Automation RunAs service principal
        runas_connection = automationassets.get_automation_connection("AzureRunAsConnection")
        azure_credential = get_automation_runas_credential(runas_connection)
        print(azure_credential)

        # Intialize the resource management client with the RunAs credential and subscription
        resource_client = azure.mgmt.resource.ResourceManagementClient(
            azure_credential,
            str(runas_connection["SubscriptionId"]))

        # Get list of resource groups and print them out
        groups = resource_client.resource_groups.list()
        for group in groups:
            print(group.name)
            

def main():
    """
    """

    
    # if my full python script *.py name is "ETL_dynamic_Azure" then we have 1 element on len(sys.argv)
    # sys.argv will take count how many seperate elements in your command line
    # for example, if my script is "> python ELT_dynamic_Azure.py" then len(sys.argv) will output 1
    # if my script is "> python ELT_dynamic_Azure.py 1 2 3" then len(sys.argv) will output 4 even "1 2 3" are not defined parameters
    # its more like sys.argv record parameters and split by space into a list ['ELT_dynamic_Azure.py', '1', '2', '3']
    # so we got 4 parameters, add its dash part and file name part itself, we need at least 9 elements length
    #  if len(sys.argv) < 9:
    # raise Exception("Requires Subscription id -s, \
    #                 Automation resource group name -g, \
    #                 account name -a, and module name -g as arguments. \
    #                 Example: -s xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx -g contosogroup -a contosoaccount -m pytz ")
    if len(sys.argv) < 3:
        raise Exception("Requires bear token -b. Example: ETL_dynamic_Azure.py -b xxxxxxxxxxxxxxxxxx")
    
    # Process any arguments sent in
    bear_token = None
    # placeholder, not use at all
    test_param = None
    # read parameters from command line
    # opts, args = getopt.getopt(sys.argv[1:], "s:g:a:m:")
    opts, args = getopt.getopt(sys.argv[1:], "b:t:")
    for opt, string in opts:
        if opt == '-b':  
            bear_token = string
        elif opt == '-t':  
            test_param = string
#         elif o == '-a': 
#             automation_account = i
#         elif o == '-m': 
#             module_name = i
    
    class_ci = CustomerInsightsAPI(auth_bear_token = bear_token)
    response_json_data = class_ci.get_entity_data()
    class_ci.load_to_sql(response_json_data)
    
    
    
    return response_json_data
    
if __name__=="__main__":
    """
    """
    response_json_data = main()