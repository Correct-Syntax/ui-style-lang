from setuptools import setup


setup(
  name = 'uistylelang',   
  packages = ['uistylelang'],   
  version = '0.5.0',
  license='BSD 3-Clause',   
  description = 'Simple CSS-like language which allows for drawing and styling wxPython elements.',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  author = 'Noah Rahm, Correct Syntax', 
  author_email = 'correctsyntax@yahoo.com',     
  url = 'https://github.com/Correct-Syntax/ui-style-lang', 
  keywords = ['wxPython', 'css', 'language', 'user interface', 'GUI', 'drawing'], 
  install_requires=[           
          'wxpython>=4.1.0'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Topic :: Desktop Environment',
    'License :: OSI Approved :: BSD License', 
    'Programming Language :: Python :: 3',
  ],
)
