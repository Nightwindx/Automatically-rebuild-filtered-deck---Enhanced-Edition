# -*- coding: utf-8 -*-
# See github page to report issues or to contribute:
# https://github.com/Arthaey/anki-rebuild-all
#
# Also available for Anki at https://ankiweb.net/shared/info/1639597619
#
# Contributors:
# - @Arthaey
# - @ankitest
# - @ArthurMilchior


import time
from anki.lang import _
from anki.hooks import wrap, addHook
from aqt import mw, gui_hooks
from aqt.deckbrowser import DeckBrowser
from aqt.utils import tooltip
from .config import getUserOption

def _updateFilteredDecks(actionFuncName):
    dynDeckIds = [ d["id"] for d in mw.col.decks.all() if d["dyn"] ]
    count = len(dynDeckIds)

    if not count:
        tooltip("No filtered decks found.")
        return

    # should be one of "rebuildDyn" or "emptyDyn"
    actionFunc = getattr(mw.col.sched, actionFuncName)

    mw.checkpoint("{0} {1} filtered decks".format(actionFuncName, count))
    mw.progress.start()
    [ actionFunc(did) for did in sorted(dynDeckIds) ]
    mw.progress.finish()
    tooltip("Updated {0} filtered decks.".format(count))

    mw.reset()


def _handleFilteredDeckButtons(self, url):
    if url in ["rebuildDyn", "emptyDyn"]:
        _updateFilteredDecks(url)


def _addButtons(self):
    drawLinks = [
        ["", "rebuildDyn", _("Rebuild All")],
        ["", "emptyDyn", _("Empty All")]
    ]
    # don't duplicate buttons every click
    if drawLinks[0] not in self.drawLinks:
        self.drawLinks += drawLinks

DeckBrowser._drawButtons = wrap(DeckBrowser._drawButtons, _addButtons, "before")
DeckBrowser._linkHandler = wrap(DeckBrowser._linkHandler, _handleFilteredDeckButtons, "after")

# --- automatic rebuild on profile open/close ---

def rebuild_on_profile_loaded():
    _updateFilteredDecks("rebuildDyn")

def rebuild_on_profile_unloaded():
    _updateFilteredDecks("rebuildDyn")

addHook("profileLoaded", rebuild_on_profile_loaded)
addHook("unloadProfile", rebuild_on_profile_unloaded)

# --- automatic rebuild when adding cards ---

last_rebuild_ts = None

def maybe_rebuild_on_add(note):
    """
    Called after a note was added via the Add dialog.
    """
    global last_rebuild_ts

    delta = getUserOption("time")
    # time == null  → feature disabled
    if delta is None:
        return

    now = time.time()

    # time <= 0  → rebuild on every add
    if delta <= 0:
        _updateFilteredDecks("rebuildDyn")
        last_rebuild_ts = now
        return

    # time > 0 → rebuild at most once every `delta` seconds
    if last_rebuild_ts is None or now - last_rebuild_ts >= delta:
        _updateFilteredDecks("rebuildDyn")
        last_rebuild_ts = now

gui_hooks.add_cards_did_add_note.append(maybe_rebuild_on_add)
