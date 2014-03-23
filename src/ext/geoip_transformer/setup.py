from setuptools import find_packages, setup


setup(name="logstore-geoip-transformer",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore_geoip_transformer': 'src'},
      packages=["logstore_geoip_transformer"] + ["logstore_geoip_transformer." + p
                                                 for p in find_packages("src")],
      install_requires=["pygeoip", "django-kronos", "logstore.extractor"])