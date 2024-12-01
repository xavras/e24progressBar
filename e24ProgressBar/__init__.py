# import the main window object (mw) from aqt
from aqt import gui_hooks
# import all of the Qt GUI library
from aqt.qt import *
# import the "show info" tool from utils.py
from aqt.utils import showInfo

from e24ProgressBar.ProgressBarsWidget import *
from e24ProgressBar.ReviewLogsCounts import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction(text) -> None:
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.stats().todayStats()
    # show a message box
    showInfo("Card count: {0}".format(text))

def getCountFunc() -> None:
    remainCount = {}
    doneCount = {}
    totalCount = {}

    todayCutoff = (mw.col.sched.day_cutoff - 86400) * 1000
    cards = mw.col.db.first("""
            select
            sum(case when ease >=1 then 1 else 0 end) /* cards */
            from revlog where id > ? """, todayCutoff)
    cards = cards[0] if cards and cards[0] is not None else 0

    showInfo("Cards count: {0}".format(cards))
    for node in mw.col.sched.deck_due_tree().children:
        showInfo(("{0} [{1}, {2}]\n" +
                 "Counts: R = {3}, L = {4}, N = {5}\n" +
                 "Intraday: learning = {6}\n" +
                 "Uncapped: R = {7}, InL = {8}, N = {9}\n" +
                 "Total: inDeck = {10}, InclChildren = {11}").format(node.name,
                    node.deck_id, node.level, node.review_count, node.learn_count,
                    node.new_count, node.intraday_learning, node.review_uncapped,
                    node.interday_learning_uncapped, node.new_uncapped,
                    node.total_in_deck, node.total_including_children))

# revlog Type: 0 = new, 1 = learning, 2 = review, 3 = relearning * /
def getCountFuncFor(cardType):
    todayCutoff = (mw.col.sched.day_cutoff - 86400) * 1000
    cards = mw.col.db.first("""select sum(case when ease >=1 then 1 else 0 end) /* cards */
            from revlog where type = """ + str(cardType) + """ AND id > ? """,
    todayCutoff)
    cards = cards[0] if cards and cards[0] is not None else 0
    return cards

def printCounts():
    countO = getCountFuncFor(0)
    count1 = getCountFuncFor(1)
    count2 = getCountFuncFor(2)
    count3 = getCountFuncFor(3)
    showInfo("Cards count:\n0 = {0}\n1 = {1}\n2 = {2}\n3 = {3}"
             .format(countO, count1, count2, count3))

def dockWidget(progressBarsWidget: ProgressBarsWidget):
    dockingArea = Qt.DockWidgetArea.TopDockWidgetArea
    mw.addDockWidget(dockingArea, progressBarsWidget.dockWidget)
    mw.web.setFocus()

def onGuiShowQuestion(*args,**kwargs):
    progressBarsWidget.update()

def onGuiUndoStateChanged(*args, **kwargs):
    progressBarsWidget.update(True)

def onMainWindowInit(*args,**kwargs):
    global progressBarsWidget
    progressBarsWidget = ProgressBarsWidget()
    dockWidget(progressBarsWidget)
    progressBarsWidget.update()

try:
    progressBarsWidget = None

    gui_hooks.reviewer_did_show_question.append(onGuiShowQuestion)
    gui_hooks.state_did_undo.append(onGuiUndoStateChanged)
    gui_hooks.main_window_did_init.append(onMainWindowInit)

except Exception as e:
    showInfo("Error: %s" % e)