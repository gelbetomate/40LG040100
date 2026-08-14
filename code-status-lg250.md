# LG250 Code-Status (40LG040100)

Stand: 2026-08-14
Quelle: aktuelle Nutzkonfiguration, ESPHome-Logs und Feldtest auf deiner Anlage

## 0) Geräteidentifikation und elektrische Ausstattung laut Typenschild

Das fotografierte Typenschild gehört zur verwendeten Steuerungsplatine und nennt:

### 0.1 Identifikation

- **Type:** `40LG040100 V. 4.0`. Das ist die Typen- und Versionsbezeichnung der Steuerung. `V. 4.0` wird hier nicht automatisch als separater Firmwarestand interpretiert.
- **No:** `1409051`. Das ist die individuelle Nummer der Steuerungskomponente.

### 0.2 Spannungsversorgung

- **Power:** `AC 100-240 V, 50/60 Hz, 5 VA`.

Die Angabe beschreibt die Versorgung der Steuerungsplatine selbst. Die größeren Lasten der Lüfter und Heizregister werden nicht durch diese 5-VA-Logikversorgung erklärt, sondern über die auf dem Typenschild genannten Ausgänge beziehungsweise externe Leistungskomponenten geschaltet.

### 0.3 Eingänge

- **In:** `5 x KTY81`.

Die Platine besitzt fünf Eingänge für KTY81-Temperaturfühler. Das passt zu den fünf beobachteten Temperaturregistern `T1` bis `T5`. Die fachliche LG250-Zuordnung aus den Feldtests lautet derzeit `T1=Fortluft`, `T2=Zuluft`, `T3=Aussenluft`, `T4=Abluft` und `T5=Fortluft-Zusatzkanal`; die Typenschildangabe allein definiert nicht, welcher Fühler welchem Hermes-Code entspricht.

### 0.4 Ausgänge

- **Out:** `3 x DC 0...10 V`.
- **Out:** `AC 230 V, 6 A`.

Die drei 0-10-V-Ausgänge passen zu einer stufenlosen Ansteuerung von EC-Lüftern und weiteren analogen Stellgrößen. Die beobachteten Register `UA` und `UZ` entsprechen den beiden Luftweg-Steuerspannungen. Die konkrete Belegung des dritten 0-10-V-Ausgangs ist anhand des Typenschilds allein nicht bestimmt; Bypassklappe oder externes Heizregister bleiben hierfür Hypothesen.

Der 230-V-Ausgang kann netzgespeiste Komponenten schalten. Welche LG250-Funktion ihn im konkreten Gerät nutzt, muss aus `RL`-Readbacks und der Anlagenverdrahtung abgeleitet werden; das Typenschild beweist keine einzelne Zuordnung zu Bypass, Vorheizregister oder Zusatzheizung.

### 0.5 Sicherheitskennzeichnung

Das Doppelquadrat kennzeichnet Schutzklasse II beziehungsweise Schutzisolierung. Das CE-Zeichen steht für die auf dem Produkt erklärte Konformität mit den einschlägigen europäischen Anforderungen.

Die LG250 ist in dieser Anlage eine reine KWL-/Lüftungsanwendung ohne Verdampfer und ohne Kondensator. Bezeichnungen wie `Verdampfertemperatur` oder `Kondensatortemperatur` sind für diese Anlage daher fachlich falsch und dürfen nicht als LG250-Entity-Namen verwendet werden. Dass die Anlage ohne angeschlossenes Display in einen Standby-/Sicherheitszustand wechselt, stammt aus dem Feldtest und ist keine direkte Aussage des Typenschilds.

## 1) Aktive Sensor-Codes (Produktiv)

Diese Datei beschreibt die Feldtests der konkreten LG250-Anlage. Sie ist kein allgemeines Registerprofil fuer LG150, LG350 oder andere 40LG040100-Firmwarestaende. Generische Transport- und Parsinglogik bleibt im Component; Auswahl, Benennung, Skalierung und fachliche Ableitungen werden modellbezogen in YAML beziehungsweise Profilen festgelegt.

