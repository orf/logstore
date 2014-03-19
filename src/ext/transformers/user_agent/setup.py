from setuptools import find_packages, setup


setup(name="logstore.ext.transformers.user_agent",
      version="0.1",
      description="",
      author="Tom Forbes",
      author_email="tom@tomforb.es",
      package_dir = {'logstore.ext.user_agent_transformer': 'src'},
      namespace_packages =["logstore", "logstore.ext", "logstore.ext.transformers"],
      packages=["logstore.ext.transformers.user_agent"] + ["logstore.ext.transformers.user_agent." + p
                                                           for p in find_packages("src")],
      install_requires=["httpagentparser", "logstore.extractor"])