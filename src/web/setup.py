from setuptools import find_packages, setup


setup(name="logstore.web",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.web': 'src'},
      namespace_packages =["logstore"],
      packages=["logstore.web"] +["logstore.web." + p for p in find_packages("src")],
      install_requires=["django >= 1.6"])