| Code | Funktion | Einheit | Intervall | Beobachtete Werte | Status | Plausibilitaet | Empfehlung |
|---|---|---|---|---|---|---|---|
| T1 | Fortlufttemperatur (Fortluft FO) | degC | 30s | 28.8 bis 29.0 | funktioniert | plausibel im KWL-Luftschema, durch Zewotherm-Unterlage gestuetzt | aktiv lassen |
| T2 | Zulufttemperatur (Zuluft ZU) | degC | 30s | 26.9 | funktioniert | plausibel im KWL-Luftschema, durch Zewotherm-Unterlage gestuetzt | aktiv lassen |
| T3 | Aussentemperatur (Aussenluft) | degC | 30s | 26.0 | funktioniert | plausibel und stabil | aktiv lassen |
| T4 | Ablufttemperatur Raum (Abluft) | degC | 30s | 26.9 bis 27.0 | funktioniert | plausibel und stabil | aktiv lassen |
| T5 | Nach Waermetauscher Fortluft (Fortluft) | degC | 30s | 0.0 | funktioniert | numerisch gueltig, fachlich anlagenseitig pruefen | aktiv lassen, Verlauf beobachten |
| NA | Drehzahl Abluft/Fortluftseite | rpm | 30s | ca. 1007 bis 1171 | funktioniert | plausibel, dynamisch zur Stufe passend | aktiv lassen |
| NZ | Drehzahl Zuluft | rpm | 30s | ca. 1245 bis 1261 | funktioniert | plausibel, dynamisch zur Stufe passend | aktiv lassen |
| UA | Steuerspannung Abluft | V | 60s | 31.0 | funktioniert | plausibel und stabil | aktiv lassen |
| UZ | Steuerspannung Zuluft | V | 60s | 35.0 | funktioniert | plausibel und stabil | aktiv lassen |
| RA | Rueckwaermzahl | % | 60s | 1.0 | funktioniert | numerisch stabil, fachlich sehr niedrig | aktiv lassen, spaeter verifizieren |
| LS | Aktuelle Luftstufe | Stufe | 30s | 2 | funktioniert | plausibel zu L1/L2/L3 | aktiv lassen |
| L1 | Luftstufe 1 Sollwert | % | 2min | 20 | funktioniert | plausibel | aktiv lassen |
| L2 | Luftstufe 2 Sollwert | % | 2min | 33 | funktioniert | plausibel | aktiv lassen |
| L3 | Luftstufe 3 Sollwert | % | 2min | 68 | funktioniert | plausibel | aktiv lassen |
| ER | Fehlercode Leistungsteil Rohwert | Code | 60s | 0 | funktioniert | gueltig, kein Fehler aktiv | aktiv lassen |
| Rd | Raum-Solltemperatur Anzeige | degC | 2min | Rohwerte `134..156`, vorlaeufig als `13.4..15.6 degC` skaliert | funktioniert lesend | Schreibtest `Rd=23` erhielt NAK; Skalierung am Bedienteil gegenpruefen | als Anzeige aktiv lassen |

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

Ein weiterer Feldtest bestaetigt den Zustandswechsel im Lesepfad: Die Anlage meldete zunaechst `LS=4` mit `Automatik - Grundlueftung` und spaeter `LS=2` mit `Manuell - Stufe 2`. Dazu wurden etwa `NZ=1246` beziehungsweise `NZ=917` und `NA=975` beobachtet. Die LS-basierte Statusableitung folgt damit dem realen Anlagenzustand und nicht einem optimistischen HA-Wunschwert.

`LD` ist laut Hermes-WP-Schnittstellenbeschreibung ein les-/schreibbarer Zuluft-Korrekturwert (Zuluft +/-). Der generische Component-Pfad ist vorhanden; fuer die LG250 wird er jetzt als Number `LG250 Zuluft-Korrektur (LD)` mit `-40..40 %` aktiviert. Auch hier gilt: Ein Write ist erst nach passendem Readback bestaetigt.

Der Feldtest `RL=6` setzt die Masken `2` und `4`. Nach der Hermes-RL-Tabelle entspricht das den Relais fuer Zusatzheizung und Erdwaermetauscher. Diese beiden Diagnosen sind deshalb in der produktiven YAML jetzt sichtbar; zuvor waren sie vorsichtshalber deaktiviert.

Die Werte `48` und `52` entsprechen `0b00110000` beziehungsweise `0b00110100`. Der einzige Unterschied ist Bit 4. Die Testfolge spricht dafuer, dass dieses Bit mit Sommer-/Winterbetrieb zusammenhaengt; das ist noch nicht unabhaengig bestaetigt. Bit 8 wurde in der Testreihe nicht beobachtet.

