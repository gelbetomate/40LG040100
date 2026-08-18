# LG250 Code-Status (40LG040100)

Stand: 2026-08-18
Quelle: aktuelle Nutzkonfiguration, ESPHome-Logs und Feldtest auf deiner Anlage

## Abschlussstand: produktiver LG250-Einsatz nur lesend

Die aktive Konfiguration `lg250-esp.yaml` wurde am 2026-08-18 bewusst auf bestätigte passive Readbacks reduziert. Sie sendet keine Steuer-, Setpoint-, Reset-, Relais-, Save- oder RS-Handshake-Schreibtelegramme. Die vollständige vorherige Testkonfiguration bleibt als `lg250-esp-tested.yaml` erhalten.

Der Hermes-Transport und mehrere Lesewerte sind belastbar, aber kein funktionaler PC-Schreibpfad ist bestätigt: `L1`, `L2` und `L3` erhielten bei Tests zwar `ACK`, lieferten aber stets den unveränderten Readback; `Rd`, `RS`, `SW`, `LS` und `MD` waren abgelehnt oder nicht als schreibbar nutzbar. Ohne passenden Readback und dauerhafte Zustandsänderung zählt kein Write als erfolgreich.

Damit endet die aktive Suche nach einer Schreibfreigabe für diese konkrete LG250-Installation. Weiterarbeit ist willkommen, wenn sie neue überprüfbare Evidenz bringt: aufgezeichnete Telegramme der Pichler-PC-Software oder des Bedienteilbusses, eindeutig identifizierte Adapteranschlüsse, herstellerspezifische Dokumentation oder eine reproduzierbare Sequenz mit persistierendem Readback. Vermutete Reset-, Save-, Watchdog- oder Relaisbefehle werden nicht blind an der Anlage getestet.

## 0) Geräteidentifikation und elektrische Ausstattung laut Typenschild

Das fotografierte Typenschild gehört zur verwendeten Steuerungsplatine und nennt:

### 0.1 Identifikation

- **Type:** `40LG040100 V. 4.0`. Das ist die Typen- und Versionsbezeichnung der Steuerung. `V. 4.0` wird hier nicht automatisch als separater Firmwarestand interpretiert.
- **No:** `1409051`. Das ist die individuelle Nummer der Steuerungskomponente.

### 0.1.1 Zusatzkennzeichnung des Leistungsteils beziehungsweise DESIGN-Adapters

Das neu bereitgestellte Foto eines Typaufklebers liefert eine weitere Hardwarekennung:

- **Baugruppenbezeichnung:** wahrscheinlich `080DESIGNBOARD` (die letzte Lesung des unscharfen Fotos ist bei `BOARD/BOAD` nicht vollständig sicher).
- **Version:** `1.2`.
- **Seriennummer:** `1407524`.
- **Zusatzangabe Bedienteil:** `12345`.

Die Nummer `1407524` ist damit als individuelle Seriennummer einer weiteren beziehungsweise anders gekennzeichneten Baugruppe dokumentiert. Sie ersetzt nicht die bereits bekannte Seriennummer `1409051` des Typenschilds der Steuerung, sondern muss einer konkreten Platine oder Adapter-/Leistungsteilbaugruppe zugeordnet werden. `Version 1.2` ist eine Baugruppen-/Hardwareversion; daraus wird kein Firmwarestand des Hermes-Controllers abgeleitet.

Die Bezeichnung `080DESIGNBOARD` passt fachlich zum installierten `BT-M1 DESIGN` beziehungsweise zu dessen Leistungsteil-/Bedienteilfamilie und stärkt die Zuordnung des Fotos zur DESIGN-Anlage. Sie beweist allein weder einen Modbus-Transceiver noch eine Hermes-/Modbus-Protokollübersetzung.

Die Angabe `Bedienteil 12345` bleibt vorläufig unklar. In den mitgelieferten BACnet/EDE-Dateien wird `12345` mehrfach als Objektinstanz beziehungsweise Geräte-ID verwendet; es ist daher möglich, dass es sich hier um eine Dokumentations- oder Standardnummer und nicht um die echte Seriennummer des Bedienteils handelt. Für eine sichere Bedienteilidentifikation wären ein schärferes Etikett, die Rückseite des `BT-M1 DESIGN` oder ein Eintrag aus der Pichler-Software erforderlich.

### 0.1.2 Bewertung der Gateway-Hypothese zum `080DESIGNBOARD`

Die vorliegende Gemini-Einschaetzung beschreibt folgende moegliche Architektur:

```text
BT-M1 DESIGN --(moeglicherweise RS485/Modbus)--> 080DESIGNBOARD
080DESIGNBOARD --(moeglicherweise Hermes)--> 40LG040100
```

Diese Architektur ist als Arbeitshypothese interessant, aber aktuell nicht als technische Tatsache bestaetigt. Gesichert ist nur:

- Das konkrete Etikett nennt wahrscheinlich `080DESIGNBOARD`, Version `1.2` und Seriennummer `1407524`.
- Die LG250-Anleitung beschreibt eine Bedieneinheit beziehungsweise einen Adapter und eine RS485-Verbindung im Bedienteilkontext.
- Die separate `08KNXGAC_LS_ConfigTool.wz8861` beschreibt ein Weinzierl-Modbus-RTU-Gateway mit `19200`, gerader Paritaet und einem offiziellen numerischen LS-Modbus-Datenmodell.
- Der beobachtete PC-Anschluss dieser Anlage verwendet dagegen Hermes mit `9600 7E1` und Zweizeichenbefehlen.

Nicht belegt sind derzeit:

- dass das `080DESIGNBOARD` auf seiner Displayseite Modbus RTU spricht;
- dass diese Modbusseite mit `19200 8N1` arbeitet. Das vorliegende Gateway-Mapping ist `19200 8E1`, nicht `8N1`;
- dass das DESIGN-Display selbst Modbus und nicht ein Pichler-spezifisches Protokoll verwendet;
- dass das Board Hermes-Anfragen aktiv in Modbus-Anfragen uebersetzt oder umgekehrt;
- dass ein permanentes Hermes-Keep-alive oder ein Hardware-Watchdog vom Adapter erzeugt wird;
- dass Schreibwerte dadurch in ein EEPROM uebernommen werden;
- dass die Beispielbytes `04 30 30 31 31 02 4C 53 32 ...` ein gueltiges LG250-Hermes-Schreibtelegramm darstellen. Das bekannte Hermes-Schreibformat benoetigt unter anderem `STX`, Daten, `ETX` und eine passende XOR-Pruefsumme; die gezeigte Folge ist dafuer unvollstaendig.

Die KNX-/BACnet-Dateien beweisen den Modbus-Pfad des jeweiligen Gateways. Sie sind kein Mitschnitt der Leitung zwischen `BT-M1 DESIGN`, `080DESIGNBOARD` und Leistungsteil. Auch die Tatsache, dass die Anlage ohne angeschlossenes Display in `LS=0`, `RL=0` und ausgeschaltete Ausgaenge wechselt, beweist noch keinen Watchdog; sie kann ebenso eine BDE-Kommunikations- oder Freigabelogik des Leistungsteils bedeuten.

#### Konsequenz fuer eine Bridge

Ein passives Mithoeren auf der vermuteten Display-/Adapterleitung koennte die Hypothese pruefen, ist aber erst nach Identifikation der konkreten Klemmen und Pegel sinnvoll. Ein RS485-Transceiver darf nicht anhand des `08KNXGAC`-Handbuchs direkt an die Anlage angeschlossen werden: Dessen Klemmenbelegung, Abschlusswiderstand, Baudrate und Paritaet gelten zunaechst nur fuer das Weinzierl-Gateway.

Ein USR-RS485-Gateway oder MAX485 am vermuteten Displaybus darf deshalb nicht einfach mit `19200 8N1` als Modbus-Master aktiv senden. Ein aktiver zweiter Master koennte mit dem vorhandenen Display oder Adapter kollidieren. Der erste sichere Test waere ein hochohmiger passiver Mitschnitt beziehungsweise eine Messung mit galvanisch geeigneter, fuer RS485 vorgesehener Hardware. Erst wenn echte Modbus-Frames mit Slave-Adresse, Function Code und CRC beobachtet wurden, koennen die LS-Modbusadressen fuer diesen Bus verwendet werden.

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

### 0.6 Produktdatenblatt LG 250 System VENTECH und Bedienteilaufbau

Die zusätzlich bereitgestellten Pichler-Datenblattseiten beschreiben das Gerät als kompaktes KWL-Gerät `LG 250, System VENTECH`:

