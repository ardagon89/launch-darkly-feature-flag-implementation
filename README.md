# Launch Darkly - Project

Using any language or framework along with the LaunchDarkly SDK, implement a feature flag.

## Getting started - Option 1

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

## Getting started - Option 2 (recommended)

Use `ardagon/launchdarkly:1.0` docker image.

Execute the below command to bring up the entire stack:

```
docker-compose -f compose.yaml up -d
```

Access the Streamlit app at:

```
http://localhost:8501/
```

See the db records at:

```
http://localhost:8081/
```

NOTE:

```
Replace "localhost" by VM IP (ex. "192.168.99.100") if using docker on a VM.
```

## Solution

Created a simple web application using streamlit api with separate User and Admin views.

User:

![image](https://user-images.githubusercontent.com/55037808/113381565-e8ef7b00-9344-11eb-8182-a9770e39ebc8.png)


    This page presents a simple login page which the users can use to enter into their profile.

        
![image](https://user-images.githubusercontent.com/55037808/113381710-4aafe500-9345-11eb-9cfb-0e0dcf2b566d.png)

![image](https://user-images.githubusercontent.com/55037808/113381793-7f23a100-9345-11eb-8062-a5b6efd517db.png)

    (You can find randomly generated user ids and passwords using the randomuser api.
        https://randomuser.me/api/?seed=usageai&results=10&inc=name,email,login,dob)
        
![image](https://user-images.githubusercontent.com/55037808/113381763-66b38680-9345-11eb-97d3-481c0ffa535b.png)

    The initial version of the page calls the api whenever a user logs in.

    A new feature is added to this page to cache the api calls to speed up the response time.

    This feature is turned on or off using the "cache" feature flag using the LaunchDarkly SDK.
    You can even do a progressive roll-out by migrating only a small percentage of users to the
    new version of the app and slowly increasing the percentage in case of a smooth roll-out.

Admin:

    This page serves the dual purpose of controlling the fraction of users directed to the new version
    of the app and a chart which plots the page load response times of users using the old version of the
    app vs the caching feature version of the page.

    The slider control was origianlly added to control the percentage of users visiting the old version of
    the login page as opposed to the percentage of users visiting the page with caching feature added.
    But it was later removed in favor of controlling the percentage of users visiting the old and
    the new versions of the login page directly from the LaunchDarkly UI.

    The line chart shows the page load duration of the login page for the version of the app which uses the
    caching feature vs the version which doesn't use the caching feature.
    As you can clearly see, using the caching feature has reduced the page load time from 5 seconds to < 1 second,
    which is an improvement of more than 80%.