Die Klartextdiagnose darf deshalb Bit 16 nicht als "Automatik aktiv" ausgeben. `MO` liefert auf dieser Firmware weiterhin `??????.` und kann den Betriebsmodus nicht bestaetigen.

## 1.2 Schreibverhalten

Manuelle Schreibtests wurden mit `enable_unsafe_writes: true` durchgefuehrt. Die Steuerung antwortete auf die bisher getesteten `LS`, `MD`, `SW` und `RS`-Schreibversuche mit `NAK`. Die produktive YAML verwendet deshalb `enable_rs_handshake: false`; die Selects fuer Luftstufe und Betriebsmodus sind reine Anzeige.

Die automatischen Startup-/Polling-Schreibvorgaenge fuer `SW` und `MD` wurden aus den Komponenten entfernt. Schreibbar bleiben nur die durch die neue PDF belegten Sollwertpfade `L1`, `L2`, `L3` und `LD`; diese werden als Numbers angeboten. Nach dem Neustart waren keine wiederkehrenden automatischen `SW=0`- oder `MD=0`-Schreibversuche mehr im Log sichtbar.

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

Die Register `MO`, `BY`, `HP`, `HZ` sind in dieser PDF nicht aufgefuehrt. Das ist ein Hinweis auf eine abweichende Variante, beweist aber weder fehlende Lesbarkeit noch fehlende Schreibbarkeit auf der LG250. Antworten `??????.` werden deshalb als ungueltiger Readback dokumentiert; Schreibbarkeit muss separat mit einem passenden Datenformat und `ACK`/`NAK` getestet werden.

#### Schreibrechte laut WP-Schnittstellen-PDF

Die neu hinzugefuegte WP-Schnittstellen-PDF beschreibt dasselbe Telegrammformat, aber eine andere und fuer dieses Projekt entscheidende Registertabelle:

- `LS` ist **nur lesbar**.
- `MD` ist **nur lesbar** und hat die dokumentierten Werte `0=Sommer`, `1=Winter`, `2=Hand`, `3=Sommer Abluft`, `4=Plattenwaermetauscher`, `5=Abs Betrieb`.
- `WP` und `ZH` sind **nur lesbar**.
- `L1`, `L2`, `L3` und `LD` sind **lesbar und schreibbar**.
- `SW` und `RS` kommen in dieser Tabelle nicht vor.

Das erklaert die bisherigen Feldtests: `LS`, `MD`, `SW` und `RS` mit `NAK` sind kein Beleg fuer ein falsches Telegramm, sondern passen zu den dokumentierten Schreibrechten dieser Variante. Die bisherige `SW`-/RS-Handshake-Annahme wird fuer diese LG250-Schnittstelle verworfen. Das gilt nicht als allgemeiner Beweis, dass ein Register mit `??????.` niemals schreibbar ist.

Die PDF dokumentiert als Schreibbeispiel `L1=50`:

```text
04 30 30 31 31 02 4C 31 35 30 03 7B
```

Die `L1`-/`L2`-/`L3`-Schreibfunktionen sind im Connector bereits vorhanden und wurden in der YAML jetzt als drei Numbers mit dem empirisch bestaetigten Bereich `0..100 %` aktiviert. Der Feldwert `L3=68` zeigt, dass die zuvor aus einer anderen Registerliste uebernommene Begrenzung `3..40` fuer diese LG250 nicht verwendet werden darf. Diese Werte aendern die Sollwerte der einzelnen Stufen; sie starten keine Stufe unmittelbar. Die aktuelle Stufe bleibt ueber `LS` lesbar.

Der erste Feldtest mit der neuen Konfiguration war erfolgreich:

- Home Assistant schrieb `L1=21`.
- Gesendeter Frame: `04 30 30 31 31 02 4C 31 32 31 03 7D`.
- Die XOR-Pruefsumme `0x7D` stimmt.
- Die LG250 antwortete mit `ACK` (`0x06`).
- Home Assistant veroeffentlichte anschliessend `LG250 Luftstufe 1 Sollwert = 21`.
- `LS` blieb unveraendert bei `4`; der Write aendert also den Sollwert, nicht die aktuell aktive Betriebsstufe.

