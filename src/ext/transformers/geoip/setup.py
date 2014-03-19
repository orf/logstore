from setuptools import find_packages, setup


setup(name="logstore.ext.transformers.geoip",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.ext.transformers.geoip': 'src'},
      namespace_packages =["logstore", "logstore.ext", "logstore.ext.transformers"],
      packages=["logstore.ext.transformers.geoip"] + ["logstore.ext.transformers.geoip." + p
                                                      for p in find_packages("src")],
      install_requires=["pygeoip", "django-kronos", "logstore.extractor"])