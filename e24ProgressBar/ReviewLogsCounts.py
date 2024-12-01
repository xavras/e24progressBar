from e24ProgressBar.ReviewLog import *
from aqt import mw

class ReviewEaseWages:
    def __init__(self, wrong: float, hard: float, ok: float, easy: float):
        self.wrong = wrong
        self.hard = hard
        self.ok = ok
        self.easy = easy

class ReviewLogsCounts:
    def __init__(self, easeWages: ReviewEaseWages):
        self.lastFetchedReviewId = self.__todayStartTime()
        reviewLogs = self.__fetchLogsFromDb()
        self.__set(reviewLogs)
        self.easeWages = easeWages

    @staticmethod
    def __todayStartTime() -> int:
        return (mw.col.sched.day_cutoff - 86400) * 1000

    def update(self):
        self.add(self.__fetchLogsFromDb())

    def reset(self):
        self.lastFetchedReviewId = self.__todayStartTime()
        self.__set(self.__fetchLogsFromDb())

    def toString(self):
        return ("wrong: {}\t     hard: {}\t     ok: {}\t     easy: {}"
                .format(self.wrong, self.hard, self.ok, self.easy))

    def __set(self, reviewLogs: list[ReviewLog]):
        self.wrong = len([x for x in reviewLogs if x.ease == ReviewEase.wrong])
        self.hard = len([x for x in reviewLogs if x.ease == ReviewEase.hard])
        self.ok = len([x for x in reviewLogs if x.ease == ReviewEase.ok])
        self.easy = len([x for x in reviewLogs if x.ease == ReviewEase.easy])

    def add(self, reviewLogs: list[ReviewLog]):
        self.wrong += len([x for x in reviewLogs if x.ease == ReviewEase.wrong])
        self.hard += len([x for x in reviewLogs if x.ease == ReviewEase.hard])
        self.ok += len([x for x in reviewLogs if x.ease == ReviewEase.ok])
        self.easy += len([x for x in reviewLogs if x.ease == ReviewEase.easy])

    def getSumValue(self) -> float:
        return (self.wrong * self.easeWages.wrong + self.hard * self.easeWages.hard
                + self.ok * self.easeWages.ok + self.easy * self.easeWages.easy)

    def __fetchLogsFromDb(self) -> list[ReviewLog]:
        sqlQuery =  "SELECT id, cid, type, ease FROM revlog WHERE id > ?"
        revlogsRows = mw.col.db.all(sqlQuery, self.lastFetchedReviewId)
        result = [ReviewLog(x[0], x[1], x[2], x[3]) for x in revlogsRows]
        if len(result) > 0:
            self.lastFetchedReviewId = result[-1].id
        return result