Ein zweiter Feldtest bestaetigte den Telegrammweg auch fuer einen hohen Wert: `L3=82` wurde mit `ACK` (`0x06`) bestaetigt. Weitere Tests mit `L3=80`, `L3=79`, `L3=92`, `L3=83`, `L3=76`, `L3=94` und `L3=88` erhielten ebenfalls `ACK`, aber der anschliessende Readback lieferte jeweils wieder `L3=68`. In einem erweiterten Test wurden auch `L2=44` und `L1=33` mit `ACK` bestaetigt; die Readbacks blieben bei `L2=33` beziehungsweise `L1=20`. Der Controller bestaetigt damit den Transport beziehungsweise die Telegrammgueltigkeit, uebernimmt die neuen Sollwerte in der aktuellen Betriebsart aber nicht dauerhaft. Die Number-Komponente liest deshalb nach `ACK` das Register erneut und veroeffentlicht nur den bestaetigten Readback-Wert.

Ein anschliessender Schreibtest mit `Rd=23` wurde mit `NAK` abgelehnt. Das schliesst den Lesepfad nicht aus: `Rd` kann auf dieser Anlage gelesen werden, ist aber nicht als schreibbarer Befehl bestaetigt. Ein Readback von `154` wird im LG250-YAML vorlaeufig mit `0.1` multipliziert und als `15.4 degC` angezeigt, weil der Rohwert sonst als unmoegliche `154 degC` erscheinen wuerde. Diese Skalierung muss noch gegen den am Bedienteil angezeigten Sollwert verifiziert werden. `Rd` bleibt ein schreibgeschuetzter Sensor und wird nicht als Number angeboten. `L1`, `L2` und `L3` bleiben als durch `ACK` bestaetigte Schreibpfade aktiv.

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
| 0x82 | 130 | Geraetefehler, genaue Bedeutung fuer LG250 offen |
| 0x04 | 4 | HD-Fehler |
| 0x85 | 133 | Vorheizregister-Fehler |
| 0x3y | 49-56 | Unterbrechung Sensor y (y=1 T1, y=2 T2, y=3 T3, y=5 T5, y=6 T6, y=7 EWT, y=8 VHR) |
| 0x1y | 17-24 | Kurzschluss Sensor y (gleiche y-Zuordnung) |

Der `ER`-Sensor hat jetzt eine Klartextdiagnose (`LG250 ER Fehlerdiagnose`), die alle obigen Codes dekodiert.

#### Temperatursensoren T1-T6 laut PDF

Die bisher verwendeten T1-/T2-Labels `Verdampfertemperatur` und `Kondensatortemperatur` passen nicht zur LG250-Wohnraumlüftung ohne Kältekreis. Das Typenschild `40LG040100 V. 4.0` und die Zewotherm-LG250-Unterlage stützen die Einordnung als KWL-Gerät mit den vier primären Luftströmen Außenluft, Abluft, Zuluft und Fortluft. Zusammen mit den Sommermesswerten ergibt sich die Zuordnung `T1=Fortluft (FO)` und `T2=Zuluft (ZU)`.

Die derzeit belastbare Zuordnung lautet:

| Register | Offizielle Bedeutung |
|---|---|
| T1 | Fortlufttemperatur (Fortluft FO) |
| T2 | Zulufttemperatur (Zuluft ZU) |
| T3 | Aussentemperatur |
| T4 | Ablufttemperatur (Raumtemperatur) - nicht in der PDF explizit, aber bestaetigt durch Feldtest |
| T5 | Temperatur nach Waermetauscher, optionaler Fortluft-Zusatzkanal |
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

### 1.2.4 Regel fuer ungueltige Readbacks

Ein Readback `??????.` bedeutet nur: Der aktuelle Leseversuch hat keinen numerisch verwertbaren Wert geliefert. Es bedeutet nicht automatisch, dass das Register nicht schreibbar ist. Fuer jeden moeglichen Write muessen Registerbeschreibung, Datenformat, Wertebereich und die echte Antwort (`ACK` oder `NAK`) separat bewertet werden. Bis dahin bleiben solche Befehle Testkandidaten und werden nicht produktiv als schreibbare Bedienelemente angeboten.

### 1.2.5 Aktueller Betriebsstatus und Setpoints

`L1`, `L2` und `L3` sind Sollwerte der drei Luftstufen. Ein erfolgreicher Write wie `L3=82` aendert nicht die aktuell laufende Stufe. `LS=4` bleibt deshalb korrekt als `Automatik / Grundlueftung` sichtbar, solange die Anlage selbst in der Grundlueftung laeuft.

