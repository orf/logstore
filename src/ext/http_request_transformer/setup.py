from setuptools import find_packages, setup


setup(name="logstore.ext.http_request_transformer",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.ext.http_request_transformer': 'src'},
      namespace_packages =["logstore", "logstore.ext"],
      packages=["logstore.ext.http_request_transformer"] + ["logstore.ext.http_request_transformer." + p for p in find_packages("src")],
      install_requires=[])