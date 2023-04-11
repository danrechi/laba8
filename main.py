import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Shedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_shedule_tab()

        self._create_teachers_tab()

        self._create_subjects_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="timetable",
                                     user="postgres",
                                     password="2104",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Timetable")

        self.schedule_gbox = QGroupBox("timetable")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.schedule_gbox)

        self._create_timetable_table()

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.shedule_tab.setLayout(self.svbox)



    def _create_timetable_table(self):
        self.schedule_table = QTableWidget()
        self.schedule_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.schedule_table.setColumnCount(9)
        self.schedule_table.setHorizontalHeaderLabels(["id", "day", "subject", "room_numb",
                                                       "start_time", "end_time", "week"])
        self._update_timetable_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.schedule_table)
        self.schedule_gbox.setLayout(self.mvbox)

    def _update_timetable_table(self):
        self.cursor.execute("SELECT * FROM timetable ORDER BY week, id")
        records = list(self.cursor.fetchall())

        self.schedule_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")


            self.schedule_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.schedule_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.schedule_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.schedule_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.schedule_table.setItem(i, 4, QTableWidgetItem(str(r[4])))
            self.schedule_table.setItem(i, 5, QTableWidgetItem(str(r[5])))
            self.schedule_table.setItem(i, 6, QTableWidgetItem(str(r[6])))
            self.schedule_table.setCellWidget(i, 7, joinButton)
            self.schedule_table.setCellWidget(i, 8, deleteButton)

            joinButton.clicked.connect(lambda ch, num=i: self._update_db(num))
            deleteButton.clicked.connect(lambda ch, num=i: self._delete_from_db(num))

        joinButton = QPushButton("Join")
        self.schedule_table.setCellWidget(len(records), 7, joinButton)
        joinButton.clicked.connect(lambda ch, num=len(records): self._add_to_db(num))

        self.schedule_table.resizeRowsToContents()