Die bisherige Anzeige `AUS` war dagegen ein UI-Fehler: Sie wurde aus dem internen `SW`-Holder abgeleitet, dessen Readback auf dieser Firmware ungueltig ist und deshalb auf dem Defaultwert 0 blieb. Die zwischenzeitliche Template-Auswahl war ebenfalls falsch modelliert, weil sie als interaktiver Select eine Auswahl zuliess. Die Produktiv-YAML verwendet fuer den bestaetigten `LS`-Zustand jetzt ausschliesslich den Textsensor `LG250 Betriebsstatus Detail`; der Betriebsmodus wird nicht als `AUS` aus einem unbestaetigten `MD`-Holder dargestellt.

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
| T1 | LG250 T1 Fortlufttemperatur | sensor | sensor.lg250_t1_fortlufttemperatur_fortluft_fo |
| T2 | LG250 T2 Zulufttemperatur | sensor | sensor.lg250_t2_zulufttemperatur_zuluft_zu |
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

Die produktive LG250-YAML verwendet keine schreibende Lüftungsstufen-Auswahl. `LS` ist auf der getesteten PC-Schnittstelle ein Readback der aktuell durch das BDE gesetzten Stufe. Die frühere SW-basierte Auswahl ist deaktiviert, weil `SW`-Readback und `RS`-Handshake auf dieser LG250 nicht funktionieren.

Die getesteten Sollwert-Writes für `L1`, `L2` und `L3` werden zwar mit `ACK` quittiert, bleiben aber nach dem Readback bei den alten Werten (`L1=20`, `L2=33`, `L3=68`). Ein `ACK` allein ist deshalb keine Bestätigung der funktionalen Übernahme.

Beispielhafter Write-Frame für einen dokumentierten `L1`-Write:

`04 30 30 31 31 02 4C 31 DATA 03 CHK`

`CHK` ist XOR über Kommando, Daten und `ETX`. Die Steuerung quittiert die Schreibanforderung mit einem einzelnen ACK oder NAK; die Komponente liest danach das Register erneut und veröffentlicht nur den Readback-Wert.

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

## 10) Display-/PC-Schnittstellen und Gesamtfahrplan

Das BDE-Comfort-Display hängt an einer separaten RS485-Schnittstelle. Dieses Projekt verwendet ausschließlich die PC-Parametrierungsschnittstelle über RS232 mit dem Hermes-Zweizeichenprotokoll. Ein RS485-Sniffer ist daher nicht zwingend erforderlich: Displayänderungen können über die resultierenden RS232-Readbacks korreliert werden.

### 10.1 Bereits bestätigte Verhaltensdaten

- `LS=4` wird als `Automatik - Grundlüftung` erkannt.
- Eine Displayänderung kann `LS=4` auf `LS=2` ändern; die Statusanzeige meldet danach `Manuell - Stufe 2`.
- `Rd` ist lesbar und liefert LG250-Rohwerte wie `134..156`; im LG250-YAML werden sie vorläufig mit `0.1` als `13.4..15.6 degC` dargestellt.
- `ER=0`, `ST=48`, `RL=6`, `NA/NZ`, `UA/UZ`, `F1/F2` und die Luftwegtemperaturen liefern verwertbare Readbacks.
- `L1/L2/L3` erhalten bei Writes `ACK`, aber der anschließende Readback bleibt bei `20/33/68`. Diese Writes sind daher derzeit funktional nicht bestätigt.
- Kontrollierter Display-angeschlossener Test am 14.08.2026: Bei `LS=2`, `ST=48`, `RL=6`, `UA=3.1 V`, `UZ=3.5 V` und `ER=0` wurde `L2=40` gesendet. Der Controller antwortete mit `ACK`, der unmittelbare Readback blieb jedoch `L2=33`. Damit ist der L2-Schreibframe formal korrekt quittiert, aber auch im aktiven manuellen Betrieb funktional unwirksam.
- Beim Feldtest am 14.08.2026 mit abgestecktem BDE-Display wechselte die Anlage in einen Aus-/Sicherheitszustand: `LS=0`, `NA=0`, `NZ=0`, `UA=0`, `UZ=0`, `RL=0`, `ST=16` und `ER=0`. Das zeigt, dass die Displayverbindung für den normalen Betrieb relevant sein kann oder dass der Controller bei fehlendem BDE-Bus die Ausgaenge abschaltet. Es beweist noch keine PC-Schreibsperre.

