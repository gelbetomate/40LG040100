# LG250 Code-Status (40LG040100)

Stand: 2026-08-13
Quelle: aktuelle Nutzkonfiguration, ESPHome-Logs und Feldtest auf deiner Anlage

## 1) Aktive Sensor-Codes (Produktiv)

| Code | Funktion | Einheit | Intervall | Beobachtete Werte | Status | Plausibilitaet | Empfehlung |
|---|---|---|---|---|---|---|---|
| T1 | Verdampfertemperatur | degC | 30s | 28.8 bis 29.0 | funktioniert | plausibel und stabil | aktiv lassen |
| T2 | Kondensatortemperatur | degC | 30s | 26.9 | funktioniert | plausibel und stabil | aktiv lassen |
| T3 | Aussentemperatur | degC | 30s | 26.0 | funktioniert | plausibel und stabil | aktiv lassen |
| T4 | Ablufttemperatur Raum | degC | 30s | 26.9 bis 27.0 | funktioniert | plausibel und stabil | aktiv lassen |
| T5 | Nach Waermetauscher Fortluft | degC | 30s | 0.0 | funktioniert | numerisch gueltig, fachlich anlagenseitig pruefen | aktiv lassen, Verlauf beobachten |
| NA | Drehzahl Abluft | rpm | 30s | ca. 1007 bis 1171 | funktioniert | plausibel, dynamisch zur Stufe passend | aktiv lassen |
| NZ | Drehzahl Zuluft | rpm | 30s | ca. 1245 bis 1261 | funktioniert | plausibel, dynamisch zur Stufe passend | aktiv lassen |
| UA | Steuerspannung Abluft | V | 60s | 31.0 | funktioniert | plausibel und stabil | aktiv lassen |
| UZ | Steuerspannung Zuluft | V | 60s | 35.0 | funktioniert | plausibel und stabil | aktiv lassen |
| RA | Rueckwaermzahl | % | 60s | 1.0 | funktioniert | numerisch stabil, fachlich sehr niedrig | aktiv lassen, spaeter verifizieren |
| LS | Aktuelle Luftstufe | Stufe | 30s | 2 | funktioniert | plausibel zu L1/L2/L3 | aktiv lassen |
| L1 | Luftstufe 1 Sollwert | % | 2min | 20 | funktioniert | plausibel | aktiv lassen |
| L2 | Luftstufe 2 Sollwert | % | 2min | 33 | funktioniert | plausibel | aktiv lassen |
| L3 | Luftstufe 3 Sollwert | % | 2min | 68 | funktioniert | plausibel | aktiv lassen |
| ER | Fehlercode Leistungsteil Rohwert | Code | 60s | 0 | funktioniert | gueltig, kein Fehler aktiv | aktiv lassen |

## 1.1 Feldtest Betriebsarten und Statusregister

Die Betriebsarten und Lueftungsstufen wurden am Bedienteil veraendert und anschliessend ueber die Register gelesen. Die Stufe wird ueber `LS` erkannt; `ST` ist ein zusammengesetztes Statusbitfeld und kein weiterer Stufenwert.

| Beobachtung | Registerwerte | Gesicherte Aussage |
|---|---|---|
| manueller Betrieb, Stufe 2 oder 3 | `LS=2` bzw. `LS=3` | aktuelle manuelle Lueftungsstufe |
| Automatikbetrieb | `LS=4` | Automatik-/Grundlueftungsmodus |
| laufende Anlage | `ST=48` oder `ST=52` | `ST` enthaelt mehrere Statusbits |
| laufende Ventilatoren | `ST` enthaelt Bit 32 | Bit 32 ist als Luefter aktiv plausibel |
| manuell und automatisch | `ST` enthaelt Bit 16 | Bit 16 bedeutet nicht automatisch "Automatik aktiv" |
| Wechsel zwischen `ST=48` und `ST=52` | Differenz ist Bit 4 | Bit 4 ist wahrscheinlich betriebsartabhaengig, fachliche Bezeichnung noch offen |
| Fehlerabfrage in allen Testzustaenden | `ER=0` | kein Fehler im Fehlerregister |

Die Werte `48` und `52` entsprechen `0b00110000` beziehungsweise `0b00110100`. Der einzige Unterschied ist Bit 4. Die Testfolge spricht dafuer, dass dieses Bit mit Sommer-/Winterbetrieb zusammenhaengt; das ist noch nicht unabhaengig bestaetigt. Bit 8 wurde in der Testreihe nicht beobachtet.

