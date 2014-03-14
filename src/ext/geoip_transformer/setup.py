from setuptools import find_packages, setup


setup(name="logstore.ext.geoip_extractor",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.ext.geoip_transformer': 'src'},
      namespace_packages =["logstore", "logstore.ext"],
      packages=["logstore.ext.geoip_transformer"] + ["logstore.ext.geoip_transformer." + p for p in find_packages("src")],
      install_requires=["pygeoip", "django-kronos"])