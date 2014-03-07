from setuptools import find_packages, setup


setup(name="logstore.web",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.web': 'src'},
      namespace_packages =["logstore"],
      packages=["logstore.web"] + ["logstore.web." + p for p in find_packages("src")],
      install_requires=[
          "logstore.extractor",
          "django >= 1.6",
          "django.js",
          "django-debug-toolbar",
          "django-debug-toolbar-template-timings",
          "django-crispy-forms",
          "crispy-forms-foundation",
          "django-activeurl",
          "django-model-utils",
          "django-kronos",
          "elasticsearch",
          "psycopg2",
          "ipaddr",
          "pygeoip",
          "pytz"])