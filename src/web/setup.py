from setuptools import find_packages, setup


setup(name="logstore.web",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.web': 'src'},
      namespace_packages =["logstore"],
      packages=["logstore.web"] + ["logstore.web." + p for p in find_packages("src")],
      include_package_data=True,
      zip_safe=False,
      entry_points={
          "console_scripts": [
              "logstore = logstore.web.logan_runner:main"
              #"logstore_manage = logstore.web.logstore_manage:run"
          ]
      },
      extras_require = {
          'postgres': ["psycopg2"],
      },
      install_requires=[
          "logan",
          "logstore.extractor",
          "logstore.thrift-protocol",
          "logstore-geoip-transformer",
          "logstore-http-request-transformer",
          "logstore-user-agent-transformer",
          "django >= 1.6",
          "django.js",
          "django-debug-toolbar",
          "django-debug-toolbar-template-timings",
          "django-crispy-forms",
          "crispy-forms-foundation",
          "django-choice-object",
          "django-model-utils",
          "django-kronos",
          "pushbullet.py",
          "elasticsearch",
          "ipaddr",
          "thrift",
          "gunicorn",
          "pytz"])