### 10.2 Was für vollständige HA-Steuerung fehlt

1. Eine wirksame PC-RS232-Sequenz für die aktuelle Luftstufe und Betriebsmodi.
2. Die Freigabe-, Speicher- oder Folgeaktion, die nach einem formal quittierten Write möglicherweise noch erforderlich ist.
3. Ein belastbarer PC-Schreibpfad für Raum-Sollwert `Rd`.
4. Sommer-/Winterbetrieb, Aus, Automatik und manuelle Stufen als reproduzierbare Steueraktionen.
5. Zeitprogramme für Sommer/Winter einschließlich Aktivierung und Speicherung.
6. Filter-Restzeit und Filter-Reset.
7. Fehlerhistorie mit Datum/Uhrzeit und Fehlertexten.
8. Echte Betriebsstundenregister für Stufen, Grundlüftung, Gesamtbetrieb, Vorheizung, EWT und Bypass.
9. Servicefunktionen wie Neustart und geschützte Parameter.

### 10.3 Methodik ohne RS485-Sniffer

Für jede einzelne BDE-Aktion werden vor und nach der Änderung über RS232 die folgenden Werte verglichen: `LS`, `ST`, `RL`, `Rd`, `L1-L3`, `NA`, `NZ`, `UA`, `UZ` und `ER`. Dazu werden Bedienaktion, Uhrzeit, sichtbarer Vorher-/Nachher-Zustand und die Readback-Änderungen dokumentiert.

Diese Methode kann bestätigen, welcher Anlagenzustand durch das Display gesetzt wurde und ob ein PC-Kommando denselben Zustand reproduziert. Sie kann nicht den ursprünglichen RS485-Schreibframe oder eine interne BDE-Speichersequenz rekonstruieren. Für eine produktive Schreibfunktion sind deshalb sowohl ein reproduzierbarer PC-Write als auch ein passender Readback erforderlich.

### 10.4 Architekturgrenze

Die C++-Komponente bleibt für Transport, Framing, Parsing, Checksummen und generische Read-/Write-Requests modellneutral. LG250-spezifische Registerauswahl, Skalierung, Luftwegbezeichnungen, Statusableitungen und Schreibrechte bleiben in YAML beziehungsweise Modellprofilen. Erkenntnisse aus der LG250 dürfen nicht ohne Feldtest als allgemeine LG150-/LG350-Semantik übernommen werden.

### 10.5 Vergleich mit Schwörer WGT / WR3223

Die Projekte `kaepse/schwoerer-wgt-wr3223` und `schmurgel-tg/esphome-components` verwenden ebenfalls einen Hermes-WR3223-Controller und dasselbe BDE-Konzept. Daraus ergeben sich folgende prüfbare Vergleichshypothesen:

- Die Lüftungsstufen-Sollwerte `L1`, `L2` und `L3` werden dort ebenfalls als Prozentwerte behandelt. Das bestätigt die Darstellung der LG250-Number-Entities als Prozentwerte, beweist aber nicht den zulässigen Wertebereich dieser konkreten LG250.
- Beim Schwörer-WGT wird ein regelmäßiges `SW`-Status-/Freigabekommando beschrieben. Ohne diese Kommunikation kann der Controller nach ungefähr 20 Sekunden in einen eingeschränkten Defaultzustand wechseln. Zusätzlich werden gespeicherte Statuswerte erst geschrieben, wenn das Bedienteil nicht aktiv ist.
- Die fremde Komponente bietet explizite Save-/Restore-Aktionen. Das ist ein Hinweis auf eine mögliche Folge- oder Speicheraktion, aber kein Nachweis, dass die LG250 dieselben Befehle oder dieselbe Reihenfolge verwendet.

Für die LG250 darf daraus derzeit nur folgender Test abgeleitet werden:

