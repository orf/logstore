from setuptools import find_packages, setup


setup(name="logstore.extractor",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.extractor': 'src'},
      namespace_packages =["logstore"],
      packages=["logstore.extractor"] + ["logstore.extractor." + p for p in find_packages("src")],
      install_requires=[])