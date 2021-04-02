"""Features module for the Streamlit LaunchDarkly app"""

from mongodb import Db

def upsert_feature(flag, value):
    """Save a feature in the db.
    
    Parameters: 
        - flag: string
            Name of the feature
        - value: string
            Value of the feature
            
    Raises:
        SystemExit: If the database call fails.
    """

    db = Db()
    db.upsert_feature(flag, value)

def get_feature(flag):
    """Get a feature value from the db.
    
    Parameters: 
        - flag: string
            Name of the feature
            
    Returns:
        The first result in the list of None
        
    Raises:
        SystemExit: If the database call fails.
    """

    db = Db()
    result = db.get_feature(flag)
    if result.count() != 0:
        return result[0]
    return None