import xml.etree.ElementTree as ET
import gspread
from collections import defaultdict
import time

# Performance Block
xTimer = time.perf_counter()
print('Perftimer in: ', round(time.perf_counter(), 4))

# Constants
xLOCS = {'en': 'imof_en.xml', 'ru': 'imof_ru.xml', 'tj': 'imof_tj.xml'}
xGCRD: str = 'iMofCreds.json'
xCORE: dict = {}
xRSLT: list = []
xDROW: int = 2  # Here start actual data rows
xRWNM: int = 100000  # Numbering Base

# Declarations
xFXML = defaultdict(dict)  # Data from all XML-s
xTXML = []  # Data to write to XSL

xGA = gspread.service_account(filename=xGCRD)
xGS = xGA.open_by_key('1_WgKOTJUBKRmDEbB0e7ZabyXf1HpkCiv2pDAPaN7Uig')
xGW = xGS.worksheet('SRN1')

xLGWD = xGW.get_all_records()
xLGWX = {xTempItem['sr'] : [xTempItem['en']] for xTempItem in xLGWD}
print(xLGWX)

# for xTempLocA in xLOCS:
#     xCORE[xTempLocA] = ET.parse(xLOCS[xTempLocA]).getroot()[0]
#     for TempNodeA in xCORE[xTempLocA]:
#         if TempNodeA.attrib['name'] in xLGWD:
#             print('Lang: ', xTempLocA, 'Node: ', TempNodeA.attrib['name'])


# Performance Block
print('Perftimer out: ', round(time.perf_counter(), 4))
xTimer = time.perf_counter() - xTimer
print('Perftimer diff: ', round(xTimer, 4))
