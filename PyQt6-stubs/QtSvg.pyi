# The PEP 484 type hints stub file for the QtSvg module.
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
from PyQt6 import QtCore, QtGui

# Convenient type aliases.
PYQT_SIGNAL = typing.Union[QtCore.pyqtSignal, QtCore.pyqtBoundSignal]
PYQT_SLOT = typing.Union[typing.Callable[..., None], QtCore.pyqtBoundSignal]

class QSvgGenerator(QtGui.QPaintDevice):
    def __init__(self) -> None: ...
    def metric(self, metric: QtGui.QPaintDevice.PaintDeviceMetric) -> int: ...
    def paintEngine(self) -> QtGui.QPaintEngine: ...
    @typing.overload
    def setViewBox(self, viewBox: QtCore.QRect) -> None: ...
    @typing.overload
    def setViewBox(self, viewBox: QtCore.QRectF) -> None: ...
    def viewBoxF(self) -> QtCore.QRectF: ...
    def viewBox(self) -> QtCore.QRect: ...
    def setDescription(self, description: str) -> None: ...
    def description(self) -> str: ...
    def setTitle(self, title: str) -> None: ...
    def title(self) -> str: ...
    def setResolution(self, resolution: int) -> None: ...
    def resolution(self) -> int: ...
    def setOutputDevice(self, outputDevice: QtCore.QIODevice) -> None: ...
    def outputDevice(self) -> QtCore.QIODevice: ...
    def setFileName(self, fileName: str) -> None: ...
    def fileName(self) -> str: ...
    def setSize(self, size: QtCore.QSize) -> None: ...
    def size(self) -> QtCore.QSize: ...

class QSvgRenderer(QtCore.QObject):
    @typing.overload
    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...
    @typing.overload
    def __init__(self, filename: str, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...
    @typing.overload
    def __init__(self, contents: QtCore.QByteArray, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...
    @typing.overload
    def __init__(self, contents: QtCore.QXmlStreamReader, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...
    def transformForElement(self, id: str) -> QtGui.QTransform: ...
    def setAspectRatioMode(self, mode: QtCore.Qt.AspectRatioMode) -> None: ...
    def aspectRatioMode(self) -> QtCore.Qt.AspectRatioMode: ...
    repaintNeeded: typing.ClassVar[QtCore.pyqtSignal]
    @typing.overload
    def render(self, p: QtGui.QPainter) -> None: ...
    @typing.overload
    def render(self, p: QtGui.QPainter, bounds: QtCore.QRectF) -> None: ...
    @typing.overload
    def render(self, painter: QtGui.QPainter, elementId: str, bounds: QtCore.QRectF = ...) -> None: ...
    @typing.overload
    def load(self, filename: str) -> bool: ...
    @typing.overload
    def load(self, contents: QtCore.QByteArray) -> bool: ...
    @typing.overload
    def load(self, contents: QtCore.QXmlStreamReader) -> bool: ...
    def animationDuration(self) -> int: ...
    def setCurrentFrame(self, a0: int) -> None: ...
    def currentFrame(self) -> int: ...
    def setFramesPerSecond(self, num: int) -> None: ...
    def framesPerSecond(self) -> int: ...
    def boundsOnElement(self, id: str) -> QtCore.QRectF: ...
    def animated(self) -> bool: ...
    @typing.overload
    def setViewBox(self, viewbox: QtCore.QRect) -> None: ...
    @typing.overload
    def setViewBox(self, viewbox: QtCore.QRectF) -> None: ...
    def viewBoxF(self) -> QtCore.QRectF: ...
    def viewBox(self) -> QtCore.QRect: ...
    def elementExists(self, id: str) -> bool: ...
    def defaultSize(self) -> QtCore.QSize: ...
    def isValid(self) -> bool: ...
