from setuptools import find_packages, setup


setup(name="logstore-user-agent-transformer",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore_user_agent_transformer': 'src'},
      namespace_packages =["logstore", "logstore.ext", "logstore.ext.transformers"],
      packages=["logstore_user_agent_transformer"] + ["logstore_user_agent_transformer." + p
                                                      for p in find_packages("src")],
      install_requires=["httpagentparser", "logstore.extractor"])