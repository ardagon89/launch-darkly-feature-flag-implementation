"""Main module for the Streamlit Launch Darkly app"""


import requests
import streamlit as st
import dateutil.parser
from user import User
from features import get_feature
from logs import insert_log
import random
import time
import ldclient
from ldclient.config import Config

# Base URL for the randomuser api to fetch only the required details
RANDOM_API_URL = 'https://randomuser.me/api/?seed=usageai&results=10&inc=name,email,login,dob'

fraction = None

def load_random_users():
    """Loads random users available from the Random User Generator API
    
    Returns:
        A list of users. Each user is a dictionary of required fields.
        
    Raises:
        SystemExit: If the
            request to the Nager.Date API fails.
    """
    
    data_load_state = st.text('Loading user data...')
    
    try:
        response = requests.get(RANDOM_API_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    data_load_state.text('Encrypting sensitive fields...')
    
    # Get random user data from API
    users = response.json()
    user_list = users['results']
    
    hashed_user_list = []
    
    # Create a list of User objects with hashed password
    for user_data in user_list:
        hashed_user_list.append(User(user_data))
        
    data_load_state.empty()
    
    return hashed_user_list

@st.cache(suppress_st_warning=True, show_spinner=False)
def load_random_users_cached():
    return load_random_users()

def load_user(email, password, hashed_user_list):
    """Loads random users available from the Random User Generator API
    
    Returns:
        A list of users. Each user is a dictionary of required fields.
        
    Raises:
        SystemExit: If the
            request to the Nager.Date API fails.
    """
    
    for user in hashed_user_list:
        if user.email == email and user.verify_password(password):
            return user
    
    return None

def get_user_dict(user_list):
    """Loads random users available from the Random User Generator API
    
    Parameters: 
        - user_list: list
            List of User objects
    
    Returns:
        A dictionary of all User objects with email id as the key
    """
    
    user_dict = {}
    for user in user_list:
        user_dict[user.email] = user
        
    return user_dict


def generate_login_block():
    """ Create two empty blocks to hold the email id and password textboxes
    
    Returns:
        A list of the two created blocks
    """
    
    blocks = [st.empty(), st.empty()]
    
    return blocks


def clean_blocks(blocks):
    """ Empty the list of blocks of all content
    
    Parameters: 
        - blocks: list
            List of blocks
    """
    
    for block in blocks:
        block.empty()


def login(blocks):
    """ Get the email id and password
    
    Parameters: 
        - blocks: list
            List of blocks
            
    Returns:
        The email id and password entered by the user
    """
    
    return blocks[0].text_input('Email'), blocks[1].text_input('Password', type="password")


def app():
    """Displays a user details if login is successful
        
    Raises:
        SystemExit: If the call to users_exist, load_random_users, save_users or get_user methods fails.
    """
    start_time = time.time()

    # Generate blocks to hold input boxes
    login_blocks = generate_login_block()

    # Get the email id and password entered by the user
    provided_email, provided_password = login(login_blocks)
    
    try:
        # If email is not empty
        if provided_email:
            # If password is not empty
                if provided_password:

                    feature = get_feature("cache")
                    probability_value = feature["value"] if feature else 0.0

                    # Configure and get a Launch Darkly client
                    ldclient.set_config(Config("sdk-dee7c530-f824-4d8c-b2a9-2bb3a883e567"))
                    ld_client = ldclient.get()

                    # feature_flag = True if random.random() < probability_value else False
                    feature_flag = ld_client.variation("cache-the-api-call", {"key": provided_email}, False)

                    if feature_flag:
                        user_list = load_random_users_cached()
                    else:
                        user_list = load_random_users()

                    # Load and authenticate the user from the API
                    user = load_user(provided_email, provided_password, user_list)
                    
                    # If a user exists with the given email and password
                    if user:
                        clean_blocks(login_blocks)
                        st.markdown('**Firstname** : '+ user.first_name)
                        st.markdown('**Lastname** : '+ user.last_name)
                        dob = dateutil.parser.parse(user.dob)
                        st.markdown('**DOB** : '+ dob.strftime('%m/%d/%Y'))
                        
                    # Else password in not valid
                    else:
                        st.info("Email id and password do not match!")

                    exec_time = time.time() - start_time
                    insert_log("cache", feature_flag, time.time(), exec_time)

                    # shut down the client, since we're about to quit
                    ld_client.close()
                
    # In case the api service is not available
    except SystemExit:
        st.error("Service Temporarily Unavailable for LaunchDarkly API! Please refresh the page.")
        ld_client.close()