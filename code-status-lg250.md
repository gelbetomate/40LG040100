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

Manuelle Schreibtests wurden mit `enable_unsafe_writes: true` und `enable_rs_handshake: false` durchgefuehrt. Die Auswahl erreicht den Schreibpfad, aber die Steuerung antwortet auf `LS`, `MD` und `SW` mit `NAK`.

Die automatischen Startup-/Polling-Schreibvorgaenge fuer `SW` und `MD` wurden anschliessend aus den Komponenten entfernt. Manuelle Schreibaktionen bleiben grundsaetzlich aktiv. Nach dem Neustart waren keine wiederkehrenden automatischen `SW=0`- oder `MD=0`-Schreibversuche mehr im Log sichtbar.

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

Read-Write-Anforderung vom PC:

EOT ADR ADR ADR ADR CMD1 CMD2 DATA... ETX

Beispiel `LS=3`:

`04 30 30 31 31 4C 53 33 03`

Die Steuerung quittiert die Schreibanforderung mit einem einzelnen ACK oder NAK. Die Checksumme gehoert zu den Antworttelegrammen der Steuerung; sie wird nicht an die Schreibanforderung angehaengt. Dieses Format ist aus der externen WR3223-Protokollbeschreibung abgeleitet und muss auf der LG250 noch verifiziert werden.

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
