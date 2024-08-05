from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
path_to_readme = os.path.join(here, "README.md")

long_description = """# Proompter

Proompter

Wrapper for llm calls, meant for experimentation with different prompt and history 
handling strategies.

"""

if os.path.exists(path_to_readme):
  with codecs.open(path_to_readme, encoding="utf-8") as fh:
      long_description += fh.read()

setup(
    name="proompter",
    packages=["proompter"],
    install_requires=['### proompter.py', 'ollama==0.2.1', 'huggingface_hub==0.24.2', 'transformers==4.43.2', 'pandas==2.1.1', 'mocker_db==0.2.0', 'attrs==23.2.0'],
    classifiers=['Development Status :: 3 - Alpha', 'Intended Audience :: Developers', 'Intended Audience :: Science/Research', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.9', 'Programming Language :: Python :: 3.10', 'Programming Language :: Python :: 3.11', 'License :: OSI Approved :: MIT License', 'Topic :: Scientific/Engineering'],
    long_description=long_description,
    long_description_content_type='text/markdown',

    author="Kyrylo Mordan", author_email="parachute.repo@gmail.com", description="Simple wrapper around some Llm handlers.", version="0.0.2"
)
