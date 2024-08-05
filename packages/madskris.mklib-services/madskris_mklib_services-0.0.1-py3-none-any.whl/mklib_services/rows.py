from attrs import define, field, frozen
from datetime import date

@frozen
class Materiell():
    id: str
    navn: str
    leverandør: str
    ordreSystem: str
    eierskap: str
    enhetsType: str
    pris: float
    
@frozen
class Produkt():
    navn: str
    beskrivelse: str
    timerPlanlegging: float
    timerProsjektLeder: float
    timerMontør: float
    timerDok:float
    timerElektriker: float
    timerTotalt:float
    entreprenørPris: float
    materiellPris: float
    totalPris: float
    
@frozen
class ProduktPris():
    fylke: str
    navn: str
    beskrivelse: str
    pris: float
    
@frozen
class Ordre():
    id: int
    ifs: int
    fagOmråde: str
    status: str
    navn:str
    planDato: date
    sluttDato: date
    fylke: str
    avdeling: str
    ordreEier: str
    url: str