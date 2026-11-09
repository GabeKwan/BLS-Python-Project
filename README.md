This project is an interactive, terminal-based, clinical training projects built in Python. The system functions as a CPR pacing assistant that emits dual-frequency audio cues to maintain American Heart Association compression rates while gathering precision tracking metrics to put down performance metrics.
Utilizes low-lag sound frequencies (`winsound`) to distinguish compression rhythms (110 BPM / 1200Hz) from procedural changes like Rescue Breath cycle (800Hz) and Pulse Checks (400Hz)
Calculates mathematical accuracy variants across compression strokes against a 0.545 second target window, translating error percentages into an overall performance score via the `statistics` code.
Dumps active logging blacks (including microsceond-accurate timestamps and telemetry gaps) into a comma-seperated dashboard file (`cpr_session_log.csv`).
Implements programmed logic traps to automatically trigger diagnostic pulse checkpoints every 5 resuscitations cycles.
Python 3.15+
`csv`, `os`, `time`, `statistics`, `datetime`
`winsound` (Windows Native OS API)
Launch the training link directly using your python driver terminal:  
```bash
   python main.py
   ```