Die Klartextdiagnose darf deshalb Bit 16 nicht als "Automatik aktiv" ausgeben. `MO` liefert auf dieser Firmware weiterhin `??????.` und kann den Betriebsmodus nicht bestaetigen.

## 1.2 Schreibverhalten

Manuelle Schreibtests wurden mit `enable_unsafe_writes: true` und `enable_rs_handshake: false` durchgefuehrt. Die Auswahl erreicht den Schreibpfad, aber die Steuerung antwortet auf `LS`, `MD` und `SW` mit `NAK`. Die Hermes-PDF beschreibt `SW` zwar als nur bei PC-Steuerung verwendbar; ob `RS=1` auf der Pichler-LG250 diese Freigabe aktiviert, ist noch nicht durch einen Feldtest bestaetigt.

Die automatischen Startup-/Polling-Schreibvorgaenge fuer `SW` und `MD` wurden anschliessend aus den Komponenten entfernt. Manuelle Schreibaktionen bleiben grundsaetzlich aktiv. Nach dem Neustart waren keine wiederkehrenden automatischen `SW=0`- oder `MD=0`-Schreibversuche mehr im Log sichtbar.

### Readback nach NAK

Antworten wie `??????.` koennen formal als gueltige Antworttelegramme ankommen, sind aber kein numerischer Status. Sie duerfen deshalb nicht als `0` uebernommen werden. Die Value-Holder pruefen Readbacks jetzt strikt numerisch; bei einem ungueltigen `SW`- oder `MD`-Readback bleibt der bisherige interne Zustand erhalten.

Selects veroeffentlichen einen neuen Wert erst nach bestaetigtem Write. Bei `NAK` oder ungueltigem Readback bleibt in Home Assistant der zuletzt bestaetigte Anlagenzustand sichtbar.

### 1.2.1 Offizielle Pichler-Modbusliste fuer LG150/LG250A

Die lokal vorliegende Datei `documents/LIST_Modbus_ES1015_FW_LG150AB_LG250A_v2.0.0.xlsx` beschreibt eine separate Modbus-Schnittstelle:

- Datapoints werden mit Funktionscode 04 als Input Register gelesen.
- Setpoints werden mit Funktionscode 03 gelesen und Funktionscode 06 geschrieben.
- Alle Werte sind unsigned 16-Bit-Register.
- Die Liste enthaelt keine Bit-Untertabellen fuer `Betriebsstatus`; eine Aussage wie "Bit 16" ist daraus nicht ableitbar.

Relevante offizielle Modbus-Adressen:

| Funktion | Modbus-Adresse | Typ | Dokumentierte Bedeutung |
|---|---:|---|---|
| Sommer-/Winterbetrieb | 1 | Setpoint | `1=Sommer`, `2=Winter` |
| Luftstufe | 2 | Setpoint | `0=Standby`, `1=LS1`, `2=LS2`, `3=LS3`, `4=Grundlueftung` |
| Betriebsstatus | 48 | Input Register | Betriebsstatus, ohne Bitaufloesung in der Liste |
| Filter-Restzeit | 50 | Input Register | Naechster Filterwechsel in Stunden |
| Bypass-Klappenposition | 51 | Input Register | Klappenposition |
| Aktuelle Luftstufe | 59 | Input Register | aktuelle Lueftungsstufe |
| Fehler Z01 bis Z21 | 60 bis 80 | Input Register | einzelne Fehler-/Statusmeldungen |
| Betriebsstunden LS2/LS3/Grund/gesamt | 81 bis 84 | Input Register | Betriebsstunden |
| Betriebsstunden Vorheizregister/Bypass/LS1 | 85, 86, 88 | Input Register | Betriebsstunden |

Wichtig fuer dieses Projekt: Diese Adressen sind Modbus-Adressen und keine neuen Befehle fuer das aktuell implementierte Hermes-/WR3223-Textprotokoll (`LS`, `ST`, `SW`, `MD` usw.). Die offiziellen Modbus-Datapoints sind zudem laut Liste lesbar; Schreibzugriffe sind nur fuer die Setpoints dokumentiert. Deshalb erklaert die Liste die bisherigen `NAK`-Antworten auf `SW` und `MD` nicht direkt und darf nicht ohne einen Modbus-Funktionscode-Adapter in die bestehende YAML-Komponente uebersetzt werden.

Die offizielle Definition bestaetigt jedoch die fachliche Interpretation von `LS=4`: Das entspricht `Grundlueftung`. Sie bestaetigt nicht, dass `ST` die Luftstufe oder einen Automatik-Bitwert enthaelt. Die beobachteten Werte `ST=48` und `ST=52` bleiben daher bis zu einer herstellerspezifischen Bitbeschreibung ein empirisches Rohstatusfeld.

