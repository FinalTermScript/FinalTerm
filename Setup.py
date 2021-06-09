from distutils.core import setup

setup(name='FLY', version='1.0',
      py_modules=['Connect','CrawlImg','Gmail','MainUI','Major','TelegramBot','University'],
      data_files=[('resource', ['chromedriver.exe','resource\\globe.png','resource\\location.png','resource\\gmail.png'],)]
      #include_package_data=True
      )