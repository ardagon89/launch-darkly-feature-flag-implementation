# Launch Darkly - Project

Using any language or framework along with the LaunchDarkly SDK, implement a feature flag.

## Getting started

Use Python 3.7+.

Install the dependencies in requirements.txt:

```
pip install -r requirements.txt
```

Run the Streamlit app:

```
streamlit run dashboard.py
```

Streamlit will tell you where to find your live app, likely at `localhost:8501`. You can open this address in your browser.

## Solution

Completed all four parts of the challenge.
Tested successfully.

Added mongodb backend to save the users on disk, so API call performed only once.
Cached the API call so successive calls are much faster.

execute "docker-compose -f compose.yaml up -d" to bring up the entire stack and access the app at "http://localhost:8501/" and see the db records at "http://localhost:8081/"

#NOTE: Replace "localhost" by VM IP (ex. "192.168.99.100") if using docker on a VM.
