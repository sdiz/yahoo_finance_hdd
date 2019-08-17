from distutils.core import setup
setup(
  name = 'yahoo_finance_hdd',         
  packages = ['yahoo_finance_hdd'],   
  version = '0.2',      
  license='MIT',        
  description = 'Download historical financial data from yahoo finance',   
  author = 'Serkan Dizbay',                   
  url = 'https://github.com/sdiz/yahoo_finance_hdd.git',   
  download_url = 'https://github.com/sdiz/yahoo_finance_hdd/archive/v_0.2.tar.gz',
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