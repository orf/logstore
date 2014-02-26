from setuptools import find_packages, setup


setup(name="logstore.analyser",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.analyser': 'src'},
      namespace_packages =["logstore"],
      packages=["logstore.analyser"] + ["logstore.analyser." + p for p in find_packages("src")],
      install_requires=[])