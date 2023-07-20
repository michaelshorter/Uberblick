#!/bin/bash
arecord --list-devices & sudo python3 main.py & cd AzureSpeechCC && /home/wordcloud/.dotnet/dotnet run & sleep 10s && sudo python3 write_to_oled.py