### 1.2.2 Webserver-Beispiel aus der Hermes-Schnittstelle

Der Beispielcode unter `documents/webserver/` ist fuer die Protokollanalyse besonders relevant. In `htl-pic.c` wird ein serieller Datenstrom mit folgendem Format verarbeitet:

- Baudrate im Beispiel: 19200.
- Telegrammstart: Byte `4` (`SOT`).
- Telegrammende: Byte `5` (`EOT`).
- Vor der Telegramm-ID wird an Position 2 ein Nullbyte erwartet.
- Die Telegramm-ID steht an Position 3.
- Nutzdaten beginnen bei Position 8.
- Fuer die dort verwendeten Telegramme wird keine XOR- oder CRC-Pruefsumme verarbeitet.

Der Parser kennt mindestens diese IDs:

| ID | Bedeutung | Nutzdaten |
|---:|---|---|
| 17 | Filter-Restlaufzeit | Bytes 8 und 9, 16-Bit-Wert |
| 8 | aktuelle Luftstufe | Byte 8 |
| 7 | Raum-Solltemperatur | Byte 8 |
| 6 | Raum-Isttemperatur | Bytes 8 und 9, 16-Bit-Wert / 10 |

Besonders wichtig fuer die Binärcode-Suche ist die explizite Sonderbehandlung:

```c
if (lst == 85) { lst = 4; }
```

Damit ist fuer diese Schnittstellenvariante dokumentiert, dass der Rohwert `85` (`0x55`) die fachliche Luftstufe `4` beziehungsweise Grundlueftung repraesentiert. Das passt zur offiziellen Modbusliste, die fuer die Luftstufe ebenfalls `4=Grundlueftung` definiert. Es ist aber noch nicht bewiesen, dass unser aktueller `LS`-Readback denselben Rohwertpfad benutzt; dort beobachten wir bisher bereits formatierte Werte wie `4`.

Der Webserver-Code ist deshalb ein starker Hinweis auf ein Hermes-/Twin-Datenprotokoll, aber kein Beweis fuer identische Telegramme auf unserem Anschluss: Beispiel und aktueller ESPHome-Aufbau unterscheiden sich bei Baudrate, Rahmenbytes und Datenformat. Die Klasse `WR3223Connector` darf daher nicht allein aufgrund ihres Namens als Herstellerbezeichnung gelten. Vor einer Änderung am Connector müssen ein aufgezeichnetes Telegramm oder die PDF-Spezifikation bestätigen, ob der LG250-Anschluss die Variante mit `SOT=4/EOT=5` oder die aktuell beobachtete Variante mit `EOT=4/ENQ=5`, `STX/ETX` und XOR verwendet.

Der Beispielcode liefert dennoch direkt verwertbare Tests:

1. Nach Rohwert `0x55` fuer die Luftstufe suchen.
2. Eine Filter-Restlaufzeit als 16-Bit-High-/Low-Byte pruefen.
3. Raumtemperatur als 16-Bit-Wert mit Faktor 0.1 pruefen.
4. Die Telegramm-ID-Positionen und Rahmenbytes getrennt vom bestehenden `LS`-/`ST`-Textparser protokollieren.

### 1.2.3 Ergebnisse aus der Hermes PDF-Dokumentation

Die Schnittstellen-PDF bestaetigt die Registernamen und liefert erstmals offizielle Bitbelegungen.

#### Register-Uebersicht laut PDF

Alle bisher verwendeten Register sind durch die PDF bestaetigt: `AE`, `AA`, `Az`, `Aa`, `AR`, `AZ`, `AP`, `AN`, `AV`, `T1`-`T8`, `LS`, `L1`-`L3`, `LD`, `Ld`, `EC`, `Es`, `ES`, `EW`, `EE`, `EA`, `ER`, `ST`, `SW`, `RL`, `UZ`, `UA`, `NZ`, `NA`, `NM`, `MD`, `CN`, `KM`, `ZH`, `ZE`, `WP`, `PA`, `II`, `rT`.

Die Register `MO`, `BY`, `HP`, `HZ` sind in der PDF nicht aufgefuehrt. Das erklaert, warum diese Befehle auf der LG250 `??????.` zurueckliefern.

#### SW - der entscheidende Fund

Die PDF beschreibt `SW` explizit als:

> SW - Status schreib byte auslesen/schreiben **(nur bei PC Steuerung)**

