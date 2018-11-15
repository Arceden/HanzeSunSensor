# Zonnescherm Project
Voor dit project van de Hanzehogeschool Groningen word er een systeem gemaakt dat automatisch of handmatig een zonnescherm kan bedienen doormiddel van een C en Python.

## Python
### Installatie
Voor het gebruik van de Python code moeten er wel verschillende Python pakketten worden geinstalleerd.
```
pip install dash
pip install dash-html-components
pip install dash-core-components
pip install pandas
pip install pyserial
```

### Gebruik
Om gebruik te maken van het Python systeem moet je in het serialv2 folder het bestand run.py starten. Bij het eerste gebruik zal het systeem vragen voor een communicatie port(USB), dit hoeft maar eenmalig te worden gedaan aangezien de Arduino.py klasse het zal onthouden voor de volgende keren. Het systeem heeft Python 3.x of hoger nodig om te kunnen starten.

## C
Het C systeem draait op een Arduino Uno (Atmega328P) en maakt gebruik van verschillende componenten. Voor informatie over de componenten, kijk naar het hoofdstuk "Arduino Aansluiting". 
Communicatie tussen Python en C werkt met een "CallForData" protocol, zo is het mogelijk om data op te vragen vanuit Python door een ASCII karakter te sturen zoals 'd' of 's'.

Voorbeeld:
```
[client] > d
[system] > {'type': 'current_data', 'rotation': 0, 'temperature': 164, 'light_intensity': 46}
[client] > s
[system] > {'type': 'settings', 'manual': 1, 'debug': 1, 'rotation': 0, 'temperature':{'max': 50, 'min': 0}, 'light':{'max': 50, 'min': 0}, 'extension':{'max': 50, 'min': 0}}
[client] > exth 180
[client] > s
[system] > {'type': 'settings', 'manual': 1, 'debug': 1, 'rotation': 0, 'temperature':{'max': 50, 'min': 0}, 'light':{'max': 50, 'min': 0}, 'extension':{'max': 180, 'min': 0}}
```

### Commandos
Voor de meeste variabelen zijn er meerdere POST commandos. De commando waarbij het eindigd met een 'h' is de maximale waarde van de variabele. En voor de commando waarbij het eindigd met een 'l' is de minimale waarde van de variabele.
```
GET commandos:
  d
  s
POST commandos:
  tmph <waarde>
  tmpl <waarde>
  exth <waarde>
  extl <waarde>
  luxh
  luxl
  manu
  debg
```

## Arduino aansluiting
De componenten die nodig zijn voor het systeem zijn als volgt;
- Arduino UNO
- Low Voltage Temperature Sensor
- Photoconductive Cell (GL5528)
- HC-SR04
- LED (green)
- LED (yellow)
- LED (red)

![Arduino aansluiting schema](https://raw.githubusercontent.com/Arceden/HanzeSunSensor/visualisation/Arduino_Project_bb.png)
