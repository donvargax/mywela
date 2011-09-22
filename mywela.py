#!/usr/bin/python

# Author: Surakarn Samkaew <tonkla@gmail.com>
# Released under the MIT license.
 
import datetime
import os
import sys

from PySide import QtCore, QtGui, QtSql

from ui_main import Ui_Main
from ui_dialog import Ui_Dialog


class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.ui = Ui_Main()
        self.ui.setupUi(self)

        self.ui.lcdTimer.display('00:00:00')

        self.bufferedTime = 0
        self.elapsed = QtCore.QTime()
        self.time = QtCore.QTime()
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updateTime)

        self.model = QtSql.QSqlQueryModel()
        self.model.setQuery("SELECT name FROM projects WHERE is_active=1")
        self.ui.cboProjects.setModel(self.model)

    @QtCore.Slot()
    def on_btnStartStop_clicked(self):
        if self.timer.isActive():
            self.ui.btnStartStop.setText('S&tart')
            self.ui.btnReset.setEnabled(True)
            self.bufferedTime += self.time.elapsed()
            self.timer.stop()
        else:
            self.ui.btnStartStop.setText('S&top')
            self.ui.btnReset.setEnabled(False)
            self.time.restart()
            self.timer.start(41)

    @QtCore.Slot()
    def on_btnReset_clicked(self):
        self.resetTimer()

    @QtCore.Slot()
    def on_btnSave_clicked(self):
        query = QtSql.QSqlQuery()
        q = "CREATE TABLE IF NOT EXISTS logs( \
                project VARCHAR(50) NOT NULL, \
                time_used INTEGER, \
                created_at DATETIME)"
        query.exec_(q)

        project_name = self.ui.cboProjects.currentText()
        q = "SELECT pid FROM projects WHERE name='%s'" % project_name
        query.exec_(q)
        query.next()
        project_id = query.value(0)
        time_used = (self.elapsed.hour() * 60 * 60) + (self.elapsed.minute() * 60) + self.elapsed.second()
        if time_used > 0:
            q = "INSERT INTO logs VALUES(%d, %d, '%s')" % (project_id, time_used, datetime.datetime.now())
            query.exec_(q)

        self.resetTimer()

    @QtCore.Slot()
    def on_btnQuit_clicked(self):
        QtGui.qApp.quit()

    @QtCore.Slot()
    def on_btnManage_clicked(self):
        dialog = ProjectsManagementDialog()
        if not dialog.exec_():
            self.updateProjectsList()

    def resetTimer(self):
        self.bufferedTime = 0
        self.time.restart()
        self.ui.lcdTimer.display('00:00:00')

    def updateTime(self):
        self.elapsed.setHMS(0, 0, 0, 0)
        self.elapsed = self.elapsed.addMSecs(self.time.elapsed())
        self.elapsed = self.elapsed.addMSecs(self.bufferedTime)
        text = self.elapsed.toString('hh:mm:ss')
        self.ui.lcdTimer.display(text)

    def updateProjectsList(self):
        self.model.setQuery("SELECT name FROM projects WHERE is_active=1")
        self.ui.cboProjects.setModel(self.model)


class ProjectsManagementDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ProjectsManagementDialog, self).__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        query = QtSql.QSqlQuery()
        q = "CREATE TABLE IF NOT EXISTS projects( \
                pid INTEGER PRIMARY KEY AUTOINCREMENT, \
                name VARCHAR(50) UNIQUE NOT NULL CHECK(name!=''), \
                is_active BOOLEAN DEFAULT 1)"
        query.exec_(q)

        self.model =  QtSql.QSqlTableModel()
        self.model.setTable("projects")
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.select()
        #self.model.removeColumn(0) # removeColumn() is a BUG of Qt (last tested on v4.7.0)
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "PID")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Project")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Active")

        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setColumnHidden(0, True) # use this to avoid removeColumn() bug
        self.ui.tableView.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.ui.tableView.resizeColumnsToContents()

    @QtCore.Slot()
    def on_btnNew_clicked(self):
        self.model.insertRecord(-1, QtSql.QSqlRecord())

    @QtCore.Slot()
    def on_btnDelete_clicked(self):
        selmodel = self.ui.tableView.selectionModel()
        selected = selmodel.selectedIndexes()
        if len(selected) > 0:
            self.model.removeRows(selected[0].row(), 1)

    @QtCore.Slot()
    def on_btnSubmit_clicked(self):
        self.model.database().transaction()
        if self.model.submitAll():
            self.model.database().commit()
        else:
            self.model.database().rollback()
            QtGui.QMessageBox.warning(self, "Error", "%s" % self.model.lastError().text())

    @QtCore.Slot()
    def on_btnRevert_clicked(self):
        self.model.revertAll()

    @QtCore.Slot()
    def on_btnClose_clicked(self):
        self.close()


def connect_db():
    data_dir = '%s/.mywela' % os.path.expanduser('~')
    try:
        os.mkdir(data_dir)
    except:
        pass
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('%s/mywela.sqlite3' % data_dir)
    if not db.open():
        QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
            QtGui.qApp.tr("Unable to establish a database connection.\n"
                          "This application needs SQLite support. Please read "
                          "the Qt SQL driver documentation for information "
                          "how to build it.\n\nClick Cancel to exit."),
            QtGui.QMessageBox.Cancel, QtGui.QMessageBox.NoButton)
    return False

if not QtSql.QSqlDatabase.isOpen(QtSql.QSqlDatabase.database()):
    connect_db()

app = QtGui.QApplication(sys.argv)
widget = MainWidget()
widget.show()
sys.exit(app.exec_())
