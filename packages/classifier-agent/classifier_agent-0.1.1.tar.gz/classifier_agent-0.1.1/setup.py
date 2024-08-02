from setuptools import setup
 
with open("Readme.md", "r") as myfile:
  long_description = myfile.read()
 
setup(
  name='classifier_agent',
  version='0.1.1', 
  description='A simple package to perform classification on a given dataset in csv or excel format',
  long_description = long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/adnanmushtaq1996/ML-Classifier-Python-Package',  
  author='Adnan Karol',
  author_email='adnanmushtaq5@gmail.com',
  license='MIT', 
  classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
  keywords= ['machine learning', 'classification', 'random forest', 
             'xgboost', 'svm', 'logistic regression', 'naive bayes', 'knn', 'decision tree'], 
  python_requires='>=3.6'
)