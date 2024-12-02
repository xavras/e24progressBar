import math
from aqt import QDockWidget, QProgressBar, QWidget, QLabel
from aqt.qt import QVBoxLayout, QHBoxLayout
from e24ProgressBar.ReviewLogsCounts import *

class ProgressBarsWidget:
    progressStepMaxValue = 50
    dayProgressMaxValue = 500
    dayProgressMaxSteps = dayProgressMaxValue/progressStepMaxValue
    reviewEaseWages = ReviewEaseWages(0.5, 1.0, 1.0, 1.0)

    height = 80
    mainProgressBarHeight = 40
    completedMainProgressBoxStyle = """QLabel {
                border: 1px solid #061a40;
                border-radius: 0px;
                background-color : #3a6ea5;
                qproperty-alignment: AlignCenter;
            }"""
    emptyMainProgressBoxStyle = """QLabel {
                border: 1px solid #061a40;
                border-radius: 0px;
                background-color : #c0c0c0;
                qproperty-alignment: AlignCenter;
            }"""

    def __init__(self):
        self.reviewLogsCounts = ReviewLogsCounts(self.reviewEaseWages)

        self.dockWidget = QDockWidget()
        self.titleWidget = QWidget()
        contentWidget = QWidget()
        boxLayout = QVBoxLayout(contentWidget)
        contentWidget.setFixedHeight(self.height)

        self.mainProgressBarContentWidget = QWidget()
        self.mainProgressBarContentWidget.setFixedHeight(self.mainProgressBarHeight)
        self.mainProgressBarLayout = QHBoxLayout(self.mainProgressBarContentWidget)
        self.mainProgressBarSteps = self.__generateAndAddMainProgressBarSteps(
            self.mainProgressBarLayout)

        self.partialProgressBar = QProgressBar()
        self.partialProgressBar.setRange(0, 100)

        boxLayout.addWidget(self.mainProgressBarContentWidget)
        boxLayout.addWidget(self.partialProgressBar)
        self.dockWidget.setWidget(contentWidget)
        self.dockWidget.setTitleBarWidget(self.titleWidget)

    def __generateAndAddMainProgressBarSteps(self, dockingLayout: QHBoxLayout)\
            -> list[QLabel]:
        result = []
        for i in range(int(self.dayProgressMaxSteps)):
            stepLabel = QLabel()
            stepLabel.setText(str((i + 1) * self.progressStepMaxValue))
            stepLabel.setStyleSheet(self.emptyMainProgressBoxStyle)
            result.append(stepLabel)
            dockingLayout.addWidget(stepLabel)
        return result

    def update(self, reset: bool = False):
        if reset:
            self.reviewLogsCounts.reset()
        else:
            self.reviewLogsCounts.update()

        reviewLogsSumValue = self.reviewLogsCounts.getSumValue()
        self.partialProgressBar.setValue(self.__getMotivatingProgressValue(
            reviewLogsSumValue / self.progressStepMaxValue) * 100)
        self.partialProgressBar.setFormat(self.reviewLogsCounts.toString())

        completedMainProgressBoxes = math.floor(reviewLogsSumValue
                                                / self.progressStepMaxValue)
        completedMainProgressBoxesToMark = (completedMainProgressBoxes
                                            % self.dayProgressMaxSteps)
        if (completedMainProgressBoxesToMark == 0 and
                completedMainProgressBoxes > self.dayProgressMaxSteps):
            completedMainProgressBoxesToMark = self.dayProgressMaxSteps

        if completedMainProgressBoxes > self.dayProgressMaxSteps:
            completedDailyIterations = math.floor(completedMainProgressBoxes
                                           / self.dayProgressMaxSteps)
            if completedMainProgressBoxesToMark == self.dayProgressMaxSteps:
                completedDailyIterations -= 1
            for i, step in enumerate(self.mainProgressBarSteps):
                step.setText(str(
                    int(((completedDailyIterations * self.dayProgressMaxSteps)
                                  + i + 1) * self.progressStepMaxValue)))

        for i, step in enumerate(self.mainProgressBarSteps):
            if i < completedMainProgressBoxesToMark:
                step.setStyleSheet(self.completedMainProgressBoxStyle)
            else:
                step.setStyleSheet(self.emptyMainProgressBoxStyle)

    motivatingPart = 0.2
    motivatingPartScalar = 1.5
    mainPart = 1 - motivatingPart
    mainPartScalar = 1 / (mainPart * 1.0 + motivatingPart * motivatingPartScalar)
    mainPartValue = mainPart * mainPartScalar
    def __getMotivatingProgressValue(self, srcValue: float) -> float:
        srcValue = srcValue % 1
        if srcValue <= self.mainPart:
            return srcValue * self.mainPartScalar
        else:
            return (self.mainPartValue
                    + (srcValue - self.mainPart) * self.motivatingPartScalar)