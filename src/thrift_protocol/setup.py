from setuptools import find_packages, setup

setup(name="logstore.thrift-protocol",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.thrift_protocol': 'src'},
      namespace_packages =["logstore"],
      packages=["logstore.thrift_protocol"] + ["logstore.thrift_protocol." + p for p in find_packages("src")],
      install_requires=["thrift"])