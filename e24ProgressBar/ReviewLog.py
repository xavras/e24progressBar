from enum import Enum

class ReviewLog:
    def __init__(self, logId : int, cardId: int, cardTypeKey: int, easeKey: int):
        self.id = logId
        self.cardId = cardId
        self.cardType = CardType(cardTypeKey)
        self.ease = ReviewEase(easeKey)
    def toString(self):
        return ("{} [{}] {} {}"
                .format(self.id, self.cardId, self.cardType, self.ease))

# revlog - copied from documentation
# Type: 0 = new, 1 = learning, 2 = review, 3 = relearning * /
# Ease: which button you pushed to score your recall.
# based on documentation, BUT seems like there is only first option
#   - review:  1(wrong), 2(hard), 3(ok), 4(easy)
#   - learn/relearn:   1(wrong), 2(ok), 3(easy)
class CardType(Enum):
    new = 0
    learning = 1
    review = 2
    relearning = 3

class ReviewEase(Enum):
    wrong = 1
    hard = 2
    ok = 3
    easy = 4