- radiale EC-Energiesparventilatoren mit Konstant-Volumenstromregelung
- Gegenstrom-Wärmetauscher mit automatischem 100-%-Bypass
- Luftleistungsbereich etwa `80..250 m3/h` bei externer Druckerhöhung von `50 Pa`
- Außenluftkassettenfilter F7 und Abluftkassettenfilter G4
- optionales internes oder externes PTC-Elektroheizregister
- drei wählbare Bedieneinheiten: `MINI`, `KOMFORT` und `DESIGN`
- zentrale Bedieneinheit `BT-M1 DESIGN` mit monochromem vollgrafischem TFT, Wochenzeitschaltung, Betriebs-/Laufzeitzählern, MicroSD-Steckplatz und RS485-Schnittstelle zur Konfiguration beziehungsweise zum Auslesen
- integrierte Filterüberwachung mit zeitgesteuerter Meldung „Filterwechsel“ am Display
- Filterwechsel ohne Werkzeug möglich
- automatisch arbeitende Frostschutzschaltung für den Wärmetauscher
- integrierter 100-%-Bypass zur Umgehung des Wärmetauschers im Sommerbetrieb
- optionale Nachheizung zur zusätzlichen Anhebung der Raumtemperatur

Für die dokumentierte LG250-Anlage ist das `BT-M1 DESIGN`-Display angeschlossen. Zwischen dem Display und der RS485-Leitung befindet sich zusätzlich ein Pichler-Display-Converter beziehungsweise Bedienteiladapter. Das Datenblatt beschreibt diesen Adapter als Konverter der Kommunikationsschnittstelle des Leistungsteils auf den RS485-Bus der Teilnehmer mit Echtzeituhr und Batteriepufferung.

Die genaue Rolle des konkreten Converters in dieser Installation ist noch offen. Er kann Pegel, galvanische Trennung, Buskopplung, Teilnehmeradressierung oder zusätzliche Zeit-/Bedienteilfunktionen übernehmen. Der Converter ist deshalb für die Interpretation der Display-/RS485-Kommunikation relevant, aber nicht automatisch Teil der hier angeschlossenen PC-Parametrierungsschnittstelle. Unser ESP32 hängt weiterhin an der beobachteten Hermes-PC-Schnittstelle über RS232. Ohne Typenschild, Schaltplan oder Messung an beiden Converter-Seiten darf aus dem Converter keine direkte RESET-, BDE- oder RS-Schreibsequenz abgeleitet werden.

### 0.7 Raumtemperatur und optionaler Elektro-Lufterhitzer

Das zusätzliche Datenblattkapitel „Mit externem Elektrolufterhitzer“ beschreibt eine optionale Ausbaustufe. Für die konkrete Anlage ist festgehalten: Es ist kein externer Elektro-Lufterhitzer vorhanden. Aussagen zu zweistufiger Nachheizung, konstanter Zulufttemperatur von `21 °C`, Schaltstufen und Mindestpausen gehören daher nicht zum aktiven Anlagenaufbau und dürfen nicht als Erklärung für die aktuellen LG250-Readbacks verwendet werden.

Das Datenblatt beschreibt außerdem, dass Sollwert und Erfassung der Raumtemperatur bei den Bedieneinheiten `KOMFORT` und `DESIGN` über einen integrierten Raumtemperaturfühler der Bedieneinheit erfolgen. Das passt zum installierten `BT-M1 DESIGN`: Die am Display angezeigte Raumtemperatur stammt wahrscheinlich vom Display beziehungsweise seinem integrierten Raumfühler und nicht von einem separat identifizierten KTY81-Luftwegfühler der Leistungsteilregister `T1` bis `T5`.

Für die Protokollanalyse müssen deshalb drei Dinge getrennt bleiben:

- Raum-Isttemperatur: wahrscheinlich vom `BT-M1 DESIGN`-Raumfühler geliefert.
- Raum-Sollwert am Display: fachlich eine Bedienteil-/Komforteinstellung.
- Hermes-Register `Rd`: auf dieser LG250 bisher nur als Rohwert `134..156` beobachtet; die Zuordnung zum angezeigten Raum-Sollwert ist nicht bestätigt. Die frühere Darstellung `14.6 °C` aus `Rd=146` wurde deshalb entfernt.

### 0.8 Geräteaufbau laut Betriebs- und Montageanleitung

Die bereitgestellte Seite 15 nennt beziehungsweise zeigt folgende Baugruppen des LG250 VENTECH:

- `1a`: Bedieneinheit Typ `DESIGN` beziehungsweise `1`: Bedieneinheit Typ `KOMFORT`
- `2`: Bedieneinheit Typ `MINI`
- `3`: Leistungsteil
- `4`: Verbindungsleitung zur Bedieneinheit, Typ `Y(ST)Y 2 x 2 x 0,64`, geschirmt
- `5`: Außenluftfilterkassette F7, optional Pollenfilter F9
- `6`: Abluftfilterkassette G4
- `7`: Gegenstromwärmetauscher
- `8`: Kondensatablauf
- `9`: Frostschutzheizung mit PTC-Niedertemperatur-Vorheizregister, optional
- `10`: Bypassklappe mit elektromotorischem Stellantrieb
- `11`: Zuluftventilator
- `12`: Abluftventilator
- `13`: Frontdeckel mit Griffschraubverschluss
- `14`: Luftleitungen beziehungsweise Geräteanschlüsse
- `15`: Kabeldurchführungen

Für die konkrete Anlage sind daraus insbesondere drei Punkte wichtig: Das optionale PTC-Vorheizregister ist nicht mit einem vorhandenen Elektro-Lufterhitzer gleichzusetzen; der Wärmetauscher und die motorische Bypassklappe gehören dagegen zum dokumentierten VENTECH-Gerätekonzept. Die Abbildung beschreibt den Serienaufbau und beweist nicht allein, welche optionalen Baugruppen in deinem konkreten Gerät bestückt oder elektrisch angeschlossen sind.

### 0.9 Weitere Betriebs- und Montagehinweise aus dem Datenblatt

Die Detailbeschreibung ergänzt folgende Punkte:

- Die Bedieneinheiten `KOMFORT` und `DESIGN` zeigen Betriebszustände und Systemwerte wie Betriebsart, Lüfterstufe, Temperaturen, Filterwechsel und Störungen. Bei `DESIGN` werden diese Informationen im Klartext mit Status- und Störmeldeanzeigen dargestellt.
- `KOMFORT` und `DESIGN` besitzen einen integrierten Raumtemperaturfühler. Zusätzlich können dort individuelle Einstellungen sowie bei Servicearbeiten Parameter vorgenommen werden.
- Die Betriebsart kann automatisch nach Zeitprogramm oder manuell gewählt werden. Das bestätigt die fachliche Bedeutung der Displayzustände, ersetzt aber keine bestätigte Hermes-Schreibsequenz für `LS` oder `MD` auf dieser LG250.
- Das Leistungsteil kann laut Beschreibung über die Bedieneinheit `KOMFORT`, über eine PC-Schnittstelle oder über Kommunikationssoftware bedient werden. Das stützt die getrennte Existenz der PC-Parametrierungsschnittstelle, beweist aber nicht, dass jeder Displayparameter über den aktuellen RS232-Zugang derselben Anlage schreibbar ist.
- Die Verbindungsleitung zur Bedieneinheit ist laut Montageanleitung nicht im Lieferumfang enthalten. Für die Kommunikation ist eine geschirmte Leitung vom Typ `Y(ST)Y 2x2x0,64` vorgesehen.
- Der Außenluftfilter ist standardmäßig Klasse `F7`; optional wird ein Pollenfilter Klasse `F9` genannt. Der Abluftfilter ist standardmäßig `G4`, optional wird `F5` genannt. Die frühere Kurzbeschreibung mit F7/G4 bleibt damit korrekt, wird aber um die optionalen Varianten ergänzt.
- Der Kondensatablauf führt im Wärmetauscher entstehendes Kondenswasser ab und muss über einen wirksamen Geruchsverschluss angeschlossen werden. Das ist ein Anlagen-/Montagehinweis und kein zusätzlicher Kältekreisnachweis.
- Das optionale PTC-Niedertemperatur-Vorheizregister schützt den Wärmetauscher bei sehr kalten Außentemperaturen vor dem Einfrieren. Ein zusätzlich erwähnter Sole-Registerschutz ist ebenfalls optional; beides darf bei deiner Anlage nicht als vorhanden angenommen werden.
- Die Bypassklappe umgeht den Wärmetauscher im Sommerbetrieb, wenn die Außentemperatur niedriger als die Raumtemperatur ist. Die konkrete Regelung erfolgt anlagenintern; ein direktes Hermes-Register für diese Bypassentscheidung ist auf deiner LG250 nicht bestätigt.

### 0.10 Detaillierte Funktionshinweise zu den Positionen 11 bis 15

