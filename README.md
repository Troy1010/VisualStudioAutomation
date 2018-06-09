VisualStudioAutomation

Unfortunately, some features of Visual Studio's DTE object seem to be inaccessable by pythonwin32.
1)The DTE will throw errors if multiple threads prompt it. There is a fix by replacing the COM error handler, but I think python is lacking the command to insert it.
2)pywin32 can't read all COM object types. For example, the configs within ConfigurationManager are a matrix type and seem to be unreadable.

In order to access more automation features, you must write in another language or to simply directly edit files such as .proj .sln.
