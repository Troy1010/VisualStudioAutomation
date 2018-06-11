from setuptools import setup

setup(name='VisualStudioAutomation'
    ,version='0.1'
    ,description=r'Convenience functions for writing Visual Studio macros'
    ,author='Troy1010'
    #,author_email=''
    #,url=''
    ,license='MIT'
    ,packages=['VisualStudioAutomation']
    ,zip_safe=False
    ,test_suite='nose.collector'
    ,tests_require=['nose']
    ,python_requires=">=3.6"
    ,install_requires=['TM_CommonPy']
    ,setup_requires=['TM_CommonPy'
        #?Why doesn't this work?
        #I'll come back to it later. For now, people will have to install TM_CommonPy on their own..
        #'TM_CommonPy @ https://github.com/Troy1010'

        ,'nose'
        ]
      )
