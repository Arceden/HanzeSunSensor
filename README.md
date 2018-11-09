# Zonnescherm Project
Voor dit project van de Hanzehogeschool Groningen word er een systeem gemaakt dat automatisch of handmatig een zonnescherm kan bedienen doormiddel van een C en Python.

## Python
Voor het gebruik van de Python code moeten er wel verschillende Python packets worden geinstalleerd.

```
pip install dash
pip install dash-html-components
pip install dash-core-components
pip install pandas
pip install pyserial
```

Gelieve seriële port in app.py specificeren, in callbacks_home,py en callbacks_data.py. Vervolgens de juiste poort invullen.

In de terminal: python run.py om het bestand uit te voeren

## C
Op het moment kan het systeem alleen nog maar een simpele verbinding maken met de client als de client een willekeurige letter verstuurd.
Zodra een verbinding tot stand is gekomen, dan is het mogelijk om doormiddel van verschillende letter combinaties data op te vragen.

Voorbeeld:
```
[c] > a
[s] > Connected!
[c] > s
[s] > {type: settings, rotation: 0}
[c] > d
[s] > {type: current_data, rotation: 0, temperature: 14, light_intensity: 96}
[c] > x
[s] > Disconnected!
```
[s] = Systeem
[c] = Client

Op het moment is er nog geen sprake van een goede handshake protocol. Dat zal later nog toegevoegd worden.


## Arduino aansluiting
De componenten die nodig zijn voor het systeem zijn als volgt;
- Low Voltage Temperature Sensor
- Photoconductive Cell (GL5528)
- Arduino UNO
- LED

![Arduino aansluiting schema](https://raw.githubusercontent.com/Arceden/HanzeSunSensor/visualisation/Arduino_Project_bb.png)