Aus der zusätzlich bereitgestellten Detailseite ergeben sich für den Geräteaufbau folgende textliche Funktionshinweise:

- `11 Zuluftventilator`: stellt den Zuluftvolumenstrom für die Zuluft sicher und versorgt Wohnräume mit aufbereiteter Außenluft.
- `12 Abluftventilator`: stellt den Abluftvolumenstrom für die Abluft sicher und fördert verbrauchte Luft aus der Wohnung nach außen.
- `13 Frontdeckel mit Griffschraubverschluss`: dient Wartungsarbeiten; für Revisionszugang wird der Frontdeckel geöffnet, beim Schließen ist auf vollständigen Dichtsitz zwischen Frontdeckel und Gerätegehäuse zu achten.
- `14 Luftleitungsanschluss`: dient dem Anschluss der Luftleitungssysteme; bei der Montage ist auf die richtige Zuordnung der Leitungen zu Zuluft, Abluft, Außen- und Fortluft zu achten.
- `15 Kabeldurchführungen`: das Lüftungsgerät ist werkseitig elektrisch verdrahtet; die Kabeldurchführungen werden für den Anschluss der Bedieneinheit und optionaler Systemfühler verwendet.

Diese Hinweise sind für Inbetriebnahme und Plausibilitätsprüfung wichtig (Luftwege, Dichtheit, Verdrahtung), liefern aber keine direkte zusätzliche Registerbelegung für das Hermes-Textprotokoll.

### 0.11 Technische Daten und Bedienungslogik aus der vollständigen LG250-Anleitung

Die zusätzlich bereitgestellten Seiten enthalten die folgenden Herstellerdaten für das Lüftungsgerät `LG 250 System VENTECH`:

#### Gerätespezifikation

- Abmessungen des Lüftungsgeräts: `672 x 867 x 610 mm` (B x H x T).
- Gehäuse aus verzinktem Stahlblech, beschichtet nach `RAL 9010`, Wärmedämmung etwa `30 mm`.
- Luftleitungsanschlüsse: `4 x 160 mm`; Kondensatanschluss: `15 mm`.
- Versorgung: `230 V / 50 Hz`; Schutzart: `IP 20`.
- Zulässige Gerätetemperatur: `+5 bis +40 °C`; zulässige Außenlufttemperatur: `-15 bis +35 °C`.
- Gerätegewicht: etwa `60 kg`.
- Einstellbarer Luftvolumenstrom: `80 bis 250 m3/h` in Schritten von `4 m3/h`.
- Geräuschangabe: `0,30 W/m3/h` als spezifische Geräuschzahl im Datenblatt.
- Leistungsaufnahme im Stand-by: `1,6 W`.
- Gegenstromwärmetauscher aus Kunststoff; Wärmebereitstellungsgrad gemäß PHI: `88 %`.
- PHI-Benaglichkeitskriterium: `T_ZUL = +18,2 °C` bei `T_AUL = -10 °C`.
- Gehäusedichtheit gemäß PHI: externe Undichtheit kleiner als `0,6 %` im Druckbereich `50 bis 300 Pa`, interne Undichtheit kleiner als `1,0 %` bezogen auf den mittleren Luftvolumenstrom.

Die werkseitigen Lüfterstufen sind in der Anleitung mit diesen Volumenströmen beschrieben: Stufe I `80 m3/h`, Stufe II `160 m3/h`, Stufe III `250 m3/h`. Die dargestellten Leistungsaufnahmen bei externer Druckerhöhung `50/100 Pa` betragen laut Tabelle ungefähr `24/33 W`, `37/50 W` und `70/91 W` für die drei Stufen. Die Mess- und Kennliniendiagramme gelten laut Anleitung für F7-Zuluft- und G4-Abluftfilter sowie für die Ausführung ohne PTC-Nachheizregister; Filterzustand, Druckverlust und optionale Heizregister beeinflussen die realen Werte.

Die Anleitung beschreibt die drei Betriebsstufen fachlich als Grundlüftung (`80 m3/h`), Normallüftung (`160 m3/h`) und Intensivlüftung (`250 m3/h`). Die Tabelle enthält außerdem empfohlene Luftwechselraten von etwa `0,3/h`, `0,5/h` und `0,8/h`. Diese Angaben sind Soll-/Auslegungswerte und keine Umrechnung der aktuell gelesenen Hermes-Werte `L1` bis `L3`.

#### Bedieneinheiten und konkrete DESIGN-Anlage

Die Anleitung unterscheidet `MINI`, `KOMFORT` und `DESIGN`. Für die konkrete Anlage ist das `BT-M1 DESIGN` relevant. Das DESIGN-Bedienteil besitzt ein vollgrafisches Display, Status-LEDs sowie eine horizontale und vertikale Schiebeleiste. Die horizontale Leiste wählt Menüs beziehungsweise Zeilen; die vertikale Leiste bewegt sich innerhalb eines Menüs. Die Tasten `Zurück` und `Enter` dienen zum Verlassen beziehungsweise Bestätigen.

Die Anleitung beschreibt für DESIGN folgende Anzeige- und Bedienfunktionen:

- Betriebsstatus mit `Betrieb` (grüne LED), `Filterwartung` (gelbe LED) und `Störung` (rote LED).
- Hauptanzeige mit Uhrzeit, Datum, Luftstufe, Jahreszeit, Raumtemperatur und Betriebsart.
- Betriebsarten `Manueller Betrieb`, `Automatikbetrieb`, `Grundlüftung` und `Anlage Aus`.
- Auswahl der Luftstufen 1 bis 3; im Automatikbetrieb wird die Stufe über ein Zeitprogramm bestimmt.
- Auswahl von `Sommer` und `Winter`. Im Sommerbetrieb wird die Wärmerückgewinnung über die Bypassklappe umgangen; im Winterbetrieb bleibt die Wärmerückgewinnung aktiv.
- Anzeige und Auswahl der Raum-Solltemperatur. Laut Anleitung ist diese Funktion an eine externe Zusatzheizung gekoppelt; ohne solche Zusatzheizung darf daraus kein aktiver Heizbetrieb der konkreten Anlage abgeleitet werden.
- Einstellungen für Sommer- und Winter-Zeitprogramme mit Wochentagen, Zeitfenstern und Luftstufen.
- Systeminformationen wie Softwareversion, aktuelle Luftstufe, Raumtemperatur, Filter-Restlaufzeit und Betriebsstunden.
- Fehleranzeige mit Fehlernummer, Klartext und Zeitstempel; der Fehlerspeicher kann bis zu fünf Fehler anzeigen.

Die Darstellung `Anlage Aus` im DESIGN-Menü ist damit eine echte dokumentierte Betriebsart. Für die ESPHome-Anzeige bleibt trotzdem die Feldregel bestehen: `Anlage Aus / Standby` wird nur aus einem bestätigten `LS=0` abgeleitet, nicht aus dem unlesbaren oder unbestätigten Register `SW` beziehungsweise `MD`.

#### Zeitprogramme und Sonderfunktionen

Im Automatikbetrieb kann das DESIGN-Bedienteil die Luftstufe nach einem Zeitprogramm umschalten. Die Anleitung beschreibt getrennte Programme für Sommer und Winter, drei Zeitfenster je Wochentag sowie eine Kopierfunktion für weitere Wochentage. Zusätzlich kann eine zeitweise Intensivstufe beziehungsweise eine einstellbare Dauer der Luftstufe 3 aktiviert werden.

Das Service-Hauptmenü ist passwortgeschützt. In der Anleitung ist als Zugangscode `1001` abgebildet. Dort werden unter anderem Filter, Sprache, Temperaturabgleich, Luftvolumenströme, Grundlüftung, Werkseinstellungen und weitere Parameter verwaltet. Dieser Code wird nur als dokumentierter Bedienhinweis aufgenommen und nicht als ESPHome-Service oder automatischer Schreibpfad verwendet.

Die Einstellung `Luftvolumenströme` erlaubt laut Anleitung die Anpassung der Stufen 1 und 2 in Schritten von `4 m3/h`; die werkseitige Stufe 3 beträgt `250 m3/h`. Die Grundlüftung kann aktiviert oder deaktiviert werden. Diese Bedienwerte erklären die fachliche Bedeutung der Sollwerte, beweisen aber keine funktionierende Hermes-Schreibsequenz für `L1`, `L2`, `L3` oder `LS`.

#### Filterüberwachung und Fehlercodes

Die Filter-Restlaufzeit wird am DESIGN-Display angezeigt und kann über `Filter Reset` zurückgesetzt werden. Die Anleitung beschreibt einen zeitgesteuerten Filterwechsel sowie die Anzeige der verbleibenden Laufzeit. Das bestätigt die Wartungsfunktion, identifiziert aber kein Hermes-Register; `FI`, `FH` und `FR` bleiben auf dieser LG250 gemäß Feldtests nicht produktiv nutzbar.

