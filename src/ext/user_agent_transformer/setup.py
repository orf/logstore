from setuptools import find_packages, setup


setup(name="logstore.ext.user_agent_extractor",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.ext.user_agent_transformer': 'src'},
      namespace_packages =["logstore", "logstore.ext"],
      packages=["logstore.ext.user_agent_transformer"] + ["logstore.ext.user_agent_transformer." + p for p in find_packages("src")],
      install_requires=["httpagentparser"])