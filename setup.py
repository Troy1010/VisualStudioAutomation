from setuptools import setup

setup(name='Macro_VisualStudio',
      version='0.1',
      description=r'Convenience function for writing Visual Studio macros',
      author='Troy1010',
      #author_email='',
      #url='',
      license='MIT',
      packages=['Macro_VisualStudio'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      python_requires=">=3.6",
      install_requires=[
          'TM_CommonPy'
          ],
      setup_requires=[
          #?Why doesn't this work?
          #I'll come back to it later. For now, people will have to install TM_CommonPy on their own..
          #'TM_CommonPy @ https://github.com/Troy1010'
          'TM_CommonPy'
          ],
      )
