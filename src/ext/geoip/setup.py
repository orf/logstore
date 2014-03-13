from setuptools import find_packages, setup


setup(name="logstore.ext.geoip",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.ext.geoip': 'src'},
      namespace_packages =["logstore", "logstore.ext"],
      packages=["logstore.ext.geoip"] + ["logstore.ext.geoip." + p for p in find_packages("src")],
      install_requires=["pygeoip"])