Das ist eine plausible Erklaerung fuer das `NAK` bei SW-Schreibzugriffen, aber noch kein Nachweis fuer die konkrete Pichler-LG250-Firmware. Dafuer existiert im Connector ein optionaler RS-Handshake-Pfad (`send_write_request RS=1` vor dem SW-Write). Er bleibt in der Produktiv-YAML vorerst deaktiviert, bis ein kontrollierter Feldtest bestaetigt, dass `RS=1` den RL-Zustand `Bedienung ueber RS Schnittstelle` setzt und anschliessende SW-/MD-Schreibzugriffe akzeptiert werden.

#### RL - vollstaendige offizielle Bitmaske

Die Bitmaske fuer `RL` (Relais lesen) ist jetzt durch die PDF gesichert:

| Bitmask | Bedeutung |
|---:|---|
| 1 | Kompressor |
| 2 | Zusatzheizung Relais |
| 4 | Erdwaermetauscher |
| 8 | Bypass |
| 16 | Vorheizregister |
| 32 | Netzrelais Bypass |
| 64 | Bedienteil aktiv |
| 128 | Bedienung ueber RS Schnittstelle |
| 256 | Luftstufe vorhanden |
| 512 | WW_Nachheizregister |
| 2048 | Magnetventil |
| 4096 | Vorheizen aktiv |

Die Bitmaske in `binary_sensor.py` stimmt vollstaendig mit der PDF ueberein; das Bitmuster springt absichtlich von 512 auf 2048 und laesst 1024 aus.

#### ER - offizielle Fehlercodes

| Hex-Wert | Dezimalwert | Bedeutung |
|---|---:|---|
| 0x00 | 0 | kein Fehler |
| 0x81 | 129 | Drehzahldifferenz (delta_n_error) |
| 0x80 | 128 | Zuluftventilator / n500error |
| 0x84 | 132 | Abluftventilator |
| 0x82 | 130 | Kondensatorfehler |
| 0x04 | 4 | HD-Fehler |
| 0x85 | 133 | Vorheizregister-Fehler |
| 0x3y | 49-56 | Unterbrechung Sensor y (y=1 T1, y=2 T2, y=3 T3, y=5 T5, y=6 T6, y=7 EWT, y=8 VHR) |
| 0x1y | 17-24 | Kurzschluss Sensor y (gleiche y-Zuordnung) |

Der `ER`-Sensor hat jetzt eine Klartextdiagnose (`LG250 ER Fehlerdiagnose`), die alle obigen Codes dekodiert.

#### Temperatursensoren T1-T6 laut PDF

Die YAML-Sensor-Labels waren falsch benannt. Korrekte Zuordnung laut PDF:

| Register | Offizielle Bedeutung |
|---|---|
| T1 | Verdampfertemperatur Istwert |
| T2 | Kondensatortemperatur |
| T3 | Aussentemperatur |
| T4 | Ablufttemperatur (Raumtemperatur) - nicht in der PDF explizit, aber bestaetigt durch Feldtest |
| T5 | Temperatur nach Waermetauscher (Fortluft) |
| T6 | Zulufttemperatur - neu aktiviert |
| T7 | Temperatur nach Solevorwaermung |
| T8 | Temperatur nach Vorheizregister |

Die YAML-Sensornamen wurden korrigiert und T6 wurde neu hinzugefuegt.

#### rT - Relaistest

`rT` ist ein reines Schreib-Register fuer Relaistests:
- `rT 0x5501`: Test Relais 1
- `rT 0x5502`: Test Relais 2
- `rT 0x550C`: Test Relais 12

Dieser Befehl ist nur fuer Servicezwecke relevant und nicht in der produktiven YAML aktiviert.

#### ST - noch ohne offizielle Bitdefinition

Die PDF beschreibt `ST` nur als „Status auslesen" ohne Bitaufschluesselung. Die empirisch ermittelten Werte `ST=48` (0b00110000) und `ST=52` (0b00110100) bleiben vorlaeufig mit neutralen Labels. Die Bitdefinitionen aus einer Hermes-/WR3223-Dokumentation duerfen nicht automatisch der Pichler-LG250 zugeordnet werden.

## 1.3 Display-Menues und Zielabbildung in Home Assistant

Die Screenshots zeigen ein BDE-Comfort-Bedienteil. Die Menues lassen sich fuer Home Assistant in folgende Funktionsgruppen ordnen:

### A) Hauptanzeige

Die Hauptanzeige zeigt:

