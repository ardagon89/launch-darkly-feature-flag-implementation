import streamlit as st
from features import upsert_feature, get_feature
import pandas as pd
from logs import get_logs

def app():
    """Displays a user details if login is successful
        
    Raises:
        SystemExit: If the call to users_exist, load_random_users, save_users or get_user methods fails.
    """
    
    st.title('Admin')

    feature = get_feature("cache")
    default_value = feature["value"] if feature else 0.0
    fraction = st.slider('Set fraction of users testing the cache feature', 0.0, 1.0, default_value, 0.1)
    upsert_feature("cache", fraction)

    st.write("Fraction of users testing the cache feature currently:`"+str(get_feature("cache")["value"])+"`")
    st.write("\n")

    result = get_logs("cache")
    without_caching_result = [hash["exec_time"] for hash in result if not hash["value"]]
    with_caching_result = [hash["exec_time"] for hash in result if hash["value"]] + [None]

    if len(without_caching_result) > len(with_caching_result):
        with_caching_result.extend([None]*(len(without_caching_result)-len(with_caching_result)))
    else:
        without_caching_result.extend([None]*(len(with_caching_result)-len(without_caching_result)))

    data  = list(zip(without_caching_result, with_caching_result))

    chart_data = pd.DataFrame(data, columns=['without caching', 'with caching'])

    st.markdown("### Line chart: Page load duration with & without caching")
    st.line_chart(chart_data)
    st.write("Y-axis: Page load duration (in seconds)")
    st.write("X-axis: Request id (in decimal)")