Die Anleitung enthält für das DESIGN-Bedienteil unter anderem folgende Fehlergruppen:

| Gruppe | Dokumentierte Beispiele |
|---|---|
| Lüfter 1 | keine Drehzahl, Lüfter fährt nicht an, Überdrehzahl |
| Kommunikation 2 | Verbindung unterbrochen, keine Antwort eines Teilnehmers, Kommunikation Adapter/Leistungsteil |
| Messung 3 | Sensoreingang kurzgeschlossen oder offen |
| System 4 | Speicherfehler, interner Bus gestört, Systemfehler Leistungsteil |
| Extern 5 | externer Fehlereingang ausgelöst |
| Leistungsteil 6 | Frostmeldung, EWT-Fehler |

Die separate Fehlernummerntabelle nennt außerdem konkrete Sensorfehler für offene beziehungsweise kurzgeschlossene Eingänge sowie Lüfter- und Kommunikationsfehler. Für die aktuelle ESPHome-Integration bleibt `ER=0` die einzige auf der Anlage wiederholt bestätigte Aussage „kein Fehler“. Ein historischer DESIGN-Fehlerspeicher mit Datum und Uhrzeit ist dadurch noch nicht erschlossen.

#### Optionale bedarfsgerechte Lüftung

Die Anleitung beschreibt optionale bedarfsgerechte Lüftung über einen CO2-Sensor, einen Feuchtesensor oder eine kombinierte CO2-/Feuchtesensorik. Bis zu vier Sensoren können angezeigt werden; die Luftstufe wird anhand des höchsten Messwerts ausgewählt. Umschaltschwellen können für CO2 in `ppm` und für relative Feuchte in `% rH` eingestellt werden.

Diese Funktion ist für die konkrete Anlage nur als Option dokumentiert. Ein vorhandener CO2- oder Feuchtesensor sowie eine dafür passende Hermes-Registerbelegung sind bisher nicht nachgewiesen. Deshalb werden keine virtuellen CO2-/Feuchtewerte und keine Bedarfslüftungssteuerung in die Produktiv-YAML aufgenommen.

#### Temperaturfühler, Zusatzheizung und Verdrahtung

Die Verdrahtungsseite präzisiert die Fühler- und Erweiterungsanschlüsse: `T1` bis `T4` sind werkseitig elektrisch verdrahtet. Der Anschluss eines Außentemperaturfühlers an `T5` wird von der Steuerung automatisch erkannt. Weitere externe Systemkomponenten und Erweiterungsfühler sind optional und müssen entsprechend dem elektrischen Anschlussplan verdrahtet werden.

Damit entsteht eine wichtige Dokumentationsabgrenzung: Das Typenschild nennt `5 x KTY81`, während der Verdrahtungsplan T1 bis T4 als werkseitige Fühler und T5 als optional erkannten Außentemperaturfühler beschreibt. Die beobachteten Hermes-Namen und die Luftweg-Zuordnung der konkreten Firmware dürfen deshalb nicht ausschließlich aus der Anzahl der KTY-Eingänge abgeleitet werden. Die bestehende Zuordnung `T1` bis `T5` bleibt als Feldbeobachtung erhalten; die genaue elektrische Bestückung ist am konkreten Gerät zu prüfen.

Die Anleitung zeigt optionale Baugruppen wie PTC-Vorheizregister, Elektro- oder Warmwasser-Nachheizregister, Sole-Erdwärmetauscher/Wärmepumpe, Außenluftklappe und externe Sensoren. Der Schaltplan beweist deren Anschlussmöglichkeiten, aber nicht ihre Bestückung in deiner Anlage. Insbesondere darf aus einem `RL`-Bit kein vorhandenes Heizregister oder EWT geschlossen werden.

Die Verbindung zwischen Bedieneinheit und Leistungsteil erfolgt laut Anleitung über eine geschirmte Leitung `Y(ST)Y 2x2x0,64`, maximal etwa `100 m`. Die PC-Konfiguration verwendet einen separaten Schnittstellenadapter am Leistungsteil; darüber können Messwerte und Einstellungen gelesen, aufgezeichnet und grafisch dargestellt werden. Diese Beschreibung stützt die getrennte PC-Parametrierungsschnittstelle, liefert aber weiterhin keine direkte Hermes-Entsprechung für die DESIGN-Menüaktionen.

#### Inbetriebnahme und sicherheitsrelevante Hinweise

Vor der Inbetriebnahme sollen laut Anleitung alle Luftleitungen, Ein- und Auslassventile, Filter, der Kondensatanschluss, die elektrische Verdrahtung, die Bedieneinheit sowie optionale Komponenten geprüft werden. Werkseitige Einstellungen sollen nur durch Fachpersonal verändert werden. Arbeiten an Netzanschluss und elektrischen Komponenten sind Elektrofachkräften vorbehalten.

Für das Reverse Engineering folgt daraus: Bedienänderungen am DESIGN-Display sind gute Vorher-/Nachher-Trigger für die Beobachtung des PC-/Hermes-Lesepfads. Sie sind aber kein Beweis, dass dieselbe Funktion über die aktuelle RS232-Schnittstelle schreibbar ist. Jede spätere Schreibimplementierung braucht weiterhin gültiges Telegramm, `ACK`, passenden Readback und eine dauerhafte Zustandsänderung.

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
| Rd | Bedeutung auf dieser LG250 unbestätigt | Rohwert | 2min | Rohwerte `134..156` | funktioniert lesend | BDE zeigte etwa `20.5 degC`, während `Rd=146` bisher fälschlich als `14.6 degC` dargestellt wurde; Schreibtest `Rd=23` erhielt NAK | nur als Diagnose-Rohwert anzeigen |

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

#### 1.2.1.1 KNX-Gateway 08KNXGAC und ETS-Vorlage `LS`

Der neue Hinweis auf Pichlers `08KNXGAC`-KNX-Gateway und die Datei `08KNXGAC_LS_ETS_Vorlage.zip` ist fuer die weitere Recherche relevant. Der Dateiname `LS` ist ein plausibler Hinweis auf die dokumentierte LG150/LG250- beziehungsweise VENTECH-Geraetefamilie. Er ist jedoch allein noch kein Beweis, dass die Vorlage exakt die Firmware `40LG040100 V.4.0` der konkreten Anlage abbildet. Die Vorlage selbst liegt derzeit nicht im Repository vor und wurde hier noch nicht entpackt oder in ETS geprueft.

Das `08KNXGAC` ist laut Bezeichnung und Produktunterlagen ein Gateway zwischen KNX und Modbus RTU. Daraus folgt belastbar:

- Eine `LS`-ETS-Vorlage kann offizielle KNX-Kommunikationsobjekte, Klartexte, Datenlaengen, Skalierungen und moeglicherweise die dahinterliegenden Modbus-Datapoints dokumentieren.
- Die bereits vorliegende Modbusliste fuer `LG150/LG250A` ist damit eine passende Vergleichsquelle. Besonders relevant sind Luftstufe, Sommer-/Winterbetrieb, Filter-Restzeit, Bypassposition, Fehlerregister und Betriebsstunden.
- Die KNX-Vorlage kann zeigen, welche Funktionen Pichler offiziell ueber den Modbus-Gateway-Weg anbietet und welche davon lesbar oder schreibbar sind.

Aus der Gateway-Dokumentation folgt aber nicht automatisch:

- dass der konkrete Bedienteiladapter in deiner Anlage Hermes in Modbus RTU uebersetzt;
- dass das `BT-M1 DESIGN`-Display intern denselben Modbus-Datenpunktweg verwendet wie das KNX-Gateway;
- dass ein Modbus-Register direkt als Hermes-Zweizeichenbefehl (`LS`, `L2`, `Rd` usw.) adressierbar ist;
- dass eine in ETS sichtbare Schreibfunktion ueber die aktuelle PC-RS232-Schnittstelle ebenfalls funktioniert.

Die bisherige Feldarchitektur bleibt daher unveraendert: Der ESP32 spricht auf dem beobachteten PC-Anschluss das native Hermes-Protokoll mit `9600 7E1`, ASCII-Zweizeichenbefehlen, `EOT`/`STX`/`ETX` und XOR-Schreibpruefung. Der Modbusweg des KNX-Gateways ist ein separater Protokollpfad, solange kein Schaltplan, kein Gateway-Telegramm oder kein Busmitschnitt die Kopplung nachweist.

#### Auswertungsplan fuer die ETS-Vorlage

Falls die ZIP-Datei beschafft wird, sollte sie zuerst nur lesend als Dokumentationsquelle ausgewertet werden:

