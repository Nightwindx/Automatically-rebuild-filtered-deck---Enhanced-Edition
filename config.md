## time (auto-rebuild timing)

Controls how often filtered decks rebuild when you add a note.

- null  → auto rebuild disabled (except for Anki startup/shutdown)
- 0     → rebuild every time you add a note  
- N     → rebuild at most once every N seconds when you add a note

Examples:

- { "time": null }
- { "time": 0 }
- { "time": 30 }
