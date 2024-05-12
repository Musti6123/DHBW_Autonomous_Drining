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

1. Installation: Installieren der notwendigen Packages und Ausetzen des Projektes bei GitHub
2. Implementierung: Entwicklung der einzelnen Module gemäß der spezifizierten Anforderungen
3. Testen: Durchführung von Tests der einzelnen Module, um die Funktionalität sicherzustellen
4. Zusammenführung der Module: Alle Module werden in der main.py zusammen ausgeführt, um das Auto autonom fahren zu lassen
5. Testen und Verbessern: Wenn das Auto noch nicht, wie gewünscht fährt, sollten noch Anpassungen gemacht werden.
6. Dokumentation: Erstellung einer umfassenden Dokumentation des Codes, einschließlich Readme-Datei und Inline-Kommentaren,
 die Ansätze, Gleichungen und Verbesserungen erläutert.





## 3. Umsetzung

Die Umsetzung wurde in verschiedene Module gegliedert:

### 3.1 Fahrspurerkennung

Die Fahrspurerkennung erfolgt durch die Verarbeitung von Bilddaten mithilfe der Klasse  LaneDetection. 
Dabei werden Bilddaten verarbeitet, indem verschiedene Schritte durchlaufen werden. Zunächst erfolgt die Konvertierung
des Bildes in den HSV-Farbraum, gefolgt von der Anwendung von Schwellenwerten für Grautöne sowie der Kantenerkennung.
Danach wird die Fahrspurbegrenzungen erkannt. Die Positionen der linken und 
rechten Fahrspur wird in Form von Koordinatenpunkten gespeichert. 
Diese Informationen sind wichtig, um den Pfad für das autonome Fahrzeug zu planen.

### 3.2 Pfadplanung

Die Pfadplanung basiert auf den erkannten Fahrspurbegrenzungen [left_line_coordinates, right_line_coordinates] aus der .
Fahrspurerkennung.
Die Klasse "PathPlanning" empfängt die Positionen der linken und rechten Fahrspurbegrenzungen als Arrays. Anhand dieser Daten plant 
sie einen Pfad, der die Mitte zwischen den beiden Begrenzungen berechnet.

Wir nutzen zwei Funktionen, um den Pfad zu planen: "distance" berechnet die euklidische Distanz zwischen zwei Punkten,
während "midpoint" den Mittelpunkt zwischen zwei Punkten berechnet.

Die Punkte der rechten Begrenzung werden analysiert, um einen Punkt zu identifizieren, der sich in einer 
bestimmten Entfernung zur linken Begrenzung befindet. 
Wenn ein geeigneter Punkt gefunden wird, wird der Mittelpunkt zwischen diesem Punkt und dem entsprechenden Punkt auf 
der linken Begrenzung als nächster Punkt auf dem Pfad hinzugefügt.

Nachdem der Pfad geplant wurde, wird seine Krümmung berechnet. Dazu werden die absoluten Differenzen zwischen den 
x-Koordinaten aufeinanderfolgender Punkte im Pfad summiert. Dies ermöglicht eine Abschätzung der Krümmung des geplanten Pfads.

### 3.3 Querregelung
Die Querregelung bestimmt den optimalen Lenkwinkel, um das Fahrzeug innerhalb der Fahrspur auf dem Pfad zu halten. 
Dies wird durch den Stanley-Regler realisiert, der

### 3.4 Längsregelung
Die Längsregelung steuert die Fahrzeuggeschwindigkeit basierend auf dem geplanten Pfad und der aktuellen Fahrzeuggeschwindigkeit.
Die Längsregelung wird mit dem PID-Regler umgesetzt. 


## 4. Anmerkungen
Obwohl das Projekt bereits bedeutende Fortschritte gemacht hat, gibt es noch Raum für Verbesserungen und zusätzliche Funktionen.
Einige Features, die wir geplant hatten, konnten unter anderem aus zeitlichen Gründen nicht umgesetzt werden.
Zum Beispiel war in der Pfadplanung geplant, einen sportlicheren Pfad abzufahren, der nicht immer der Mitte der Fahrbahn entspricht,
sondern die Kurve sportlich schneidet. 
Des Weiteren gab es große Probleme in der Lenkung, wie unter anderem auch in der Simulation gezeigt ist.

