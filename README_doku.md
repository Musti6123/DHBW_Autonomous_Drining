# Dokumentation zu dem Projekt 


## 0. Projektbeschreibung
Dieses Projekt soll ein Auto autonom fahren lassen und ist in folgende 
Module eingeteilt:
Fahrspurerkennung, Pfadplanung, Querregelung und Längsregelung.

## 1. Anforderungen

1. **Fahrspurekennung**: Erkennen und Zuordnen der linken und rechten Fahrspurbegrenzungen.
2. **Pfadplannung**: Planung des zu fahrenden Pfads basierend auf den erkannten Fahrspurbegrenzungen.
3. **Querregelung**: Bestimmung des Lenkwinkels, um das Fahrzeug in der Spur zu halten.
4. **Längsregelung**: Steuerung der Fahrzeuggeschwindigkeit basierend auf dem geplanten Pfad und der aktuellen Fahrzeuggeschwindigkeit.

## 2. Vorgehensweise

1. Installation: Installieren der notwendigen Packete und Aufsetzen des Projektes bei GitHub
2. Implementierung: Entwicklung der einzelnen Module gemäß der spezifizierten Anforderungen
3. Testen: Durchführung von Tests der einzelnen Module, um die Funktionalität sicherzustellen
4. Zusammenführung der Module: Alle Module werden in der main.py zusammen ausgeführt, um das Auto autonom fahren zu lassen
5. Testen und Verbessern: Wenn das Auto noch nicht, wie gewünscht fährt, sollten noch Anpassungen gemacht werden.
6. Dokumentation: Erstellung einer umfassenden Dokumentation des Codes, einschließlich Readme-Datei und Inline-Kommentaren,
 die Ansätze, Gleichungen und Verbesserungen erläutert.


   
## 3. Umsetzung

Die Umsetzung wurde in verschiedene Module gegliedert:

### 3.1 Fahrspurerkennung

Die Fahrspurerkennung erfolgt durch die Verarbeitung von Bilddaten mithilfe der Klasse LaneDetection. 
Dabei werden Bilddaten verarbeitet, indem verschiedene Schritte durchlaufen werden. Zunächst erfolgt die Konvertierung
des Bildes in den HSV-Farbraum, gefolgt von der Anwendung von Schwellenwerten für Grautöne sowie der Kantenerkennung.
Danach wird die Fahrspurbegrenzungen erkannt. Die Positionen der linken und 
rechten Fahrspur wird in Form von Koordinatenpunkten gespeichert. 
Diese Informationen sind wichtig, um den Pfad zu planen.

### 3.2 Pfadplanung

Die Pfadplanung basiert auf den erkannten Fahrspurbegrenzungen [left_line_coordinates, right_line_coordinates] aus der 
Fahrspurerkennung.
Die Klasse "PathPlanning" empfängt die Positionen der linken und rechten Fahrspurbegrenzungen als Arrays. Anhand dieser Daten plant 
sie einen Pfad, der die Mitte zwischen den beiden Begrenzungen berechnet.

Wir nutzen zwei Funktionen, um den Pfad zu planen: "distance" berechnet die euklidische Distanz zwischen zwei Punkten,
während "midpoint" den Mittelpunkt zwischen den zwei Punkten berechnet.

Die Punkte der rechten Begrenzung werden analysiert, um einen Punkt zu identifizieren, der sich in einer 
bestimmten Entfernung zur linken Begrenzung befindet. 
Wenn ein geeigneter Mittelpunkt gefunden wird, wird er als nächster Punkt auf dem Pfad hinzugefügt.

Nachdem der Pfad geplant wurde, wird seine Krümmung berechnet. Dazu werden die absoluten Differenzen zwischen den 
x-Koordinaten aufeinanderfolgender Punkte im Pfad summiert. Dies ermöglicht eine Abschätzung der Krümmung des geplanten Pfads.

### 3.3 Querregelung
Die Querregelung bestimmt den optimalen Lenkwinkel, um das Fahrzeug innerhalb der Fahrspur auf dem Pfad zu halten. 
Dies wird durch den Stanley-Regler realisiert, der kontinuierlich die Abweichung des Fahrzeugs 
von der geplanten Pfadmitte überwacht und entsprechende Lenkeingaben generiert

Sie verwendet einen Gain-Parameter, um die Lenkung zu beeinflussen. Bei der Initialisierung werden verschiedene Parameter 
festgelegt, wie der Gain-Parameter und die Position des Fahrzeugs. 
Die Methode "find_nearest_point" lokalisiert den nächstgelegenen Punkt auf der Trajektorie zum aktuellen Standort des Fahrzeugs. 
Die Methode "calculate_path_angle" berechnet den Winkel des Pfads basierend auf dem nächsten Punkt und einem zukünftigen Punkt. 
Die Hauptmethode "control" steuert den Lenkwinkel des Fahrzeugs unter Berücksichtigung der aktuellen Trajektorie und Geschwindigkeit. 
Wenn das Fahrzeug nicht in Bewegung ist oder die control Methode weniger als 20 Mal aufgerufen wurde, erfolgt keine Lenkung. 
Die Rückgabewerte sind die berechneten Lenkwinkel des Fahrzeugs.

### 3.4 Längsregelung
Die Längsregelung steuert die Fahrzeuggeschwindigkeit basierend auf dem geplanten Pfad und der aktuellen Fahrzeuggeschwindigkeit, 
Dies geschieht mittels eines Proportional-Integral-Differential-Reglers (PID-Reglers). 
Nachdem die Parameter K<sub>p</sub>, K<sub>i</sub> und K<sub>d</sub> entsprechend eingestellt sind, 
ermöglicht die Klasse LongitudinalControl eine effektive und sichere Längsregelung des Fahrzeugs.

Mithilfe der Methode control wird die Geschwindigkeit des Fahrzeugs entsprechend des Reglerausgangs angepasst,  
wobei sowohl Beschleunigung als auch Bremsen je nach Abweichung von der Zielgeschwindigkeit gesteuert werden. 
Zusätzlich prognostiziert die Methode predict_target_speed die Zielgeschwindigkeit anhand der Straßenkrümmung und des Lenkwinkels. 
Zusammen gewährleisten diese Funktionen eine präzise und zuverlässige Geschwindigkeitsregelung während der Fahrt.


## 4. Anmerkungen
Obwohl das Projekt bereits bedeutende Fortschritte gemacht hat, gibt es noch Raum für Verbesserungen und zusätzliche Funktionen.
Einige Features, die wir geplant hatten, konnten nicht vollständig umgesetzt werden.


