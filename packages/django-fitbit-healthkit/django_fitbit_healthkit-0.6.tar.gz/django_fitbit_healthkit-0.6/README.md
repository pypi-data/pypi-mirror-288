# django-fitbit-healthkit

django-fitbit-healthkit is a Django Fitbit App with HealthKit-friendly API.
The goal is to provide a wrapper over fitbit authentication, token management, and web APIs
that is similar to other high-level healthkit wrappers like [react-native-healthkit](https://github.com/kingstinct/react-native-healthkit).
The HealthKit API from Apple is [here](https://developer.apple.com/documentation/healthkit/queries) for reference.

A sample app is included in the `sample` directory to showcase how to use the fitbit app.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "fitbit" to your INSTALLED_APPS setting like this:

```
INSTALLED_APPS = [
    ...,
    "django_fitbit_healthkit",
]
```

2. Include the fitbit URLconf in your project urls.py like this:

```
path("fitbit/", include("django_fitbit_healthkit.urls")),
```

3. Run ``python manage.py migrate`` to create the models.

4. Visit the ``/fitbit/login`` URL to sign in with Fitbit.


Running the sample app
----------------------

Make sure to set environment variables for 

```sh
FITBIT_CLIENT_ID=xxx
FITBIT_CLIENT_SECRET=xxx
```

which will be picked up by `sample/settings.py`.
In your fitbit app settings, add `http://localhost:8000/fitbit/success` to the allowed callback URLs.

Set up dev environment.
There is nothing complicated here,
so vanilla venv on any platform is probably sufficient
(no nix/devbox, dev container type setup is necessary).

```
python3 -m venv venv
source venv/bin/activate
pip3 install Django
```

Apply DB migrations with `python3 manage.py migrate`.
You can run the app quite simply:

```
python3 manage.py runserver
```

This will allow you to register an account,
sign in with fitbit,
and view some of your data.

Release workflow
----------------

Develop on a branch.
When it's ready,
merge to main.

If this is not a release (no bumped version in `setup.cfg`),
then TestPyPI _may_ fail
with a duplicate sdist upload (it has before).

If it's a new version, then the `setup.cfg`
should have been bumped **on the branch**.
When it's merged,
we expect TestPyPI to succeed.
Then the tag can be pushed to GH,
which will trigger real PyPI release.
