from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'yahoo_finance_hdd',         
  packages = ['yahoo_finance_hdd'],   
  version = '0.2.1',      
  license='MIT',        
  description = 'Download historical financial data from yahoo finance',   
  author = 'Serkan Dizbay',                   
  url = 'https://github.com/sdiz/yahoo_finance_hdd.git',   
  download_url = 'https://github.com/sdiz/yahoo_finance_hdd/archive/v_0.2.1.tar.gz',
  long_description=long_description,
  long_description_content_type='text/markdown',
  keywords = ['financial data', 'yahoo finance'],  
  install_requires=[            
          'numpy',
          'pandas',
          'requests',
          'datetime',
          'pandas_market_calendars',
      ],
  classifiers=[
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: 3",
  ],
)