- Uhrzeit und Datum
- aktuelle Lueftungsstufe, zum Beispiel `Luftstufe 3`
- Jahreszeit, `Sommer` oder `Winter`
- Raumtemperatur
- Betriebsart, zum Beispiel `Automatikbetrieb`

Ziel in HA: eine kompakte Statusansicht aus `LS`, `ST`, `T4` beziehungsweise der passenden Raumtemperatur und den Ventilatordrehzahlen. `LS=1..3` steht fuer manuelle Stufen; `LS=4` wird auf dieser Anlage als Automatik-/Grundlueftungsmodus beobachtet.

### B) Steuerung

Das Menue "Steuerung" umfasst:

1. Betriebsmodus: `Sommerbetrieb` oder `Winterbetrieb`
2. Kuehlung: Ein/Aus
3. Lueftungsstufe: `Aus`, `Luftstufe 1`, `Luftstufe 2`, `Luftstufe 3`, Automatik beziehungsweise Grundlueftung
4. Waermepumpe: Ein/Aus
5. Zusatzheizung: Ein/Aus

Ziel in HA: ein Select fuer den Betriebsmodus, ein Select fuer die Lueftungsstufe sowie Switches fuer Kuehlung, Waermepumpe und Zusatzheizung. Die zugehoerigen Protokollkandidaten sind `MD`, `LS` beziehungsweise `SW`; die LG250 quittiert aktuelle Schreibversuche jedoch noch mit `NAK`.

### C) Zeitprogramme

Es gibt getrennte Zeitprogramme fuer:

- Sommer
- Winter

Ein Zeitprogramm enthaelt mindestens:

- Wochentag
- Beginn
- Ende
- Zielstufe, zum Beispiel `Luftstufe 3` oder `Grundlueftung`
- Speichern beziehungsweise Aktivieren

Ziel in HA: Wochenplan oder mehrere Zeitplan-Automationen. Die Zeitplanwerte sind in den bisher getesteten Registern noch nicht belastbar identifiziert. Die direkt getesteten Kandidaten `H1` bis `H4`, `HL`, `FH` und `FR` liefern auf dieser Anlage keine gueltigen Werte oder Platzhalterantworten.

### D) Filter und Wartung

Das Display zeigt:

- Filter-Restlaufzeit, im Screenshot `2284 h`
- Filter Reset

Ziel in HA: Sensor fuer die Filterlaufzeit und ein Button fuer den Reset. Der angefragte Wert ist noch nicht sicher einem lesbaren Register zugeordnet; `FH` und `FR` waren auf dieser Firmware nicht gueltig. Ein Reset darf erst implementiert werden, wenn das Schreibregister und die erforderliche Sequenz bekannt sind.

### E) Fehlerspeicher

Das Display kann bis zu fuenf Fehler anzeigen, jeweils mit:

- Fehlernummer
- Fehlertext
- Datum/Uhrzeit

Ziel in HA: Fehlerbit, aktueller Fehlertext und spaeter ein Fehlerarchiv. `ER=0` liefert aktuell verlaesslich "kein Fehler". Ein historischer Fehlerspeicher ist durch `ER` allein noch nicht abgedeckt.

### F) Systeminformationen

Die Systeminformationen zeigen unter anderem:

- Betriebsstunden je Luftstufe
- Betriebsstunden Grundlueftung
- Betriebsstunden Zusatzheizung
- Betriebsstunden Sole-EWT
- Raum-Solltemperatur
- Filter-Restlaufzeit
- Geraetetyp und Softwarestand

Ziel in HA: diagnostische Sensoren fuer Laufzeiten, Raum-Solltemperatur, Filterzeit, Geraet und Firmware. Die Screenshots bestaetigen die fachlichen Werte, aber nicht die Protokollregister. Die bisher getesteten Stundenregister `H1` bis `H4` und `HL` waren auf dieser LG250 nicht lesbar.

### G) Service

Das Service-Hauptmenue ist passwortgeschuetzt. Sichtbar sind mindestens:

- Zeitprogramm Winter
- Filter
- Dauer Luftstufe 3
- Fehlerspeicher
- Geraete-Neustart

Ziel in HA: Servicefunktionen nur als bewusst geschuetzte Diagnose-/Konfigurationsaktionen. Ein Neustart-Button und schreibende Serviceparameter werden erst umgesetzt, wenn die Protokollbefehle eindeutig bekannt sind.

### Umsetzungsstatus der naechsten Funktionen