#изменения в бд---
    def _add_to_db(self, num):
        row = list()
        for i in range(self.schedule_table.columnCount()):
            try:
                row.append(self.schedule_table.item(num, i).text())
            except:
                row.append(None)
        try:
            columns = ["id", "day", "subject", "room_numb", "start_time", "end_time", "week"]
            self.cursor.execute(f"INSERT INTO timetable({columns[0]}, {columns[1]}, {columns[2]}, {columns[3]},"
                                f" {columns[4]}, {columns[5]}, {columns[6]}) values('{row[0]}', '{row[1]}',"
                                f" '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}')")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _delete_from_db(self, num):
        row = list()
        for i in range(self.schedule_table.columnCount()):
            try:
                row.append(self.schedule_table.item(num, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"DELETE from timetable where id = '{row[0]}'")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _update_db(self, num):
        row = list()
        for i in range(self.schedule_table.columnCount()):
            try:
                row.append(self.schedule_table.item(num, i).text())
            except:
                row.append(None)
        try:
            columns = ["id", "day", "subject", "room_numb", "start_time", "end_time", "week"]
            for i in range(1, 7):
                self.cursor.execute(f"UPDATE timetable SET {columns[i]} = '{row[i]}' WHERE id = '{row[0]}'")
                self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")
#----


    def _create_teachers_tab(self):
        self.teachers_tab = QWidget()
        self.tabs.addTab(self.teachers_tab, "Teachers")

        self.teachers_gbox = QGroupBox("teacher")

        self.tvbox = QVBoxLayout()
        self.thbox1 = QHBoxLayout()
        self.thbox2 = QHBoxLayout()

        self.tvbox.addLayout(self.thbox1)
        self.tvbox.addLayout(self.thbox2)

        self.thbox1.addWidget(self.teachers_gbox)

        self._create_teachers_table()

        self.update_teachers_button = QPushButton("Update")
        self.thbox2.addWidget(self.update_teachers_button)
        self.update_teachers_button.clicked.connect(self._update_shedule)

        self.teachers_tab.setLayout(self.tvbox)

    def _create_teachers_table(self):
        self.teachers_table = QTableWidget()
        self.teachers_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teachers_table.setColumnCount(5)
        self.teachers_table.setHorizontalHeaderLabels(["id", "teacher", "subject"])

        self._update_teachers_table()

        self.tchbox = QVBoxLayout()
        self.tchbox.addWidget(self.teachers_table)
        self.teachers_gbox.setLayout(self.tchbox)

    def _update_teachers_table(self):
        self.cursor.execute("SELECT * FROM teacher ORDER BY ID")
        records = list(self.cursor.fetchall())

        self.teachers_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")

            self.teachers_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.teachers_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.teachers_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.teachers_table.setCellWidget(i, 3, joinButton)
            self.teachers_table.setCellWidget(i, 4, deleteButton)

            joinButton.clicked.connect(lambda ch, num=i: self._update_teacher_db(num))
            deleteButton.clicked.connect(lambda ch, num=i: self._delete_from_teach_db(num))

        joinButton = QPushButton("Join")
        self.teachers_table.setCellWidget(len(records), 3, joinButton)
        joinButton.clicked.connect(lambda ch, num=len(records): self._add_to_teach_db(num))

        self.teachers_table.resizeRowsToContents()

#db
    def _delete_from_teach_db(self, num):
        row = list()
        for i in range(self.teachers_table.columnCount()):
            try:
                row.append(self.teachers_table.item(num, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"DELETE from teacher where id = '{row[0]}'")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _add_to_teach_db(self, num):
        row = list()
        for i in range(self.teachers_table.columnCount()):
            try:
                row.append(self.teachers_table.item(num, i).text())
            except:
                row.append(None)
        try:
            columns = ["id", "full_name", "subject"]
            self.cursor.execute(f"INSERT INTO teacher({columns[0]}, {columns[1]}, {columns[2]}) values('{row[0]}',"
                                f" '{row[1]}', '{row[2]}')")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _update_teacher_db(self, num):
        row = list()
        for i in range(self.teachers_table.columnCount()):
            try:
                row.append(self.teachers_table.item(num, i).text())
            except:
                row.append(None)
        try:
            columns = ["id", "full_name", "subject"]
            for i in range(1, 2):
                self.cursor.execute(f"UPDATE teacher SET {columns[i]} = '{row[i]}' WHERE id = '{row[0]}'")
                self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")


    def _create_subjects_tab(self):
        self.subjects_tab = QWidget()
        self.tabs.addTab(self.subjects_tab, "Subjects")

        self.subjects_gbox = QGroupBox("subject")

        self.fvbox = QVBoxLayout()
        self.fhbox1 = QHBoxLayout()
        self.fhbox2 = QHBoxLayout()

        self.fvbox.addLayout(self.fhbox1)
        self.fvbox.addLayout(self.fhbox2)

        self.fhbox1.addWidget(self.subjects_gbox)

        self._create_subjects_table()

        self.update_subjects_button = QPushButton("Update")
        self.fhbox2.addWidget(self.update_subjects_button)
        self.update_subjects_button.clicked.connect(self._update_shedule)

        self.subjects_tab.setLayout(self.fvbox)

    def _create_subjects_table(self):
        self.subjects_table = QTableWidget()
        self.subjects_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subjects_table.setColumnCount(4)
        self.subjects_table.setHorizontalHeaderLabels(["id", "subject_name"])

        self._update_subjects_table()

        self.ffvbox = QVBoxLayout()
        self.ffvbox.addWidget(self.subjects_table)
        self.subjects_gbox.setLayout(self.ffvbox)

    def _update_subjects_table(self):
        self.cursor.execute("SELECT * FROM subject ORDER BY id")
        records = list(self.cursor.fetchall())

        self.subjects_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")

            self.subjects_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.subjects_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.subjects_table.setCellWidget(i, 2, joinButton)
            self.subjects_table.setCellWidget(i, 3, deleteButton)

            joinButton.clicked.connect(lambda ch, num=i: self._update_sub_db(num))
            deleteButton.clicked.connect(lambda ch, num=i: self._delete_from_sub_db(num))

        joinButton = QPushButton("Join")
        self.subjects_table.setCellWidget(len(records), 2, joinButton)
        joinButton.clicked.connect(lambda ch, num=len(records): self._add_to_sub_db(num))

        self.schedule_table.resizeRowsToContents()

#db
    def _delete_from_sub_db(self, num):
        row = list()
        for i in range(self.subjects_table.columnCount()):
            try:
                row.append(self.subjects_table.item(num, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"DELETE from subject where id = '{row[0]}'")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _add_to_sub_db(self, num):
        row = list()
        for i in range(self.subjects_table.columnCount()):
            try:
                row.append(self.subjects_table.item(num, i).text())
            except:
                row.append(None)
        try:
            columns = ["id", "subject_name"]
            self.cursor.execute(f"INSERT INTO subject({columns[0]}, {columns[1]}) values('{row[0]}', '{row[1]}')")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _update_sub_db(self, num):
        row = list()
        for i in range(self.subjects_table.columnCount()):
            try:
                row.append(self.subjects_table.item(num, i).text())
            except:
                row.append(None)
        try:
            columns = ["id", "subject_name"]
            for i in range(1, 2):
                self.cursor.execute(f"UPDATE subject SET {columns[i]} = '{row[i]}' WHERE id = '{row[0]}'")
                self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")


    def _update_shedule(self):
        self._update_timetable_table()
        self._update_teachers_table()
        self._update_subjects_table()






app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())