1. BDE angeschlossen lassen und am Display `LS=2` einstellen.
2. Einen einzelnen Write auf `L2` ausführen, zum Beispiel von `33` auf `40`, und ACK sowie anschließenden Readback protokollieren.
3. Danach `LS`, `L2`, `NA/NZ`, `UA/UZ`, `ST`, `RL` und `ER` vergleichen. Ein unveränderter `L2`-Readback bleibt ein fehlgeschlagener Funktionstest, auch wenn der Write ACK erhält.
4. Erst wenn ein wirksamer L2-Write nachgewiesen ist, eine mögliche Speicher-/Folgeaktion untersuchen.

Die Schwörer-Sequenz wird nicht automatisch aktiviert: Auf der getesteten LG250 erhielt `RS=1` ein `NAK`, und ein `SW`-Readback ist ungültig. Außerdem zeigte der LG250-Test mit abgestecktem Display `LS=0`, `RL=0` und abgeschaltete Ausgänge statt des im Schwörer-Projekt beschriebenen eingeschränkten Betriebs. Das Fremdverhalten ist daher eine nützliche Vergleichshypothese, aber keine übertragene LG250-Funktion.

### 10.6 Herstellernahe WR3223-Erfahrungen: RESETCode und dauerhafte Parameter

Weitere herstellernahe beziehungsweise praxisbasierte WR3223-Dokumentationen liefern eine neue Arbeitshypothese für das bisherige Schreibverhalten:

- In der [openHAB-WR3223-Diskussion](https://community.openhab.org/t/wr3223-ventilation-controller-schworer-haus/11086) wird für Schreibzugriff das Abziehen des Bedienteil-Steckers `X1` beschrieben.
- Die [Symcon-WR3223-Diskussion](https://community.symcon.de/t/abfragen-und-regeln-der-lueftungssteuerung-wr-3223-von-hermes-electronic/35008) bestätigt die gemeinsame Hermes-WR3223-Protokollfamilie, 9600 Baud, 7 Datenbits, gerade Parität und die ASCII-Steuerzeichenstruktur.
- In der [Anlagenparameter-Dokumentation](https://hendrich.org/blogs/entscheidungshilfe-luftungsheizung/anlagenparameter/) wird beschrieben, dass vor der Parameteränderung `RESETCode=1` gesetzt werden muss. Die dort gezeigten Tabellen unterscheiden zwischen Messwerten und Parametern und enthalten auch `Luftstufe1`, `Luftstufe2` und `Luftstufe3` als Prozentwerte.

Das passt als Hypothese zu `L2=40 -> ACK -> Readback L2=33`: Der Frame wird auf Transportebene akzeptiert, aber der Parameter wird ohne eine Freigabe-/Schreibschutzsequenz nicht dauerhaft übernommen. Es ist jedoch nicht bewiesen, dass `RESETCode` bei der Pichler-LG250 denselben Hermes-Befehl oder dieselbe Bedeutung hat. Der Name ist in der aktuell bekannten zweistelligen Registerliste dieses Projekts nicht enthalten.

Der Displaybefund schränkt die Übertragung zusätzlich ein: Bei der LG250 führte das Abziehen des BDE zu `LS=0`, `RL=0`, `ST=16` und abgeschalteten Ausgängen. Deshalb darf `X1` nicht erneut als normaler Schreibtest abgezogen werden, solange kein sicherer Wiederanlauf- und Rückfallplan besteht. Das kann eine Watchdog-/Freigabefunktion sein, ist durch die bisherigen Readbacks aber noch nicht als konkrete Firmwareimplementierung bewiesen.

#### Priorisierter Test für RESETCode

1. Die Hermes-/WR3223-Unterlagen und vorhandenen Community-Implementierungen nach einer exakten Register- oder Frame-Zuordnung für `RESETCode` durchsuchen.
2. Prüfen, ob der Wert als zweistelliges Hermes-Kommando, als Teil eines Parameterframes oder nur über das BDE-Protokoll existiert.
3. Erst nach bestätigter Zuordnung einen einzelnen, reversiblen Test mit dem bestehenden Readback-Schutz ausführen.
4. Erfolg nur bei `ACK` plus passendem Readback und anschließend stabiler Wiederholungslesung annehmen.

Bis dahin bleiben `L1`, `L2` und `L3` formal quittierte, aber funktional nicht bestätigte Writes. Die verwandten WR3223-Quellen enthalten außerdem Wärmepumpen-/Kältekreisparameter wie `VerdTemp` und `KondTEMP`; diese gelten nicht als Beleg dafür, dass die konkrete LG250-Anlage einen Verdampfer oder Kondensator besitzt.