| Displayfunktion | HA-Umsetzung | Registerstatus |
|---|---|---|
| Raum-Solltemperatur | `number` `LG250 Raum-Solltemperatur` aktiviert | `Rd` ist als Raumsollwert definiert; Lesen/Schreiben muss am Geraet noch bestaetigt werden |
| Filter-Restlaufzeit | noch nicht produktiv aktiviert | `FH`/`FR` liefern Platzhalter; `FI` bleibt Testkandidat |
| Zeitprogramm Sommer/Winter | noch nicht produktiv aktiviert | Register und Schreibsequenz noch nicht identifiziert |
| Fehlerarchiv | noch nicht produktiv aktiviert | `ER` liefert aktuell den Fehlerstatus, nicht nachweislich das Archiv |
| Software-/Geraeteinformation | noch nicht produktiv aktiviert | `II` ist ein Identifikationskandidat, am Geraet noch nicht bestaetigt |

### HA-Zielstruktur

Die Display-Funktionen sollten in HA in diese Bereiche aufgeteilt werden:

| HA-Bereich | Entitaeten |
|---|---|
| Steuerung | Select Betriebsmodus, Select Lueftungsstufe, Switch Kuehlung, Waermepumpe, Zusatzheizung |
| Status | aktuelle Stufe, Betriebsart, Raumtemperatur, Drehzahlen, Rohstatus |
| Zeitplan | Sommer- und Winter-Zeitplan als Automationen oder Wochenplan |
| Wartung | Filter-Restlaufzeit, Filter-Reset-Button |
| Diagnose | Fehlerstatus, Fehlertext, Fehlerarchiv, ST/ER-Rohwerte |
| Systeminfo | Betriebsstunden, Solltemperatur, Geraet, Softwarestand |
| Service | Neustart und geschuetzte Parameter erst nach Protokollverifikation |

Diese Struktur ist die Arbeitsgrundlage fuer den weiteren Ausbau. Sicher implementiert sind zuerst Status und Lesen; Schreiben, Filterreset, Zeitprogramme und Servicefunktionen brauchen jeweils einen eigenen Protokolltest.

## 2) Zusatzcodes getestet, auf deiner Anlage nicht unterstuetzt

| Code | Erwartete Bedeutung | Intervall im Test | Ergebnis im Log | Status | Empfehlung |
|---|---|---|---|---|---|
| FI | Filter-Restlaufzeit | 2min | Antwort war wiederholt ??????. | nicht unterstuetzt | nicht verwenden |
| H1 | Betriebsstunden Stufe 1 | 2min | Antwort war wiederholt ??????. | nicht unterstuetzt | nicht verwenden |
| H2 | Betriebsstunden Stufe 2 | 2min | Antwort war wiederholt ??????. | nicht unterstuetzt | nicht verwenden |
| H3 | Betriebsstunden Stufe 3 | 2min | Antwort war wiederholt ??????. | nicht unterstuetzt | nicht verwenden |
| H4 | Betriebsstunden Stufe 4 | 2min | Antwort war wiederholt ??????. | nicht unterstuetzt | nicht verwenden |
| HL | Betriebsstunden Luefter gesamt | 2min | Antwort war wiederholt ??????. | nicht unterstuetzt | nicht verwenden |
| SN | Solar-Nutzen Laufzeit | 2min | Antwort war wiederholt ??????. | nicht unterstuetzt | nicht verwenden |

Hinweis zur Auswertung: Die Firmware verwirft diese Antworten korrekt als ungueltig numerisch und publiziert keinen Fake-Wert.

## 3) Relaisbits und bekannte Besonderheit

| Relais-Sensor | Gemapptes Bit | Beobachtung | Interpretation | Aktueller Zustand in YAML |
|---|---|---|---|---|
| Zusatzheizung | 2 | dauerhaft EIN | offenbar Steuer-/Freigabebit, nicht zwingend Hardware-Nachweis | deaktiviert |
| Erdwaermetauscher | 4 | dauerhaft EIN | offenbar Steuer-/Freigabebit, nicht zwingend Hardware-Nachweis | deaktiviert |

Deshalb sind diese beiden Entitaeten in der Nutzkonfiguration deaktiviert, um Fehlinterpretationen in Home Assistant zu vermeiden.

## 4) Anzeige und Rundung

Temperatur- und Spannungswerte werden mit einer Nachkommastelle publiziert. Falls in einer Lovelace-Karte ganze Zahlen erscheinen, rundet meist die Karte die Anzeige. Rohzustand in Entwicklerwerkzeugen zeigt den tatsaechlichen Wert.

## 5) Fazit fuer den Betrieb

Die aktive reduzierte Konfiguration ist stabil und fuer den Dauerbetrieb geeignet. Die unterstuetzten Codes liefern konsistente Werte, die nicht unterstuetzten Register sind bereinigt.

