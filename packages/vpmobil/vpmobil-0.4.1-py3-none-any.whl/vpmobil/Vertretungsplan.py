from datetime import datetime, date
import requests as WEB

from .workflow import Exceptions
from .VpDay import VpDay

class Vertretungsplan():
    """
    Enthält die notwendigen Daten um auf einen stundenplan24.de-Vertretungsplan zuzugreifen

    #### Argumente:
        schulnummer (int): Schulnummer des Vertretungsplans
        benutzer (str): Benutzername des Benutzers über den zugegriffen werden soll
        passwort (str): Passwort des Benutzers über den zugegriffen werden soll
        serverurl (str): URL und Verzeichnispfad, an dem die Quelldateien gespeichert werden
        dateipfadschema (str): Schema des Pfads der Quelldateien
            z.B. `PlanKl%Y%m%d.xml`. Es können [Platzhalter des datetime-Moduls](https://strftime.org/) verwendet werden

    #### Methoden:
        .fetch(): Ruft die Daten eines Tages ab
    """

    def __init__(self,
                 schulnummer: int,
                 benutzername: str,
                 passwort: str,
                 serverurl: str = 'stundenplan24.de',
                 dateipfadschema: str = "{schulnummer}/mobil/mobdaten/PlanKl%Y%m%d.xml"):
        """
        #### Argumente:
            schulnummer (int): Schulnummer des Vertretungsplans
            benutzer (str): Benutzername des Benutzers über den zugegriffen werden soll
            passwort (str): Passwort des Benutzers über den zugegriffen werden soll
            serverurl (str): URL und Verzeichnispfad
                Muss angegeben werden, wenn der Vertretungsplan selbst gehostet wird
            dateipfadschema (str): Schema des Pfads an dem die Quelldateien gespeichert werden
                z.B. `"{schulnummer}/mobil/mobdaten/PlanKl%Y%m%d.xml"`. Es können [Platzhalter des datetime-Moduls](https://strftime.org/) verwendet werden
        """
        self.schulnummer = schulnummer
        self.benutzername = benutzername
        self.passwort = passwort

        if serverurl.endswith('/'):
            serverurl= serverurl[:-1]
        if serverurl.startswith("http://") or serverurl.startswith("https://"):
            parts = serverurl.split("://", 1)
            serverurl = parts[1] if len(parts) > 1 else parts[0]
        self._webpath = f"http://{benutzername}:{passwort}@{serverurl.format(schulnummer=schulnummer)}"
        
        self._dateischema = dateipfadschema

    def __repr__(self): return f"Vertretungsplan {self.benutzername}@{self.schulnummer}"

    def fetch(self, datum: date | int = date.today(), datei: str = None):
        """
        Ruft die Daten eines Tages ab

        #### Argumente:
            datum (date | int | str): Abzurufender Tag
                int oder str muss im Schema yymmdd sein (z.B. `240609`)
            datei (str): Abzurufende Datei mit Dateipfad
                Ignoriert datum bei Angabe 

        #### Raises:
            FetchingError: Wenn für den Tag keine Daten verfügbar sind
        """

        datum: date = datetime.strptime(str(datum), "%Y%m%d").date() if isinstance(datum, int) else datum

        datei: str = datum.strftime(self._dateischema) if datei is None else datei
        uri = f"{self._webpath}/{datei.format(schulnummer=self.schulnummer)}"
        
        response = WEB.get(uri)

        if response.status_code != 200:
            raise Exceptions.FetchingError(f"Die Daten für das Datum {datum} konnten nicht abgerufen werden. Statuscode: {response.status_code}", status_code=response.status_code)

        return VpDay(mobdaten=response.content)