1. ZIP entpacken und Dateityp feststellen (`.knxprod`, XML oder ETS-DCA-Dateien); keine Datei in die Anlagensteuerung importieren.
2. Produktname, Herstellerkennung, Modellfamilie, Firmware-/Applikationsversion und gegebenenfalls Modbus-Slave-ID dokumentieren.
3. Kommunikationsobjekte und Klartexte exportieren, insbesondere Luftstufe, Stufe-1/2/3-Sollwerte, Sommer/Winter, Bypass, Filter, Fehler und Betriebsstunden.
4. Bei jedem Objekt Datentyp, Einheit, Wertebereich, Richtung (lesen/schreiben) und Modbus-Adresse getrennt erfassen.
5. Die Ergebnisse mit `LIST_Modbus_ES1015_FW_LG150AB_LG250A_v2.0.0.xlsx` vergleichen; Widersprueche als Versions- oder Produktfamilienabweichung markieren.
6. Erst danach pruefen, ob sich ein Modbus-Telegramm oder eine Herstellerbeschreibung auf den konkreten Bedienteiladapter beziehen laesst.

Die ETS-Kommunikationsobjekte sind damit ein Schluessel fuer das offizielle Datenmodell, aber noch nicht automatisch der Schluessel fuer die fehlende Hermes-Schreibsequenz. Fuer jede spaetere Uebertragung in die ESPHome-Komponente gilt weiterhin: Registersemantik, Frameformat, `ACK`, Readback und dauerhafte Zustandsaenderung muessen auf der konkreten LG250 bestaetigt werden. Fuer netzspannungsnahe Relais-, Heizungs- oder Reset-Funktionen bleibt ein passiver Dokumentationsvergleich die einzige zulaessige erste Stufe.

#### 1.2.1.2 Auswertung der entpackten `LS`-ConfigTool-Datei

Die entpackten Dateien liegen jetzt unter `documents/KNX/`. Die wichtigste Datei fuer die Registerauswertung ist `08KNXGAC_LS_ConfigTool.wz8861`. Sie ist eine lesbare JSON-Konfiguration fuer das Weinzierl-Gateway `KNX Modbus RTU Gateway 886.1 secure`, nicht die Firmware der LG250 und nicht der Quellcode des Pichler-Bedienteiladapters.

Die Datei bestaetigt fuer diesen Gateway-Datensatz:

| Gateway-Einstellung | Dokumentierter Wert |
|---|---|
| Gateway-Rolle | Modbus-Master, KNX-seitig angebunden |
| gemeinsame Modbus-Slave-Adresse | `20` |
| Baudrate | `19200` |
| Paritaet/Stop | `even`, 1 Stopbit (`8E1`) |
| Byte-Reihenfolge | MSB first |
| Registeradressierung | 0-basiert |
| Lesen | Function `04`, Read Input Registers |
| Bit-Schreiben | Function `05`, Write Single Coil |
| Word-Schreiben | Function `06`, Write Single Holding Register |

Die `LS`-Konfiguration enthaelt folgende relevante Datenpunkte. Die Adressen sind Modbus-Adressen dieses Gateway-Mappings und keine Hermes-Codes:

| Beschreibung in der LS-Datei | Richtung | Modbus-Adresse | Datentyp/Funktion |
|---|---|---:|---|
| Alarm Lüftungsgerät | Modbus -> KNX | 29 | Bit 0 aus Function 04 |
| Alarm Reset + Neustart | KNX -> Modbus | 63 | 16-Bit-Wert, bei EIN Wert `3` |
| Ist Außenlufttemperatur | Modbus -> KNX | 30 | 16-Bit Temperatur, Function 04 |
| Ist Fortlufttemperatur | Modbus -> KNX | 31 | 16-Bit Temperatur, Function 04 |
| Ist Ablufttemperatur | Modbus -> KNX | 32 | 16-Bit Temperatur, Function 04 |
| Ist Zulufttemperatur | Modbus -> KNX | 33 | 16-Bit Temperatur, Function 04 |
| Ist Zuluftvolumenstrom | Modbus -> KNX | 46 | unsigned 16-Bit, Function 04 |
| Ist Abluftvolumenstrom | Modbus -> KNX | 47 | unsigned 16-Bit, Function 04 |
| Ist aktueller Betriebsstatus | Modbus -> KNX | 48 | niederwertiges Byte, Function 04 |
| Ist aktuelle Lüftungsstufe | Modbus -> KNX | 59 | niederwertiges Byte, Function 04 |
| Soll Betriebsmode Sommer/Winter | KNX -> Modbus | 1 | niederwertiges Byte |
| Soll Lüftungsstufe | KNX -> Modbus | 2 | niederwertiges Byte |
| Parameter Regelungsart Temperatur | KNX -> Modbus | 7 | niederwertiges Byte |
| Soll Volumenstrom Stufe 1 | KNX -> Modbus | 9 | unsigned 16-Bit |
| Soll Volumenstrom Stufe 2 | KNX -> Modbus | 10 | unsigned 16-Bit |
| Soll Volumenstrom Stufe 3 | KNX -> Modbus | 11 | unsigned 16-Bit |
| Soll Volumenstrom Grundlüftung | KNX -> Modbus | 12 | unsigned 16-Bit |
| Soll Zulufttemperatur | KNX -> Modbus | 22 | 16-Bit Temperatur |
| Soll Raumlufttemperatur | KNX -> Modbus | 23 | 16-Bit Temperatur |
| Soll Ablufttemperatur | KNX -> Modbus | 24 | 16-Bit Temperatur |
| Ist CO2 Sensor 1/2 | Modbus -> KNX | 89/90 | in der Datei als DPT 9 abgebildet |
| Freigabe Heizung/Kühlung | KNX -> Modbus | 89/90 | Bit 0 im Word |
| Ist Ausgang Heiz-/Kühlregister | Modbus -> KNX | 11/12 | 0..1000 Registerwert, DPT 5 |
| Ist Ausgang Vorheiz-/Kombiregister/Kühlanforderung | Modbus -> KNX | 16/17/18 | Bit 0 aus Function 04 |
| Ist Betriebsmeldung Lüftung | Modbus -> KNX | 19 | Bit 0 aus Function 04 |
| Ist Ausgang Bypassklappe | Modbus -> KNX | 20 | Bit 0 aus Function 04 |

Der Kernabgleich mit der vorhandenen Pichler-Modbusliste ist damit deutlich staerker als zuvor: `1` Sommer/Winter, `2` Luftstufe, `48` Betriebsstatus, `59` aktuelle Luftstufe sowie `46/47` Luftvolumenstrom und `89/90` CO2-Datenpunkte passen in das offizielle LS-Datenmodell. Die Konfiguration verwendet dabei 0-basierte Adressen; Angaben aus anderen Modbuslisten muessen deshalb vor einem Vergleich auf dieselbe Adresskonvention gebracht werden.

Es gibt zugleich eine wichtige Modellierungsauffaelligkeit: Die Datei verwendet die Adressen `89` und `90` sowohl fuer `Ist_CO2 Sensor 1/2` als auch fuer die schreibbaren Bits `Para_Freigabe Heizung` und `Para_Freigabe Kühlung`. Das ist in einem Word-Register technisch moeglich, aber die JSON-Datei allein klaert nicht, ob hier unterschiedliche Bit-/Wortansichten desselben Registers, optionale Betriebsvarianten oder eine fehlerhafte/mehrdeutige Gateway-Vorlage vorliegen. Diese Adressen duerfen daher nicht blind als CO2- oder Heizungswerte in Hermes uebersetzt werden.

Die Datei bestaetigt ausserdem nicht, dass die Modbus-Schreibobjekte direkt die bisher getesteten Hermes-Writes `L1`, `L2`, `L3`, `LS` oder `Rd` ausloesen. Im Gegenteil: Das Gateway nutzt numerische Register und Modbus-Funktionscodes, waehrend der aktuelle PC-Anschluss `9600 7E1` und Hermes-Zweizeichenbefehle verwendet. Der naechste sichere Erkenntnisschritt ist deshalb ein passiver Vergleich der entpackten `LS`-Datenpunkte mit den bereits beobachteten Hermes-Readbacks; eine direkte Modbus-Anfrage an den Bedienteiladapter wird ohne bestaetigte Pegel, Busseite und Terminierung nicht durchgefuehrt.

#### 1.2.1.3 BACnet-Gateway-Unterlagen und Modbus-Master-Konfiguration

Die zusaetzlich abgelegten BACnet-Unterlagen unter `documents/Bacnet/` beschreiben einen zweiten Protokollweg:

```text
BACnet/IP <-> BACnet-/Modbus-Gateway <-> Modbus RTU
```

