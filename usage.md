# Logstore configuration instructions

## Conductor
Starting the conductor is simple: execute `twistd logstore-conductor` (on windows it may have to be `twistd.py`). This
assumes you are running RabbitMQ on port 5672 and the web interface can be reached at port 8000. Run
 `twistd logstore-conductor help` to see how to change them.

Twisted also exposes a lot of other configuration options that can be used to configure the services environment, such
as the user account to run under and the logging settings, run
`twistd --help` for more information.

## Web
Configure the initial settings by executing `logstore init`. This will create a `.logstore` directory inside your home
directory, and create a `web_settings.py` file. No configuration is needed to get started with Logstore.

Before you run the web interface the database schema needs to be set up. This is handled automatically for you by
executing the following command: `logstore syncdb`. You will be asked to enter a username and password for the first
administrator account, ensure you create one and remember the credentials as you will need them to log in.

If you are experimenting with Logstore then you can load some initial data like formats, alerts and events by executing
`logstore loaddata`.

Once the database has been configured the web application can be started. If you are simply experimenting with Logstore
then Logstore can be run with a basic built in webserver. To start this run `logstore runserver --noreload` from the
command line, by default it serves on port 8000 so visit [http://localhost:8000/](). This can be customized, run
`logstore runserver --help` to view more options.

If you are running this in production then the built in webserver will not perform well enough. On Linux the preferred
setup is to have a Nginx frontend webserver that proxies requests to several backend Gunicorn processes. Setting that
up is outside of the scope of this document, but logstore can be started with gunicorn using the `logstore run_gunicorn`
command.

### Download the GeoIP database
By default logstore comes with an extension to geolocate IP addresses. You need to download the GeoIP database by
running `logstore runtask download_geoip`.

### Running the analyser
The analyser can be started by executing `logstore analyser`. This will begin to pull messages from the queue and
index them according to your formats. **Note:** As of yet any changes made to formats after the analyser has been started
are not seen by the analyser. This will be fixed in the future, but please restart the analyser after any changes.

### Triggering alerts
Alerts are checked every minute by a separate daemon which can be started by `logstore alert_server`. Execute this in
the background.


## Importing data
Data can be imported using the `jotter` command or via Syslog. To get started quickly the jotter package comes with a
`logstore_fake_data` command that can be used to generate fake Nginx log or ping log data. Ensure that the conductor,
web interface and analyser are running and then and import some data by executing
`logstore_fake_data nginx 10000 | jotter -n access_log`.

You can import data without defining a format, but searches will be limited to fulltext ones only. Logstore comes with
some example formats, events and alerts that you can add by running `logstore loaddata example.json` (`example.json`
can be found in the root project directory). **Before you execute the loaddata command ensure that both the conductor
and the Elasticsearch server are running.**