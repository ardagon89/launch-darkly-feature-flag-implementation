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

![image](https://user-images.githubusercontent.com/55037808/113381763-66b38680-9345-11eb-97d3-481c0ffa535b.png)

    This page presents a simple login page which the users can use to enter into their profile.

![image](https://user-images.githubusercontent.com/55037808/113381793-7f23a100-9345-11eb-8062-a5b6efd517db.png)

    (You can find randomly generated user ids and passwords using the randomuser api.
        https://randomuser.me/api/?seed=usageai&results=10&inc=name,email,login,dob)

![image](https://user-images.githubusercontent.com/55037808/113381710-4aafe500-9345-11eb-9cfb-0e0dcf2b566d.png)

    The initial version of the page calls the api whenever a user logs in.

    A new feature is added to this page to cache the api calls to speed up the response time.

![image](https://user-images.githubusercontent.com/55037808/113382510-3d93f580-9347-11eb-88ad-d800eb1e0c2f.png)

    This feature is turned on or off using the "cache" feature flag using the LaunchDarkly SDK.
    You can even do a progressive roll-out by migrating only a small percentage of users to the
    new version of the app and slowly increasing the percentage in case of a smooth roll-out.
    
![image](https://user-images.githubusercontent.com/55037808/113382352-e0983f80-9346-11eb-867b-9b6ec19fe883.png)

    You can go back to the login screen by clicking the Rerun button.

Admin:

    This page serves the dual purpose of controlling the fraction of users directed to the new version
    of the app and a chart which plots the page load response times of users using the old version of the
    app vs the caching feature version of the page.
    
![image](https://user-images.githubusercontent.com/55037808/113382161-7384aa00-9346-11eb-8c3d-36d1afc01c5e.png)


    The slider control was origianlly added to control the percentage of users visiting the old version of
    the login page as opposed to the percentage of users visiting the page with caching feature added.
    But it was later removed in favor of controlling the percentage of users visiting the old and
    the new versions of the login page directly from the LaunchDarkly UI.

![image](https://user-images.githubusercontent.com/55037808/113382196-8d25f180-9346-11eb-9b85-41ad9521400e.png)

    The line chart shows the page load duration of the login page for the version of the app which uses the
    caching feature vs the version which doesn't use the caching feature.
    As you can clearly see, using the caching feature has reduced the page load time from 5 seconds to < 1 second,
    which is an improvement of more than 80%.
    
    
## Implementation

The app uses the below images

```
ardagon/launchdarkly:1.0
                        Core image which contains the Streamlit framework for web application, 
                        LaunchDarkly Python server SDK for feature flag management,
                        Pymongo for database connectivity &
                        Pandas for rendering the chart
```

```
mongodb
        For storing the data, logs, features and other required parameters in a persistent data store.
```

```
mongo-express
            For providing an easy-to-use user interface for mongo database management
```


The solution includes the below files

```
Dockerfile
            Contains instruction on how to build the ardagon/launchdarkly:1.0 docker image
```

```
compose.yaml
            Docker compose file build up or tear down the entire streamlit stack including mongo, express and the network
```

```
requirements.txt
            Contains the dependencies of the app
```

```
admin.py
            Contains the code for the Admin page
```

```
app.py
            Contains the code for routing the users to admin and user views
```

```
features.py
            Python code for the features object, which represents the feature flags and their propoerties
```

```
logs.py
            Python code for the logs object, which represents the user login and app performance parameters
```

```
mongodb.py
            Contains the code for saving and retrieving data from mongo document database
```

```
multiapp.py
            Frameworks for running multiple Streamlit applications as a single app.
```

```
person_dashboard.py
            Contains the code for the user login and details pages
```

```
user.py
            A class used to represent a user, fetched from the randomuser API
```
