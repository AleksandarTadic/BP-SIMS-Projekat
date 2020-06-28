from PySide2 import QtWidgets, QtGui, QtCore
import datetime
def dark_theme(app):
    dark_theme = QtGui.QPalette()
    dark_theme.setColor(QtGui.QPalette.Window, QtGui.QColor(14, 15, 17))
    dark_theme.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
    dark_theme.setColor(QtGui.QPalette.Base, QtGui.QColor(30, 32, 36))
    dark_theme.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(255, 255, 255))
    dark_theme.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
    dark_theme.setColor(QtGui.QPalette.Button, QtGui.QColor(14, 15, 17))
    dark_theme.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255))
    dark_theme.setColor(QtGui.QPalette.BrightText, QtGui.QColor(255, 255, 255))
    dark_theme.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(0, 0, 0))
    dark_theme.setColor(QtGui.QPalette.Highlight, QtGui.QColor(211, 211, 211))
    dark_theme.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(0, 0, 0))
    return app.setPalette(dark_theme)

def dark_moon_theme(app):
    dark_moon_theme = QtGui.QPalette()
    dark_moon_theme.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 10, 26))
    dark_moon_theme.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
    dark_moon_theme.setColor(QtGui.QPalette.Base, QtGui.QColor(0, 20, 51))
    dark_moon_theme.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(255, 255, 255))
    dark_moon_theme.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
    dark_moon_theme.setColor(QtGui.QPalette.Button, QtGui.QColor(0, 10, 26))
    dark_moon_theme.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255))
    dark_moon_theme.setColor(QtGui.QPalette.BrightText, QtGui.QColor(255, 255, 255))
    dark_moon_theme.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(0, 0, 0))
    dark_moon_theme.setColor(QtGui.QPalette.Highlight, QtGui.QColor(8, 151, 247))
    dark_moon_theme.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(255, 255, 255))
    return app.setPalette(dark_moon_theme)

def light_gray_theme(app):
    light_gray_theme = QtGui.QPalette()
    light_gray_theme.setColor(QtGui.QPalette.Window, QtGui.QColor(133, 133, 133))
    light_gray_theme.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0))
    light_gray_theme.setColor(QtGui.QPalette.Base, QtGui.QColor(211, 211, 211))
    light_gray_theme.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(0, 0, 0))
    light_gray_theme.setColor(QtGui.QPalette.Text, QtGui.QColor(0, 0, 0))
    light_gray_theme.setColor(QtGui.QPalette.Button, QtGui.QColor(150, 150, 150))
    light_gray_theme.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(0, 0, 0))
    light_gray_theme.setColor(QtGui.QPalette.BrightText, QtGui.QColor(0, 0, 0))
    light_gray_theme.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(0, 0, 0))
    light_gray_theme.setColor(QtGui.QPalette.Highlight, QtGui.QColor(150, 150, 150))
    light_gray_theme.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(0, 0, 0))
    return app.setPalette(light_gray_theme)

def set_theme_by_current_time(app):
    now = datetime.datetime.now()
    now_time = now.time()
    if now_time >= datetime.time(21,00) or now_time <= datetime.time(6,00):
        dark_theme(app)
    elif now_time >= datetime.time(18,00) or now_time <= datetime.time(21,00):
        dark_theme(app)
    else:
        light_gray_theme(app)
