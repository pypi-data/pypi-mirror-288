class JobEndpoints:
    """
    Endpoints related to jobs in Jenkins.

    Attributes
    ----------
    JOB_INFO : str
        URL template to get detailed information about a specific job.
    JOB_CONFIG : str
        URL template to get the configuration of a specific job.
    CREATE_JOB : str
        URL template to create a new job.
    DELETE_JOB : str
        URL template to delete a specific job.
    DISABLE_JOB : str
        URL template to disable a specific job.
    ENABLE_JOB : str
        URL template to enable a specific job.
    BUILD_JOB : str
        URL template to trigger a build for a specific job.
    BUILD_WITH_PARAMETERS : str
        URL template to trigger a build with parameters for a specific job.
    JOBS_QUERY : str
        URL template to query jobs with a specific tree structure.
    JOBS_QUERY_TREE : str
        URL template to define the tree structure for querying jobs.
    ALL_BUILDS : str
        URL template to get information about all builds for a specific job.
    """
    JOB_INFO: str = '{folder_url}job/{short_name}/api/json?depth={depth}'
    JOB_CONFIG: str = '{folder_url}job/{short_name}/config.xml'
    CREATE_JOB: str = '{folder_url}createItem?name={name}'
    DELETE_JOB: str = '{folder_url}job/{short_name}/doDelete'
    DISABLE_JOB: str = '{folder_url}job/{short_name}/disable'
    ENABLE_JOB: str = '{folder_url}job/{short_name}/enable'
    BUILD_JOB: str = '{folder_url}job/{short_name}/build'
    BUILD_WITH_PARAMETERS: str = '{folder_url}job/{short_name}/buildWithParameters'
    JOBS_QUERY: str = '?tree={string_value}'
    JOBS_QUERY_TREE: str = 'jobs[url,color,name,{string_value}]'
    ALL_BUILDS: str = '{folder_url}job/{short_name}/api/json?tree=allBuilds[number,url]'