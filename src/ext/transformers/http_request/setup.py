from setuptools import find_packages, setup


setup(name="logstore.ext.transformers.http_request",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.ext.transformers.http_request': 'src'},
      namespace_packages =["logstore", "logstore.ext", "logstore.ext.transformers"],
      packages=["logstore.ext.transformers.http_request"] + ["logstore.ext.transformers.http_request." + p
                                                             for p in find_packages("src")],
      install_requires=[])