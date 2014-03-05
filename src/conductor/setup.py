from setuptools import find_packages, setup


setup(name="logstore.conductor",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.conductor': 'src'},
      namespace_packages =["logstore"],
      packages=["logstore.conductor"] + ["twisted.plugins"] + ["logstore.conductor." + p for p in find_packages("src")],
      package_data={
          'twisted.plugins': ['conductor_plugin.py']
      },
      install_requires=["logstore.thrift_protocol",
                        "logstore.web",
                        "twisted==13.2.0",
                        "autobahn",
                        "pika",
                        "treq"])

try:
    from twisted.plugin import IPlugin, getPlugins
except ImportError:
    pass
else:
    list(getPlugins(IPlugin)) # Refresh the twisted plugin cache or something