## 6) Home Assistant Namen (schnelle Referenz)

Hinweis: In HA kann sich die entity_id bei Umbenennungen aendern. Deshalb sind unten der sichtbare Name (stabil) und eine typische entity_id-Form angegeben.

### 6.1 Sensoren

| ESP-Code | Sichtbarer Name in HA | Domain | Typische entity_id |
|---|---|---|---|
| T1 | LG250 T1 Verdampfertemperatur | sensor | sensor.lg250_t1_verdampfertemperatur |
| T2 | LG250 T2 Kondensatortemperatur | sensor | sensor.lg250_t2_kondensatortemperatur |
| T3 | LG250 T3 Aussentemperatur | sensor | sensor.lg250_t3_aussentemperatur |
| T4 | LG250 T4 Ablufttemperatur Raum | sensor | sensor.lg250_t4_ablufttemperatur_raum |
| T5 | LG250 T5 Nach Waermetauscher Fortluft | sensor | sensor.lg250_t5_nach_waermetauscher_fortluft |
| NA | LG250 Drehzahl Abluft | sensor | sensor.lg250_drehzahl_abluft |
| NZ | LG250 Drehzahl Zuluft | sensor | sensor.lg250_drehzahl_zuluft |
| UA | LG250 Steuerspannung Abluft | sensor | sensor.lg250_steuerspannung_abluft |
| UZ | LG250 Steuerspannung Zuluft | sensor | sensor.lg250_steuerspannung_zuluft |
| RA | LG250 Rueckwaermzahl | sensor | sensor.lg250_rueckwaermzahl |
| LS | LG250 Aktuelle Luftstufe | sensor | sensor.lg250_aktuelle_luftstufe |
| L1 | LG250 Luftstufe 1 Sollwert | sensor | sensor.lg250_luftstufe_1_sollwert |
| L2 | LG250 Luftstufe 2 Sollwert | sensor | sensor.lg250_luftstufe_2_sollwert |
| L3 | LG250 Luftstufe 3 Sollwert | sensor | sensor.lg250_luftstufe_3_sollwert |
| ER | LG250 Fehlercode Leistungsteil Rohwert | sensor | sensor.lg250_fehlercode_leistungsteil_rohwert |

### 6.2 Fehler-Sensoren (automatisch aus error_polling)

| Bedeutung | Sichtbarer Name in HA | Domain | Typische entity_id |
|---|---|---|---|
| Fehlerbit | FEHLER | binary_sensor | binary_sensor.fehler |
| Fehlertext | FEHLER Text | text_sensor | text_sensor.fehler_text |

### 6.3 Relais-Sensoren (aktuell aktiv)

| Funktion | Sichtbarer Name in HA | Domain | Typische entity_id |
|---|---|---|---|
| Kompressor | LG250 Kompressor | binary_sensor | binary_sensor.lg250_kompressor |
| Bypass | LG250 Bypass | binary_sensor | binary_sensor.lg250_bypass |
| Vorheizregister | LG250 Vorheizregister | binary_sensor | binary_sensor.lg250_vorheizregister |
| Bedienteil aktiv | LG250 Bedienteil aktiv | binary_sensor | binary_sensor.lg250_bedienteil_aktiv |
| Bedienung via RS | LG250 Bedienung via RS | binary_sensor | binary_sensor.lg250_bedienung_via_rs |
| Warmwasser Nachheizregister | LG250 Warmwasser Nachheizregister | binary_sensor | binary_sensor.lg250_warmwasser_nachheizregister |
| Magnetventil | LG250 Magnetventil | binary_sensor | binary_sensor.lg250_magnetventil |

Deaktiviert in deiner Nutz-YAML: Zusatzheizung, Erdwaermetauscher.

## 7) HEX-Codes / Telegrammformat

### 7.1 Lese-Telegramm (Read)

Format (8 Byte):

EOT ADR ADR ADR ADR CMD1 CMD2 ENQ

Hex konstant:

- EOT = 04
- Adresse = 30 30 31 31 (ASCII "0011")
- ENQ = 05

Damit gilt fuer jeden Read-Code:

04 30 30 31 31 XX YY 05

Beispiel:

- T1 -> 04 30 30 31 31 54 31 05
- RA -> 04 30 30 31 31 52 41 05
- HL -> 04 30 30 31 31 48 4C 05

### 7.2 Aktive Codes inkl. CMD-HEX

