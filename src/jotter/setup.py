from setuptools import find_packages, setup


setup(name="logstore.jotter",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.jotter': 'src'},
      namespace_packages =["logstore"],
      packages=["logstore.jotter"] + ["logstore.jotter." + p for p in find_packages("src")],
      install_requires=["logstore.thrift-protocol",
                        "twisted==13.2.0",
                        "python-dateutil",
                        "fake-factory"],
      entry_points={
          "console_scripts": [
              "jotter = logstore.jotter.jotter:main",
              "logstore_fake_data = logstore.jotter.generate_random_data:main"
          ]
      })