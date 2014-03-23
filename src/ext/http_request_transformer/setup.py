from setuptools import find_packages, setup


setup(name="logstore-http-request-transformer",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore_http_request_transformer': 'src'},
      packages=["logstore_http_request_transformer"] + ["logstore_http_request_transformer." + p
                                                        for p in find_packages("src")],
      install_requires=["logstore.extractor"])