| Code | CMD-ASCII | CMD-HEX | Voller Read-Frame |
|---|---|---|---|
| T1 | T1 | 54 31 | 04 30 30 31 31 54 31 05 |
| T2 | T2 | 54 32 | 04 30 30 31 31 54 32 05 |
| T3 | T3 | 54 33 | 04 30 30 31 31 54 33 05 |
| T4 | T4 | 54 34 | 04 30 30 31 31 54 34 05 |
| T5 | T5 | 54 35 | 04 30 30 31 31 54 35 05 |
| NA | NA | 4E 41 | 04 30 30 31 31 4E 41 05 |
| NZ | NZ | 4E 5A | 04 30 30 31 31 4E 5A 05 |
| UA | UA | 55 41 | 04 30 30 31 31 55 41 05 |
| UZ | UZ | 55 5A | 04 30 30 31 31 55 5A 05 |
| RA | RA | 52 41 | 04 30 30 31 31 52 41 05 |
| LS | LS | 4C 53 | 04 30 30 31 31 4C 53 05 |
| L1 | L1 | 4C 31 | 04 30 30 31 31 4C 31 05 |
| L2 | L2 | 4C 32 | 04 30 30 31 31 4C 32 05 |
| L3 | L3 | 4C 33 | 04 30 30 31 31 4C 33 05 |
| ER | ER | 45 52 | 04 30 30 31 31 45 52 05 |

### 7.3 Schreib-Telegramm (nur wenn enable_unsafe_writes: true)

Schreibtelegramm:

EOT ADR ADR ADR ADR STX CMD1 CMD2 DATA... ETX CHK

Die aktuelle Lüftungsstufen-Auswahl schreibt nicht direkt `LS`. Sie setzt das interne Statusbyte und schreibt dieses über `SW`, wie in der ursprünglichen WR3223-Komponente.

Beispielhafter Write-Frame für `SW`:

`04 30 30 31 31 02 53 57 DATA 03 CHK`

`CHK` ist XOR über `SW`, die Daten und `ETX`. Die Steuerung quittiert die Schreibanforderung mit einem einzelnen ACK oder NAK.

## 8) Vergleich zu Modbus

| Merkmal | LG040100-Protokoll (hier) | Modbus RTU |
|---|---|---|
| Frame-Start | EOT (04) oder STX im Antworttelegramm | kein dediziertes Startbyte, Timing-basiert |
| Adressierung | ASCII "0011" als 4 Byte | 1 Byte Slave-Adresse |
| Befehl | 2 ASCII-Zeichen (z. B. T1, RA) | Function Code (z. B. 03, 06, 10) |
| Datenmodell | semantische 2-Zeichen-Registercodes | numerische Registeradressen |
| Integritaet | XOR-Checksumme (bei Schreibtelegrammen/Antworten) | CRC16 |
| Transport | UART 9600, 7E1 | haeufig UART 8N1/8E1 |
| Kompatibilitaet | proprietaer | standardisiert |

Kurzfazit: Das ist kein Modbus, sondern ein proprietaeres ASCII-basiertes Protokoll. Ein Modbus-Client kann das nicht direkt lesen.

## 9) Ziel: Alles auslesen, was geht (Roadmap)

### 9.1 Bereits verfuegbar im Codebestand (Registerkandidaten)

AE, AA, Az, Aa, AR, AZ, AP, AN, AV, T1, T2, T3, T4, T5, T6, T7, T8, LS, L1, L2, L3, LD, Ld, EC, Es, ES, EW, EE, EA, ER, ST, SW, SP, Re, Rd, MD, RL, UZ, UA, NZ, NA, NM, CN, KM, ZH, ZE, WP, PA, II, RA, D1, D2, D3, E1, E2, E3, LR, SM, SN, DA, DE, S1, S2, S3, WS, Tf, Ta.

### 9.2 Priorisierte naechste Lesetests (nur Read, kein Write)

1. Temperatur/Prozess: T6, T7, T8
2. Sollwerte/Offsets: LD, Ld, SP, Re, Rd
3. Anlagenstatus: ST, MD, CN, II
4. Schutz-/Grenzwerte: NM, KM, D1, D2, D3, LR
5. EWT/Solar-Block: EC, Es, ES, EW, EE, EA, SM, DA, DE, S1, S2, S3, WS, Tf, Ta

### 9.3 Erfolgskriterien pro Code

- mindestens 3 gueltige Antworten ueber die Zeit
- keine Dauerantwort ??????.
- numerische Plausibilitaet oder stabiler Textstatus
- wenn unklar: als "fraglich" markieren statt produktiv aktivieren
