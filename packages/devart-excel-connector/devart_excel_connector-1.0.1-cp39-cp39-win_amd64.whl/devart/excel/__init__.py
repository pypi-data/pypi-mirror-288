"""
Python Connector for Microsoft Excel is a connectivity solution for accessing
Microsoft Excel, Apache OpenOffice Calc, and LibreOffice Calc spreadsheets
from Python applications. It fully implements the Python DB API 2.0
specification. The connector is distributed as a wheel package for Windows,
macOS, and Linux.
 
Direct connection

    Our connector provides the following advantages:
    - A direct access to an Excel workbook without installing Microsoft Excel or
    Microsoft Access Database Engine Redistributable components on the user's
    machine
    - Support for all major desktop platforms: Windows, macOS, and Linux
    - Support for the Microsoft Excel 2007-2021 Workbook (.xlsx), Microsoft Excel
    97-2003 Workbook (.xls), and OpenDocument Spreadsheet (.ods) file formats
    - A read-only multi-user mode that enables several users to read data from
    a workbook simultaneously

Version: 1.0.1 

Homepage: https://www.devart.com/python/excel/
"""
from .excel import *
