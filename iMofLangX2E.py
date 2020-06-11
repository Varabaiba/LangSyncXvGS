import xml.etree.ElementTree as ET
import gspread
from collections import defaultdict
import time

# Performance Block
xTimer = time.perf_counter()
print('Perftimer in: ', round(time.perf_counter(), 4))

# Constants
xLOFL = 'locs\\'
xLOCS = {'en': 'imof_en.xml', 'ru': 'imof_ru.xml', 'tj': 'imof_tj.xml'}
xGCRD: str = 'priv\\iMofCreds.json'
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


for xTempLocA in xLOCS:
    xCORE[xTempLocA] = ET.parse(xLOFL + xLOCS[xTempLocA]).getroot()[0]
    for xNODE in xCORE[xTempLocA]:
        xFXML[xNODE.attrib['name']][xTempLocA] = xNODE.attrib['value']

xLGWD = xGW.get_all_records()

# Processing existing records on the sheet
for xTempRow, xTmpRecA in enumerate(xLGWD):
    xTmpSRVal = xTmpRecA['sr']
    xTmpListA = []
    if xTmpSRVal in xFXML:
        # SR Value exist in the red XML-s
        xTmpListA.append(xTmpRecA['#'])
        xTmpListA.append(xTmpRecA['sr'])
        for xTempLocB in xLOCS:
            if len(xTmpRecA[xTempLocB]) == 0:
                xTmpListA.append(xFXML[xTmpRecA['sr']].get(xTempLocB, ''))  # Use value from XML if empty
            else:
                xTmpListA.append(xTmpRecA[xTempLocB]) # Use value from workbook if not empty
        xTXML.append(xTmpListA)
        xFXML.pop(xTmpSRVal)
    else:
        # SR Value not exist in the red XML-s
        xTmpListA.append(xTmpRecA['#'])
        xTmpListA.append(xTmpRecA['sr'])
        for xTempLocB in xLOCS:
            xTmpListA.append('SR DELETED')
        xTXML.append(xTmpListA)
        xFXML.pop(xTmpSRVal)
    xDROW += 1


# Adding new records on the sheet
for xTempRecB in xFXML:
    xTmpListB = [xRWNM - 1 + xDROW, xTempRecB]
    for xTempLocB in xLOCS:
        xTmpListB.append(xFXML[xTempRecB].get(xTempLocB, ''))
    xTXML.append(xTmpListB)
    xDROW += 1

# Update the sheet
xRngVal = 'A2:E'+str(xDROW+1)
xGW.update(xRngVal, xTXML)

# Performance Block
print('Perftimer out: ', round(time.perf_counter(), 4))
xTimer = time.perf_counter() - xTimer
print('Perftimer diff: ', round(xTimer, 4))