Die Datei `documents/Bacnet/ugw/config/modmster1.txt` enthaelt eine konkrete Modbus-Master-Konfiguration mit Slave `20`. Sie verwendet fuer die LS-Datenpunkte dieselben Adressen wie die entpackte KNX-ConfigTool-Datei:

| Funktion | Modbus-Richtung im Master | Adresse |
|---|---|---:|
| Außenlufttemperatur | Input lesen | `30` |
| Fortlufttemperatur | Input lesen | `31` |
| Ablufttemperatur | Input lesen | `32` |
| Zulufttemperatur | Input lesen | `33` |
| Zuluftvolumenstrom | Input lesen | `46` |
| Abluftvolumenstrom | Input lesen | `47` |
| Betriebsstatus | Input lesen | `48` |
| aktuelle Lüftungsstufe | Input lesen | `59` |
| Freigabe Heizung | Holding schreiben | `89` |
| Freigabe Kühlung | Holding schreiben | `90` |
| Volumenstrom Stufe 1 | Holding schreiben | `9` |
| Volumenstrom Stufe 2 | Holding schreiben | `10` |
| Volumenstrom Stufe 3 | Holding schreiben | `11` |
| Volumenstrom Grundlüftung | Holding schreiben | `12` |
| Soll-Zulufttemperatur | Holding schreiben | `22` |
| Soll-Raumlufttemperatur | Holding schreiben | `23` |
| Soll-Ablufttemperatur | Holding schreiben | `24` |
| Regelungsart Temperatur | Holding schreiben | `7` |
| Sommer/Winter Sollwert | Holding schreiben | `1` |
| Soll-Lüftungsstufe | Holding schreiben | `2` |

Der BACnet-Master verwendet fuer die Register `input` und `holding` die ueblichen getrennten Modbus-Bereiche. Diese Konfiguration bestaetigt damit die fachliche und technische Konsistenz des LS-Mappings deutlich staerker als eine reine BACnet-Namensliste. Sie beweist aber weiterhin nur den Modbus-Gateway-Pfad, nicht die Umsetzung auf den nativen Hermes-PC-Anschluss.

Die Datei `documents/Bacnet/ugw/config/bac1.txt` bildet dieselben Werte als BACnet-Objekte ab. Die EDE-Daten nennen unter anderem:

- Analogwerte fuer Außenluft, Fortluft, Abluft und Zuluft mit Grad-Celsius-Einheit;
- Analogwerte fuer Zuluft- und Abluftvolumenstrom;
- binäre Zustände fuer Vorheizregister/Solepumpe/EWT-Klappe, Heiz- und Kühlanforderung sowie Bypass;
- Mehrzustandsobjekte fuer aktuelle Lüftungsstufe und Betriebsstatus;
- schreibbare BACnet-Objekte fuer Heizungs-/Kühlungsfreigabe, Volumenstrom-Sollwerte, Temperatur-Sollwerte, Regelungsart, Sommer/Winter und Soll-Lüftungsstufe;
- `Alarm_Reset + Neustart` als schreibbares Objekt, das im Modbus-Mapping auf Register `63` mit dem Wert `3` abgebildet wird.

Die separat abgelegte EDE-Datei `EDE_ES2020_LG350_450_740_1000SK_v1/bacnet_EDE.csv` ist ausdrücklich fuer die Gerätefamilie `LG350/450/740/1000SK` benannt. Ihre BACnet-Objektliste ist deshalb keine direkte LG250-Firmwarequelle. Sie ist nur als Vergleich fuer Pichlers allgemeine Objektstruktur, Zustandsnamen und Gateway-Konventionen zulaessig. Das gilt besonders fuer `Alarm Reset`, Fehlerzustände, Bypass-/WRG-Texte und optionale Heizungs-/EWT-Funktionen.

Die in den BACnet-State-Texts dokumentierten Zustände sind fuer die LG250-Interpretation trotzdem hilfreich, aber noch nicht automatisch verbindlich: aktuelle Lüftungsstufe `Standby`, `Stufe 1`, `Stufe 2`, `Stufe 3`, `Grundlüftung`, `Extern Stopp`, `Fehler`; Betriebsstatus `CPU startup`, `Standby`, `Anlauf`, `Betrieb`, `Nachlauf`, `Standby Powersafe`, `Testmodus`; Jahreszeit `Sommer`/`Winter`. Die konkrete Hermes-Anzeige bleibt an den Feld-Readbacks `LS`, `ST`, `RL` und `ER` zu verifizieren.

#### BACnet-/KNX-Ergebnis fuer das Reverse Engineering

Die jetzt vorhandenen KNX- und BACnet-Dateien bestaetigen gemeinsam ein offizielles Modbus-Datenmodell fuer die `LS`-Konfiguration. Sie liefern belastbare Kandidaten fuer die Bedeutung und Schreibbarkeit der numerischen Modbus-Register `1`, `2`, `7`, `9..12`, `22..24`, `48`, `59` und `63`. Sie liefern jedoch keine direkte Hermes-Uebersetzung und keinen Nachweis, dass der konkrete Pichler-Bedienteiladapter Modbus RTU spricht.

Damit ist der naechste sichere Schritt ein Dokumentenabgleich, kein aktiver Bus-Test: Modbus-Adresse, Registertyp, Skalierung und Richtung aus KNX-/BACnet-Mapping gegen die beobachteten Hermes-Codes und Readbacks stellen. Ein Modbus- oder RS485-Sendeversuch am Bedienteiladapter bleibt gesperrt, bis dessen elektrische Busseite, Baudrate, Paritaet, Teilnehmerrolle und Terminierung eindeutig identifiziert sind.

#### 1.2.1.4 Anschlussbelegung und Terminierung des KNX-Gateways

Die neu bereitgestellte Anschlussseite des `08KNXGAC` beschreibt die Modbus-Klemmen eindeutig:

| Anschluss | Symbol | Funktion |
|---:|---|---|
| 1 | `-` | Modbus-Masse, verbunden mit Anschluss 4 |
| 2 | `A` | Modbus-Datenleitung A(+), verbunden mit Anschluss 5 |
| 3 | `B` | Modbus-Datenleitung B(-), verbunden mit Anschluss 6 |
| 4 | `-` | Modbus-Masse, verbunden mit Anschluss 1 |
| 5 | `A` | Modbus-Datenleitung A(+), verbunden mit Anschluss 2 |
| 6 | `B` | Modbus-Datenleitung B(-), verbunden mit Anschluss 3 |
| KNX `+` | `+` | positiver KNX-Busanschluss |
| KNX `-` | `-` | negativer KNX-Busanschluss |

Die Anschlüsse `1..3` und `4..6` sind zwei durchverbundene Modbus-Anschlusspaare für die Busweiterführung. Sie sind keine zwei getrennten Modbus-Kanäle. Der Modbus-Strang soll am jeweils letzten Empfänger mit einem Widerstand von `120 Ohm / 0,25 W` zwischen den beiden Signalleitungen abgeschlossen werden. Im Gateway selbst ist laut Anleitung kein Abschlusswiderstand eingebaut; der Widerstand muss extern an der oberen oder unteren Klemmenleiste gesetzt werden.

Diese Angaben gelten für das Weinzierl- beziehungsweise `08KNXGAC`-Gateway. Sie beweisen nicht, dass der Pichler-Bedienteiladapter dieselbe Klemmenbelegung, Terminierung oder Modbus-Elektrik besitzt. Für einen Anschluss an die Anlage müssen die Klemmen des konkreten Adapters separat identifiziert werden.

#### 1.2.1.5 Auswertung der Pichler-Parametrierungssoftware

Die Parametrierungssoftware aus den Pichler-Handbuch-Screenshots war bisher bereits als Funktionskontext erfasst, aber noch nicht als eigener Reverse-Engineering-Baustein. Die neuen Unterlagen erlauben jetzt eine präzisere Einordnung.

Die Software ist laut Anleitung eine PC-Konfigurations- und Diagnosesoftware für das Leistungsteil. Sie wird über einen separaten Schnittstellenadapter am Leistungsteil angeschlossen. In den Screenshots sind mindestens diese Bereiche erkennbar:

- Hauptübersicht mit Gerätezustand, Betriebsart, Luftstufe und mehreren Temperaturwerten;
- aktuelle Luftvolumenströme und Drehzahlen der beiden Ventilatoren;
- Messwerte und Stellgrößen für Zuluft-/Abluftventilator, einschließlich Spannungen beziehungsweise Ausgangswerten;
- zeitlicher Verlauf wichtiger Betriebswerte als Diagramm;
- Status der Relais beziehungsweise externen Ausgänge;
- Parameter für Luftvolumenströme, Temperaturregelung, Nachheizregister, Abluftbetrieb und optionale EWT-/Wärmepumpenfunktionen;
- Service- und Testfunktionen für Relais, Lüfterstufen und Werkseinstellungen;
- Datenaufzeichnung sowie eine Meldungs-/Ereignisliste.

