# The PEP 484 type hints stub file for the QtTest module.
#
# Generated by SIP 6.7.0
#
# Copyright (c) 2022 Riverbank Computing Limited <info@riverbankcomputing.com>
#
# This file is part of PyQt6.
#
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file.  Please review the
# following information to ensure the GNU General Public License version 3.0
# requirements will be met: http://www.gnu.org/copyleft/gpl.html.
#
# If you do not wish to use this file under the terms of the GPL version 3.0
# then you may purchase a commercial license.  For more information contact
# info@riverbankcomputing.com.
#
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

# Support for QDate, QDateTime and QTime.
import datetime
import enum
import typing

import PyQt6.sip
from PyQt6 import QtCore, QtGui, QtWidgets

# Convenient type aliases.
PYQT_SIGNAL = typing.Union[QtCore.pyqtSignal, QtCore.pyqtBoundSignal]
PYQT_SLOT = typing.Union[typing.Callable[..., None], QtCore.pyqtBoundSignal]

class QAbstractItemModelTester(QtCore.QObject):
    class FailureReportingMode(enum.Enum):
        QtTest = ...  # type: QAbstractItemModelTester.FailureReportingMode
        Warning = ...  # type: QAbstractItemModelTester.FailureReportingMode
        Fatal = ...  # type: QAbstractItemModelTester.FailureReportingMode
    @typing.overload
    def __init__(self, model: QtCore.QAbstractItemModel, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...
    @typing.overload
    def __init__(self, model: QtCore.QAbstractItemModel, mode: "QAbstractItemModelTester.FailureReportingMode", parent: typing.Optional[QtCore.QObject] = ...) -> None: ...
    def setUseFetchMore(self, value: bool) -> None: ...
    def failureReportingMode(self) -> "QAbstractItemModelTester.FailureReportingMode": ...
    def model(self) -> QtCore.QAbstractItemModel: ...

class QSignalSpy(QtCore.QObject):
    @typing.overload
    def __init__(self, signal: QtCore.pyqtBoundSignal) -> None: ...
    @typing.overload
    def __init__(self, obj: QtCore.QObject, signal: QtCore.QMetaMethod) -> None: ...
    def __delitem__(self, i: int) -> None: ...
    def __setitem__(self, i: int, value: typing.Iterable[typing.Any]) -> None: ...
    def __getitem__(self, i: int) -> typing.List[typing.Any]: ...
    def __len__(self) -> int: ...
    def wait(self, timeout: int = ...) -> bool: ...
    def signal(self) -> QtCore.QByteArray: ...
    def isValid(self) -> bool: ...

class QTest(PyQt6.sip.simplewrapper):
    class KeyAction(enum.Enum):
        Press = ...  # type: QTest.KeyAction
        Release = ...  # type: QTest.KeyAction
        Click = ...  # type: QTest.KeyAction
        Shortcut = ...  # type: QTest.KeyAction
    @typing.overload
    def qWaitForWindowExposed(self, window: QtGui.QWindow, timeout: int = ...) -> bool: ...
    @typing.overload
    def qWaitForWindowExposed(self, widget: QtWidgets.QWidget, timeout: int = ...) -> bool: ...
    @typing.overload
    def qWaitForWindowActive(self, window: QtGui.QWindow, timeout: int = ...) -> bool: ...
    @typing.overload
    def qWaitForWindowActive(self, widget: QtWidgets.QWidget, timeout: int = ...) -> bool: ...
    def qWait(self, ms: int) -> None: ...
    @typing.overload
    def mouseRelease(self, widget: QtWidgets.QWidget, button: QtCore.Qt.MouseButton, modifier: QtCore.Qt.KeyboardModifier = ..., pos: QtCore.QPoint = ..., delay: int = ...) -> None: ...
    @typing.overload
    def mouseRelease(self, window: QtGui.QWindow, button: QtCore.Qt.MouseButton, modifier: QtCore.Qt.KeyboardModifier = ..., pos: QtCore.QPoint = ..., delay: int = ...) -> None: ...
    @typing.overload
    def mousePress(self, widget: QtWidgets.QWidget, button: QtCore.Qt.MouseButton, modifier: QtCore.Qt.KeyboardModifier = ..., pos: QtCore.QPoint = ..., delay: int = ...) -> None: ...
    @typing.overload
    def mousePress(self, window: QtGui.QWindow, button: QtCore.Qt.MouseButton, modifier: QtCore.Qt.KeyboardModifier = ..., pos: QtCore.QPoint = ..., delay: int = ...) -> None: ...
    @typing.overload
    def mouseMove(self, widget: QtWidgets.QWidget, pos: QtCore.QPoint = ..., delay: int = ...) -> None: ...
    @typing.overload
    def mouseMove(self, window: QtGui.QWindow, pos: QtCore.QPoint = ..., delay: int = ...) -> None: ...
    @typing.overload
    def mouseDClick(self, widget: QtWidgets.QWidget, button: QtCore.Qt.MouseButton, modifier: QtCore.Qt.KeyboardModifier = ..., pos: QtCore.QPoint = ..., delay: int = ...) -> None: ...
    @typing.overload
    def mouseDClick(self, window: QtGui.QWindow, button: QtCore.Qt.MouseButton, modifier: QtCore.Qt.KeyboardModifier = ..., pos: QtCore.QPoint = ..., delay: int = ...) -> None: ...
    @typing.overload
    def mouseClick(self, widget: QtWidgets.QWidget, button: QtCore.Qt.MouseButton, modifier: QtCore.Qt.KeyboardModifier = ..., pos: QtCore.QPoint = ..., delay: int = ...) -> None: ...
    @typing.overload
    def mouseClick(self, window: QtGui.QWindow, button: QtCore.Qt.MouseButton, modifier: QtCore.Qt.KeyboardModifier = ..., pos: QtCore.QPoint = ..., delay: int = ...) -> None: ...
    @typing.overload
    def sendKeyEvent(self, action: "QTest.KeyAction", widget: QtWidgets.QWidget, code: QtCore.Qt.Key, ascii: str, modifier: QtCore.Qt.KeyboardModifier, delay: int = ...) -> None: ...
    @typing.overload
    def sendKeyEvent(self, action: "QTest.KeyAction", widget: QtWidgets.QWidget, code: QtCore.Qt.Key, text: str, modifier: QtCore.Qt.KeyboardModifier, delay: int = ...) -> None: ...
    def simulateEvent(self, widget: QtWidgets.QWidget, press: bool, code: int, modifier: QtCore.Qt.KeyboardModifier, text: str, repeat: bool, delay: int = ...) -> None: ...
    @typing.overload
    def keySequence(self, widget: QtWidgets.QWidget, keySequence: typing.Union[QtGui.QKeySequence, QtGui.QKeySequence.StandardKey, str, int]) -> None: ...
    @typing.overload
    def keySequence(self, window: QtGui.QWindow, keySequence: typing.Union[QtGui.QKeySequence, QtGui.QKeySequence.StandardKey, str, int]) -> None: ...
    @typing.overload
    def keyRelease(self, widget: QtWidgets.QWidget, key: QtCore.Qt.Key, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyRelease(self, widget: QtWidgets.QWidget, key: str, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyRelease(self, window: QtGui.QWindow, key: QtCore.Qt.Key, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyRelease(self, window: QtGui.QWindow, key: str, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyPress(self, widget: QtWidgets.QWidget, key: QtCore.Qt.Key, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyPress(self, widget: QtWidgets.QWidget, key: str, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyPress(self, window: QtGui.QWindow, key: QtCore.Qt.Key, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyPress(self, window: QtGui.QWindow, key: str, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyEvent(self, action: "QTest.KeyAction", widget: QtWidgets.QWidget, key: QtCore.Qt.Key, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyEvent(self, action: "QTest.KeyAction", widget: QtWidgets.QWidget, ascii: str, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyEvent(self, action: "QTest.KeyAction", window: QtGui.QWindow, key: QtCore.Qt.Key, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyEvent(self, action: "QTest.KeyAction", window: QtGui.QWindow, ascii: str, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    def keyClicks(self, widget: QtWidgets.QWidget, sequence: str, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyClick(self, widget: QtWidgets.QWidget, key: QtCore.Qt.Key, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyClick(self, widget: QtWidgets.QWidget, key: str, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyClick(self, window: QtGui.QWindow, key: QtCore.Qt.Key, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
    @typing.overload
    def keyClick(self, window: QtGui.QWindow, key: str, modifier: QtCore.Qt.KeyboardModifier = ..., delay: int = ...) -> None: ...
