# Intelcom Performance Analysis

I got curious about how long it takes Intelcom (a courier) to deliver my packages once they send out the "On our way!" email.

A more full write-up: https://todays.pointless.click/projects/intelcom.html

# Requirements

Python >=3.6
requirements.txt

# Usage
```
python3 get_intelcom_metadata.py ./mailbox.mbox ./output.json

python3 calculate_stats.py ./output.json
```
