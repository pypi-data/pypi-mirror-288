import pandas as pd
from pandas import DataFrame
from .data import DataResult
from .rows import Materiell, Produkt, ProduktPris, Ordre

folderPath = "../Files"

def readOpitel() -> DataResult[DataFrame]:
    result = readExcelFile("OpitelOverview.xlsx", "Opitel_open Database")
    if result.successful:
        return result
    
    return DataResult(f"[readPriser]: {result.error}")

def getOpitel() -> DataResult[list[Ordre]]:
    result = readOpitel()
    if result.successful is False:
        return DataResult(result.error)
    
    ordrer = result.data
    if len(ordrer.columns) != 37:
        return DataResult(f"[getOrdrer]: Malformed header length {(len(ordrer.columns))}")
    
    parsed: list[Ordre] = []
    for name, row in ordrer.iterrows():
        parsed.append(
            Ordre(
                row.iloc[1],
                row.iloc[2],
                row.iloc[3],
                row.iloc[4],
                row.iloc[6],                
                row.iloc[7],
                row.iloc[8],                
                row.iloc[9],
                row.iloc[10],
                row.iloc[11],
                row.iloc[22],
            )
        )    
    
    return DataResult(parsed)

def readPriser() -> DataResult[DataFrame]:
    
    result = readExcelFile("TelenorPriser.xlsx")
    if result.successful:
        return result
    
    return DataResult(f"[readPriser]: {result.error}")

def getPriser() -> DataResult[list[ProduktPris]]:
    
    result = readPriser()
    if result.successful is False:
        return DataResult(result.error)
    
    produktPriser = result.data
    if len(produktPriser.columns) != 4:
        return DataResult(f"[getProdukter]: Malformed header length {(len(produktPriser.columns))}")
    
    parsed: list[ProduktPris] = []
    for name, row in produktPriser.iterrows():
        parsed.append(
            ProduktPris(
                row.iloc[0],
                row.iloc[1],
                row.iloc[2],
                row.iloc[3],
            )
        )    
    
    return DataResult(parsed)

def readProdukter() -> DataResult[DataFrame]:
    
    result = readExcelFile("Produkter.xlsx")
    if result.successful:
        return result
    
    return DataResult(f"[readProdukter]: {result.error}")

def getProdukter() -> DataResult[list[Produkt]]:
    
    result = readProdukter()
    if result.successful is False:
        return DataResult(result.error)
    
    produkter = result.data    
    if len(produkter.columns) != 16:
        return DataResult(f"[getProdukter]: Malformed header length {(len(produkter.columns))}")
    
    parsed: list[Produkt] = []
    for name, row in produkter.iterrows():
        parsed.append(
            Produkt(
                row.iloc[0],
                row.iloc[1],
                row.iloc[2],
                row.iloc[3],
                row.iloc[4],
                row.iloc[5],
                row.iloc[6],
                row.iloc[7],
                row.iloc[8],
                row.iloc[9],
                row.iloc[11],
            )
        )
        
    return DataResult(parsed)

def readMateriell() -> DataResult[DataFrame]:

    result = readExcelFile("Materiell.xlsx")

    if result.successful:
        return result

    return DataResult(f"[readMateriell]: {result.error}")

def getMateriell() -> DataResult[list[Materiell]]:
    
    result = readMateriell()        
    if result.successful is False:
        return DataResult(result.error)

    materiell = result.data
    if len(materiell.columns) != 7:
        return DataResult(f"[getMateriell]: Malformed header length {(len(materiell.columns))}")
    
    parsed: list[Materiell] = []
    for name, row in materiell.iterrows():
        parsed.append(
            Materiell(
                row.iloc[0],
                row.iloc[1],
                row.iloc[2],
                row.iloc[3],
                row.iloc[4],
                row.iloc[5],
                row.iloc[6]
            )
        )
    
    return DataResult(parsed)
    
def readExcelFile(name: str, sheet="Sheet1") -> DataResult[DataFrame]:

    try:
        excelFile = pd.read_excel(f"{folderPath}/{name}", sheet_name=sheet, engine="openpyxl")
    except FileNotFoundError as ex:
        return DataResult(f"File not found: '{ex.filename}'.")
    except ValueError as ex:
        return DataResult(f"No worksheet named '{sheet}' in '{name}'.")
    if excelFile.empty:
        return DataResult(f"Worksheet '{sheet}' is empty")

    return DataResult(excelFile)

def readCsvFile(name: str) -> DataResult[DataFrame]:
    
    try:
        csvFile = pd.read_csv(f"{folderPath}/{name}", encoding= "ISO-8859-1", delimiter=";")
    except FileNotFoundError as ex:
        return DataResult(f"File not found: '{ex.filename}'.")
    if csvFile.empty:
        return DataResult(f"CSV file '{name}' is empty")

    return DataResult(csvFile)