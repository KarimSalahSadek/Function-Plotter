import FunctionPlotter
import pytest
from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api

@pytest.fixture
def window(qtbot):
    window = FunctionPlotter.Window()
    qtbot.addWidget(window)
    return window

def test_noInput(qtbot,window):
    qtbot.mouseClick(window.pltbtn, qt_api.QtCore.Qt.MouseButton.LeftButton)
    assert(window.info_box.toPlainText()=="Error!\nInvalid value for x_min!\nInvalid value for x_max!\nInvalid function!")

def test_minGTMax(qtbot,window):
    window.xmin_box.setText('10')
    window.xmax_box.setText('5')
    window.eqn_box.setText('x^2')
    qtbot.mouseClick(window.pltbtn, qt_api.QtCore.Qt.MouseButton.LeftButton)
    assert(window.info_box.toPlainText()=="Error!\nInvalid value for x_max!\nMax value cannot exceed Min value!")

def test_invalidXMax(qtbot,window):
    window.xmin_box.setText('5')
    window.xmax_box.setText('y')
    window.eqn_box.setText('x^2')
    qtbot.mouseClick(window.pltbtn, qt_api.QtCore.Qt.MouseButton.LeftButton)
    assert(window.info_box.toPlainText()=="Error!\nInvalid value for x_max!")

def test_invalidFunc(qtbot,window):
    window.xmin_box.setText('-5')
    window.xmax_box.setText('77')
    window.eqn_box.setText('print(x)')
    qtbot.mouseClick(window.pltbtn, qt_api.QtCore.Qt.MouseButton.LeftButton)
    assert(window.info_box.toPlainText()=="Error!\nInvalid function!")

def test_correctInputs(qtbot,window):
    window.xmin_box.setText('-10')
    window.xmax_box.setText('10')
    window.eqn_box.setText('5*x^3 + 2*x')
    qtbot.mouseClick(window.pltbtn, qt_api.QtCore.Qt.MouseButton.LeftButton)
    assert(window.info_box.toPlainText()=="Log:\nPlotting is successful!")

def test_overflow(qtbot,window):
    window.xmin_box.setText('0')
    window.xmax_box.setText('100')
    window.eqn_box.setText('x^1000')
    qtbot.mouseClick(window.pltbtn, qt_api.QtCore.Qt.MouseButton.LeftButton)
    assert(window.info_box.toPlainText()=="Log:\nA number may have exceeded the maximum of matplotlib")