Die Softwaredarstellung passt fachlich sehr gut zu den inzwischen aus KNX und BACnet bestätigten Modbusdatenpunkten: Temperaturen, Luftvolumenströme, Betriebsstatus, Luftstufe, Bypass-/Heizungszustände und Sollwerte. Die Software ist daher eine starke Quelle für die Bedeutung der Werte und dafür, welche Parameter der Hersteller grundsätzlich vorgesehen hat.

Sie liefert aus den Screenshots allein jedoch nicht:

- die konkrete Modbus-Slave-Adresse, sofern diese nicht im Verbindungskonfigurationsdialog angezeigt wird;
- den seriellen Modbus-Rahmen, Function Code, Byte-Reihenfolge und CRC;
- die internen Hermes-Zweizeichenbefehle des Leistungsteils;
- eine Zuordnung jedes sichtbaren Softwarefeldes zu einem bestimmten Hermes-Register;
- den Nachweis, dass die Software über den aktuellen PC-RS232-Anschluss dieselbe Schnittstelle verwendet wie das `08KNXGAC`-Modbus-Gateway.

Die Software ist deshalb für Reverse Engineering in drei Ebenen zu verwenden:

1. **Semantik:** sichtbare Bezeichnungen und Einheiten gegen KNX-/BACnet-Datenpunkte und Hermes-Readbacks vergleichen.
2. **Zugriffsrechte:** Felder in der Software als Anzeige-, Parameter- oder Testfunktion klassifizieren; ein sichtbares Eingabefeld ist noch kein Beweis für einen funktionierenden Hermes-Write.
3. **Protokoll:** nur mit einem aufgezeichneten PC- oder Bus-Telegramm die tatsächliche Modbus-/Hermes-Übertragung ableiten.

Besonders relevant für die bisherigen Schreibtests ist: Die Software kann Sollwerte und Parameter offenbar darstellen und ändern, während `L1`/`L2`/`L3` über Hermes zwar `ACK`, aber keinen dauerhaften Readback zeigen. Das spricht dafür, dass mindestens ein zusätzlicher Adapter-, Freigabe-, Speicher- oder Schnittstellenpfad beteiligt sein kann. Es beweist aber noch keine konkrete Save-Sequenz. Die KNX-/BACnet-Mappings machen jetzt einen passiven Vergleich möglich, ersetzen aber keinen Mitschnitt der Pichler-Softwarekommunikation.

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

Ein anschliessender Schreibtest mit `Rd=23` wurde mit `NAK` abgelehnt. Das schliesst den Lesepfad nicht aus: `Rd` kann auf dieser Anlage gelesen werden, ist aber nicht als schreibbarer Befehl bestaetigt. Der BDE-Sollwert lag bei etwa `20.5 degC`, während parallel ein Rohwert wie `Rd=146` gelesen wurde. Die bisherige Multiplikation mit `0.1` war deshalb eine unbelegte und irreführende Interpretation und wurde entfernt. `Rd` wird in der LG250-YAML nur noch als unskalierter Diagnose-Rohwert angezeigt. Eine Zuordnung als Raum-Sollwert erfordert einen kontrollierten Vorher-/Nachher-Test am BDE.

#### Generische WR3223-Kommandotabelle und RL-Bitmaske

Die neu bereitgestellte Hermes-Seite ist eine Primärquelle für die gezeigte WR3223-Protokollvariante. Sie ist nicht automatisch eine vollständige LG250-Firmwarebeschreibung. Die folgenden Bedeutungen gelten daher zunächst als generische WR3223-Semantik und müssen für die `40LG040100 V.4.0` durch Readbacks und Feldzustände bestätigt werden.

Die Bitmaske fuer `RL` (Relais lesen) lautet in dieser generischen Tabelle:

| Bitmask | Bedeutung |
|---:|---|
| 1 | Kompressor |
| 2 | Zusatzheizung Relais |
| 4 | Erdwaermetauscher |
| 8 | Bypass |
| 16 | Vorheizregister |
| 32 | Netzrelais Bypass |
| 64 | Bedienteil aktiv |
| 128 | Bedienung ueber RS-Schnittstelle |
| 256 | Luftstufe vorhanden |
| 512 | WW_Nachheizregister |
| 2048 | Magnetventil |
| 4096 | Vorheizen aktiv |

Die Bitmaske in `binary_sensor.py` stimmt mit dieser generischen PDF-Tabelle ueberein; das Bitmuster springt absichtlich von 512 auf 2048 und laesst 1024 aus. Für die LG250 ist konkret beobachtet: `RL=6` entspricht Bits 2 und 4, also Zusatzheizung und Erdwaermetauscher; Bit 128 wurde auf dieser Anlage bisher nicht beobachtet. Die Tabelle beweist nicht, dass `RL` selbst schreibbar ist.

Die Seite nennt außerdem `E1` bis `E8` als Kalibrierparameter der Temperaturfühler sowie `rT` als reine Relais-Testfunktion. Diese Befehle werden nicht in die produktive LG250-YAML aufgenommen: Für `E1-E8` fehlt ein LG250-Feldtest, und `rT` könnte direkt Relais beziehungsweise netzspannungsnahe Ausgänge schalten.

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

Die neu bereitgestellten Seiten dokumentieren für die konkrete Anlage das `BT-M1 DESIGN`. Die früher ausgewerteten Bedienbilder enthalten zusätzlich KOMFORT-Beispiele; die fachlichen Funktionen überschneiden sich, die Bedienoberfläche und Navigation sind aber nicht identisch.

Die DESIGN-Hauptanzeige zeigt:

- Uhrzeit und Datum
- aktuelle Lueftungsstufe, zum Beispiel `Luftstufe 3`
- Jahreszeit, `Sommer` oder `Winter`
- Raumtemperatur
- Betriebsart, zum Beispiel `Automatikbetrieb`

Ziel in HA: eine kompakte Statusansicht aus `LS`, `ST`, `T4` beziehungsweise der passenden Raumtemperatur und den Ventilatordrehzahlen. `LS=1..3` steht fuer manuelle Stufen; `LS=4` wird auf dieser Anlage als Automatik-/Grundlueftungsmodus beobachtet. Die DESIGN-Anzeige kann zusätzlich `Anlage Aus`, `Sommer/Winter`, Filterwartung und Störung direkt darstellen; diese Klartexte werden in HA aber nur aus bestätigten Registerwerten abgeleitet.

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

Das bereitgestellte Pichler-Merkblatt „Anleitung Filterwechsel LG 250“ ergänzt die praktische Geräte- und Wartungsdokumentation:

- Außenluftfilter: Kassettenfilter Klasse `F7`; optional kann ein Pollenfilter der Klasse `F9` eingesetzt werden.
- Abluftfilter: Kassettenfilter Klasse `G4`.
- Die Filterkontrollmeldung erscheint laut Merkblatt alle vier Monate an der Bedieneinheit; die Filterverschmutzung soll zusätzlich regelmäßig kontrolliert werden.
- Bei der Filterkontrollmeldung leuchtet die Leuchtdiode rechts unten gelb.
- Vor dem Öffnen wird das Lüftungsgerät zunächst über die Bedieneinheit ausgeschaltet. Danach soll die Lüftungsstufe weiter abgesenkt werden, bis die Anlage die minimale Stufe erreicht und die Diode an der Bedieneinheit nicht mehr leuchtet. Erst dann wird die Anlage allpolig vom Netz getrennt.
- Für Reinigungs- und Wartungsarbeiten ist die allpolige Netztrennung vorgeschrieben; das Merkblatt warnt ausdrücklich davor, sich nur auf das Ausschalten an der Bedieneinheit zu verlassen.

Das Display zeigt:

- Filter-Restlaufzeit, im Screenshot `2284 h`
- Filter Reset

Ziel in HA: Sensor fuer die Filterlaufzeit und ein Button fuer den Reset. Das Merkblatt bestätigt die Wartungsanzeige und die sicheren Abschaltbedingungen, aber kein Hermes-Register. Der angefragte Wert ist weiterhin nicht sicher einem lesbaren Register zugeordnet; `FH` und `FR` waren auf dieser Firmware nicht gueltig. Ein Filter-Reset darf erst implementiert werden, wenn das Schreibregister und die erforderliche Sequenz bekannt sind. Die offizielle Modbusliste nennt separat eine Filter-Restzeit, aber diese Modbus-Adresse ist nicht automatisch ein Hermes-Befehl.

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

