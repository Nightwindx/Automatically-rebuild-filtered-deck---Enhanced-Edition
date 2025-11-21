This add-on is an enhanced fork of the original “Automatically rebuild filtered decks” add-on.
Original: https://ankiweb.net/shared/info/1997713323

Adds “Rebuild All” and “Empty All” buttons to the main deck screen to rebuild or empty all filtered decks at once.

New Features 

Automatically rebuilds all filtered decks on Anki startup and shutdown.
Filtered decks are refreshed when you open or close your profile.

Automatic rebuild when adding new cards
Optionally rebuild filtered decks after adding notes.

Configurable rebuild timing
Set a timer (in seconds) to limit how often auto-rebuild happens:

null → off (except for Anki startup/shutdown)

0 → rebuild every time you add a card

N → rebuild at most once every N seconds after you add a card

Examples:

- { "time": null }
- { "time": 0 }
- { "time": 30 }

These improvements make filtered decks update themselves reliably whether you add cards, start Anki, or close Anki — while still allowing manual “Rebuild All” and “Empty All” actions.
