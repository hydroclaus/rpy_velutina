# Stepper Motor / Schrittmotor

goal: control the stepper motor for moving a constant head tank up and down

I want to control this stepper engine
https://www.amazon.de/dp/B085SXDS2B?ref=fed_asin_title&th=1
with this TB6600 controller 
https://www.amazon.de/dp/B09CCZBFV8?ref=fed_asin_title&th=1


From the amazon description

    Produktbeschreibungen
    Schrittmotor-Parameter:
    Schrittwinkel: 1,8 Grad
    Motorflanschgröße: 42 mm.
    Motorlänge: 47 mm.
    Haltemoment: 1,2 N.m
    Stromstärke: 1,5 A.
    Widerstand: 0,8 Ohm
    Induktivität: 2,4 mH
    Rotor-Trägheit: 87,3 g.
    Kabel: 4 Stück.
    Verdrahtung:
    Schwarz: A+
    Grün: A-
    Rot: B+
    Blau: B-
    Linear-Stufen-Stellantrieb. Parameter:
    Effektive Reiselänge: 100 mm.
    Gesamtlänge: 265 mm.
    Typ: Lineare System-Form.
    Kugelschrauben-Typ: SFU1605 (Durchmesser: 16 mm, Schraubenabstand: 5 mm).
    Kugelschraube: C7
    Gewicht: 1415 g.
    Lieferumfang:
    1 x Linear-Stufenantrieb mit NEMA17-Schrittmotor.
    1 x Schrittmotor-Kabel.

## Resources
- [Raspberry Pi, Python, and a TB6600 Stepper Motor Driver : 9 Steps - Instructables](https://www.instructables.com/Raspberry-Pi-Python-and-a-TB6600-Stepper-Motor-Dri/)`
- [Schrittmotor-Steuerung mit TB6600-Treiber und Raspberry Pi](https://www.heimkino-praxis.de/leinwand-maskierung-schrittmotor-steuerung/)
- [Praxisbeispiele | Maxx](https://www.maxx-gmbh.com/produkte-sortiment-qualitaet-innovation/praxisbeispiele-loesungen-aus-der-realitaet/)

10000 Schritte (Steps) entspricht ~ 3,13 mm zurueckgelegter Strecke
20000 ~ 6,26 mm
30000 ~ 9,38 mm
40000 ~ 12,505 mm
50000 ~ 15,625 mm

--> ~ 3200 Schritte pro cm zurueckgelegter Strecke

ohne Rampe:
1000 Schritte a 1000 rpm --> 0,55 s
1000 Schritte a 800 rpm --> 0,61 s
1000 Schritte a 600 rpm --> 0,72 s
1000 Schritte a 400 rpm --> 0,96 s
1000 Schritte a 200 rpm --> 1,98 s
1000 Schritte a 100 rpm --> 3,32 s
1000 Schritte a 50 rpm --> 6,19 s
1000 Schritte a 10 rpm --> 30,18 s
1000 Schritte a 5 rpm --> 60,23 s
1000 Schritte a 2,5 rpm --> 120,22 s
1000 Schritte a 1 rpm --> 300,24 s



Ziel: ca. 12 cm pro h