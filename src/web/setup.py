from setuptools import find_packages, setup


setup(name="logstore.web",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.web': 'src'},
      namespace_packages =["logstore"],
      packages=["logstore.web"] + ["logstore.web." + p for p in find_packages("src")],
      entry_points={
          "console_scripts": [
              "logstore_manage = logstore.web.logstore_manage:run"
          ]
      },
      install_requires=[
          "logstore.extractor",
          "logstore.thrift-protocol",
          "logstore.ext.transformers.geoip",
          "logstore.ext.transformers.http-request",
          "logstore.ext.transformers.user-agent",
          "django >= 1.6",
          "django.js",
          "django-debug-toolbar",
          "django-debug-toolbar-template-timings",
          "django-crispy-forms",
          "crispy-forms-foundation",
          "django-model-utils",
          "django-kronos",
          "pushbullet.py",
          "elasticsearch",
          "psycopg2",
          "ipaddr",
          "thrift",
          "pytz"])