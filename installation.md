# Logstore installation instructions

## Getting Started
Before you install the logstore system itself a few dependencies need to be installed.

**Note:** If you are using Windows it is recommended that you install [Chocolatey](https://chocolatey.org/), which
is a Windows command line package manager and can be used to install certain dependencies automatically. You can install
this from the Chocolatey website: [https://chocolatey.org/](). This provides a `cinst` command that is used in
this document and greatly simplifies installing dependencies on Windows.

### Dependencies:

#### Python
Logstore is written in Python and needs a Python 2.7 intepreter available. As of writing the latest release is 2.7.6,
but any 2.7 version will suffice.

  * **Windows**
    * Run `cinst python -Version 2.7.6` or download [https://www.python.org/ftp/python/2.7.6/python-2.7.6.msi]() and install
    * If not installed with Chocolatey then add the following locations to your systems PATH:
        * C:\python27\
        * C:\python27\scripts
    * Download this file: [https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py]()
    * Execute the file with Python: `python get-pip.py`
        * If the Python executable cannot be found ensure the locations above are in the PATH environment variable and
          restart any command windows.
    * You should now have a `pip` command available: execute `pip --version` to ensure it has been installed correctly.

  * **Unix**
    * Python should already be installed on your system.
    * Install pip by executing the following command:
        `wget https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py && python get-pip.py`

**Note:** If you use Python for other projects you may wish to create a virtual Python environment to isolate the logstore
packages and their dependencies. This is optional if you have just installed Python for the first time on your machine and
are only using it for logstore. Instructions on how to create a virtual Python environment can be found here:
[https://virtualenv.pypa.io/en/latest/virtualenv.html]()


#### Elasticsearch
Logstore works with Elasticsearch 1.1.1, you can install this like so:

  * **Windows**
    * Install the Java Runtime using `cinst javaruntime` or via their website [https://www.java.com/en/download/]()
    * Download this file and unzip: [https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.1.1.zip]()
    * Open the unzipped directory and run `bin\elasticsearch` via the command line. You now have an ElasticSearch
      server running on your machine

  * **Unix**
    * ElasticSearch can be installed via `apt` or `yum`. Visit [http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/setup-repositories.html]()
      for a detailed list of instructions

#### RabbitMQ

  * **Windows**
    * Run `cinst rabbitmq` or visit [https://www.rabbitmq.com/install-windows.html]() for manual installation instructions

  * **Unix**
    * Debian/Ubuntu: [https://www.rabbitmq.com/install-debian.html]()
    * RPM (Centos, Fedora ...): [https://www.rabbitmq.com/install-rpm.html]()

#### PostgreSQL
A PostgreSQL database is an optional dependency and is only needed if you are installing the system in a production environment.
If you are merely installing the system to experiment then the built-in SQlite database will suffice and this stage is not required.

**Note:** Only PostgreSQL 9.3 has been tested, it should work with earlier versions but 9.3 is recommended.

   * **Windows**
     * Run `cinst postgreSQL` or visit [http://www.postgresql.org/download/windows/]() for other download links

   * **Linux**
     * Ubuntu: `apt-get install postgresql-9.3 libpq-dev` (and install the `pgadmin3` package if you want a graphical
                interface to manage the system)
     * Yum: See [http://www.postgresql.org/download/linux/redhat/]()


#### PyWin32
While Python strives to be platform independent some packages distribute platform-dependent binary modules. One module
that is required only when running Windows and the Jotter command is the Pywin32 module which can be downloaded here:

  * 32bit Python: [http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win32-py2.7.exe/download]()
  * 64bit Python: [http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win-amd64-py2.7.exe/download]()

This is the only extension that cannot be installed automatically and only applies to Windows.


### Installing logstore
Once you have installed the above dependencies we can install the actual logstore system. This can be achieved by using
the provided `install_everything.bat` script, which simply installs the pre-packaged libraries found within the dist directory.

If you are not on a Windows system simply execute the following command inside the `dist/` directory:

```pip install * --find-links=. --upgrade```

You should now have the complete system and all components installed on your machine. Proceed to the configuration document
to get started with Logstore.