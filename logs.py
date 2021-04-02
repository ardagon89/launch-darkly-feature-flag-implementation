"""Log module for the Streamlit LaunchDarkly app"""

from mongodb import Db

def insert_log(flag, value, time, exec_time):
    """Save log parameters in the db.
    
    Parameters: 
        - flag: string
            Name of the feature
        - value: string
            Value of the feature
        - time: time
            Time of page load
        - exec_time: duration
            Page load duration
            
    Raises:
        SystemExit: If the database call fails.
    """

    db = Db()
    db.insert_log(flag, value, time, exec_time)

def get_logs(flag):
    """Get a feature logs from the db.
    
    Parameters: 
        - flag: string
            Name of the feature

    Returns:
        The result in the list or None
        
    Raises:
        SystemExit: If the database call fails.
    """

    db = Db()
    result = db.get_logs(flag)
    return list(result)