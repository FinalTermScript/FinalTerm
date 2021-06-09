from distutils.core import setup, Extension
spam_mod = Extension('spam', sources = ['spam.pyd'])
connect_mod = Extension('spam', sources = ['Connect.py'])
crawlimg_mod = Extension('spam', sources = ['CrawlImg.py'])
gmail_mod = Extension('spam', sources = ['Gmail.py'])
mainui_mod = Extension('spam', sources = ['MainUI.py'])
major_mod = Extension('spam', sources = ['Major.py'])
telegram_mod = Extension('spam', sources = ['TelegramBot.py'])
university_mod = Extension('spam', sources = ['University.py'])
resource_mod = Extension("resource", source=['resource\\'])

setup(name = "Fly-너의편입은",
    version = "1.0",
    description = "college",
    ext_modules = [spam_mod, connect_mod, crawlimg_mod, gmail_mod, mainui_mod, major_mod, telegram_mod, university_mod, resource_mod],
)
