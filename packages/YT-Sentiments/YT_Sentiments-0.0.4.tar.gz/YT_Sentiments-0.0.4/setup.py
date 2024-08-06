from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

setup(name = "YT_Sentiments",
      version = "0.0.4",
      description = "analyze up to 12000 comments from any youtube video!",
      package_dir = {"":"src"},
      packages = find_packages(where="src"),
      long_description=long_description,
      long_description_content_type="text/markdown",
      url = "https://github.com/ZhengJiawen44/YT_Sentiment_Analyzer",
      author = "Zheng Jiawen",
      author_email="zhengjiawen44@gmail.com",
      license = "MIT",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   "Operating System :: OS Independent",
                   ],
      install_requires = ["emoji>=2.12.1",
                          "google_api_python_client>=2.139.0",
                          "vaderSentiment>=3.3.2",
                          "vaderSentiment>=3.3.2",],
      python_requires = ">=3.10",  
    )
