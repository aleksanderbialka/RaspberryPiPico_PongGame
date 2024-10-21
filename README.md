# RaspberryPiPico_PongGame

## Gra Pong na Raspberry Pi Pico

Projekt jest implementacją klasycznej gry Pong z użyciem mikrokontrolera Raspberry Pi Pico oraz wyświetlacza LCD ST7735. Gra pozwala na rozgrywkę jednoosobową (gracz vs komputer) lub dwuosobową, gdzie dwaj gracze kontrolują paletki poprzez potencjometry i próbują zdobyć punkty, odbijając piłkę.

## Opis projektu

Gra Pong jest cyfrową wersją klasycznej gry:
- Dwóch graczy (lub jeden gracz i komputer) kontrolują paletki po przeciwnych stronach ekranu.
- Piłka porusza się po ekranie, odbijając od paletek i ścian.
- Gracz zdobywa punkt, jeśli piłka minie paletkę przeciwnika.
- Gra kończy się, gdy któryś z graczy zdobędzie 10 punktów.

Projekt został zrealizowany w ramach modułu "Systemy wbudowane" na Wydziale Nauk Ścisłych i Technicznych Uniwersytetu Śląskiego.

## Wykorzystane komponenty
- **Język**: Python (MicroPython)
- Raspberry Pi Pico WH
- Wyświetlacz LCD ST7735 1.8" TFT (interfejs SPI)
- Dwa potencjometry (do sterowania paletkami)
- Przycisk Tact (do rozpoczęcia gry)
- Dioda LED (do sygnalizacji trybu jednoosobowego)
- Rezystory 100kΩ (do integracji obwodu)

## Układ elektryczny

<img width="727" alt="image" src="https://github.com/user-attachments/assets/588b36b7-a33f-4d71-9b64-84e26ed5fde1">

## Schemat poglądowy

<img width="504" alt="image" src="https://github.com/user-attachments/assets/0e00b109-5db6-4d28-ab97-03c44f4a920e">

## Demo wideo
Krótki filmik prezentujący działanie gry w trybie jednoosobowym oraz dwuosobowym znajduje się [tutaj](https://uniwersytetslaski-my.sharepoint.com/:v:/g/personal/aleksander_bialka_o365_us_edu_pl/EcVAcoqXlBRAvESi_mX0ndUB-BSl-xXuaQJexs0UD5FreQ?e=eprgZE&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D).