Das BDE- beziehungsweise `BT-M1 DESIGN`-Display hängt an einer separaten RS485-Schnittstelle. In der konkreten Installation sitzt zwischen Display und RS485-Leitung zusätzlich ein Pichler-Display-Converter beziehungsweise Bedienteiladapter. Dieses Projekt verwendet ausschließlich die PC-Parametrierungsschnittstelle über RS232 mit dem Hermes-Zweizeichenprotokoll. Ein RS485-Sniffer ist daher nicht zwingend erforderlich: Displayänderungen können über die resultierenden RS232-Readbacks korreliert werden. Der Converter bleibt eine offene Architekturfrage, solange seine Ein-/Ausgänge und seine konkrete Protokollfunktion nicht vermessen oder aus einem Schaltplan belegt sind.

### 10.1 Bereits bestätigte Verhaltensdaten

- `LS=4` wird als `Automatik - Grundlüftung` erkannt.
- Eine Displayänderung kann `LS=4` auf `LS=2` ändern; die Statusanzeige meldet danach `Manuell - Stufe 2`.
- `Rd` ist lesbar und liefert LG250-Rohwerte wie `134..156`; im LG250-YAML wird der Wert derzeit unskaliert als Diagnose-Rohwert dargestellt, weil die Zuordnung zum DESIGN-Raum-Sollwert nicht bestaetigt ist.
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

Das passt als Hypothese zu `L2=40 -> ACK -> Readback L2=33`: Der Frame wird auf Transportebene akzeptiert, aber der Parameter wird ohne eine Freigabe-/Schreibschutzsequenz nicht dauerhaft übernommen. Es ist jedoch nicht bewiesen, dass `RESETCode` bei der Pichler-LG250 denselben Hermes-Befehl oder dieselbe Bedeutung hat. Der Name ist in der aktuell bekannten zweistelligen Registerliste dieses Projekts nicht enthalten und darf deshalb nicht geraten oder blind geschrieben werden.

Der Displaybefund schränkt die Übertragung zusätzlich ein: Bei der LG250 führte das Abziehen des BDE zu `LS=0`, `RL=0`, `ST=16` und abgeschalteten Ausgängen. Deshalb darf `X1` nicht erneut als normaler Schreibtest abgezogen werden, solange kein sicherer Wiederanlauf- und Rückfallplan besteht. Das kann eine Watchdog-/Freigabefunktion sein, ist durch die bisherigen Readbacks aber noch nicht als konkrete Firmwareimplementierung bewiesen.

#### Priorisierter Test für RESETCode

1. Die Hermes-/WR3223-Unterlagen und vorhandenen Community-Implementierungen nach einer exakten Register- oder Frame-Zuordnung für `RESETCode` durchsuchen.
2. Prüfen, ob der Wert als zweistelliges Hermes-Kommando, als Teil eines Parameterframes oder nur über das BDE-Protokoll existiert.
3. Erst nach bestätigter Zuordnung einen einzelnen, reversiblen Test mit dem bestehenden Readback-Schutz ausführen.
4. Erfolg nur bei `ACK` plus passendem Readback und anschließend stabiler Wiederholungslesung annehmen.

Bis dahin bleiben `L1`, `L2` und `L3` formal quittierte, aber funktional nicht bestätigte Writes. Die verwandten WR3223-Quellen enthalten außerdem Wärmepumpen-/Kältekreisparameter wie `VerdTemp` und `KondTEMP`; diese gelten nicht als Beleg dafür, dass die konkrete LG250-Anlage einen Verdampfer oder Kondensator besitzt.

### 10.7 Prüfung der RESETCode-Frames aus verwandten WR3223-Unterlagen

Die vorgeschlagene Sequenz `Re1 -> L240 -> Re0` ist für die LG250 derzeit nicht freigegeben. Die beiden genannten Aerex-PDFs waren erreichbar, konnten in der verfügbaren Umgebung aber nicht zuverlässig textuell extrahiert werden. Deshalb ist daraus noch kein verifizierter Register- oder Framebeleg für `RESETCode` entstanden.

Gegen einen blinden Test sprechen außerdem die bereits belegten Bedeutungen im Hermes-Registerkatalog dieses Projekts:

- `Re` ist als Zulufttemperatur-Sollwert dokumentiert und wird im generischen Number-Pfad als Register `Re` behandelt.
- `Es` ist als Schaltpunkt Sommer-Stopp des Erdwaermetauschers dokumentiert.
- `RC` ist in der bekannten zweistelligen Registerliste nicht enthalten.

Damit sind `Re1` und `Es1` keine sicheren RESETCode-Frames, sondern könnten reale Anlagenparameter verändern. Die beispielhaften Frames haben zwar die richtige Struktur eines Hermes-Schreibtelegramms, aber die Struktur allein beweist weder den Registercode noch die Schreibberechtigung oder die EEPROM-Wirkung.

Die Reset-/Speicherhypothese bleibt dennoch relevant: Die verwandten Quellen beschreiben eine Freigabe vor Parameteränderungen und erklären damit plausibel `ACK` ohne geänderten Readback. Der nächste sichere Schritt ist die genaue Zuordnung von `RESETCode` aus einer extrahierbaren Originaltabelle oder einem reproduzierbaren BDE-/Service-Frame. Bis dahin werden weder `Re1`, `Es1`, `Re0` noch `Es0` automatisch oder manuell als Testsequenz in die LG250-YAML eingebaut.

### 10.8 Neue Primärquelle: Hermes-Schnittstellenprotokoll vom 20.08.2012

Die neu bereitgestellten Originalseiten von Hermes Electronic sind deutlich belastbarer als die bisherigen Community-Zusammenfassungen. Sie bestätigen für die dokumentierte WR3223-Schnittstelle:

- `9600 Baud`, `7 Bit + 1 Bit Parität`, gerade Parität und ein Stoppbit.
- Leseanforderung: `EOT + Adresse + C1 + C2 + ENQ`.
- Schreibtelegramm: `EOT + Adresse + STX + C1 + C2 + Daten + ETX + CKS`.
- `CKS = C1 XOR C2 XOR Datenbytes XOR ETX`.
- `ACK`: Der übertragene Wert ist laut Originaltext gültig und ausgeführt beziehungsweise abgespeichert.
- `NAK`: Der übertragene Wert ist ungültig und nicht ausgeführt.

Die Seite mit dem Schreibbeispiel `L1 60` bestätigt damit, dass unser `L2=40`-Telegramm strukturell dem offiziellen Hermes-Format entspricht. Unser beobachtetes Ergebnis `ACK` mit anschließendem Readback `L2=33` ist deshalb eine echte LG250-Abweichung vom dokumentierten Erfolgsversprechen oder ein Hinweis auf eine zusätzliche, variantenspezifische Betriebs-/Speicherbedingung. Der Readback bleibt für unsere Integration das maßgebliche Kriterium.

Der abgebildete Kommandokatalog enthält `L1`, `L2`, `L3`, `LD`, `Ld`, `EC`, `Es`, `ES`, `EW`, `EE`, `EA`, `ER`, `RL`, `UZ`, `UA`, `NZ`, `NA`, `NM`, `Tf`, `Ta`, `MD`, `KM`, `ZH`, `WP`, `PA` und `II`, aber keinen Eintrag `RESETCode`, `RC`, `Re` oder `BDE 0/1`. `MD` ist dort als „Mode lesen“ aufgeführt, nicht als Schreibregister.

Wichtig für die bisherige RESET-Hypothese: `Es` ist in dieser Primärquelle als **Sole-Stopp-Temperatur lesen/schreiben** beschrieben. Es ist damit kein belegter RESET-Code. Die Quelle liefert keinen sicheren RESET- oder BDE-Freigabeframe; solche Frames werden weiterhin nicht implementiert.

Die RL-Tabelle bestätigt außerdem die Bitwerte `2=Zusatzheizung`, `4=Erdwärmetauscher`, `16=Vorheizregister`, `32=Netz Bypass`, `64=Bedienteil aktiv`, `128=Bedienung über RS-Schnittstelle`, `256=Luftstufe vorhanden`, `512=Warmwasser-Nachheizregister`, `2048=Magnetventil` und `4096=Vorheizen aktiv`. Unser `RL=6` passt damit zu Zusatzheizung plus EWT; die Bits 64 und 128 sind dabei nicht gesetzt. Die bisherige empirische Beobachtung `Bedienteil aktiv: 0` ist daher konsistent mit dem Originalkatalog.

`RL` ist laut Primärquelle ein Leseregister („Relais lesen“). Das Bit `128` kann deshalb nicht durch einen `RL=128`-Write gesetzt werden. Der separate Kandidat für die RS-Bedienfreigabe ist `RS`; genau `RS=1` wurde auf dieser LG250 jedoch mit `NAK` beantwortet. Damit ist derzeit kein funktionierender Weg bekannt, das Bit `Bedienung über RS-Schnittstelle` vor einem Write zu setzen.
