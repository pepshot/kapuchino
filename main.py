import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.table()

    def table(self):
        con = sqlite3.connect('coffee.db')

        cur = con.cursor()

        result = cur.execute(f"""select * from infa_cof""").fetchall()

        con.close()

        title = ['ID', 'Название сорта', 'Степень обжарки',
                 'Молотый/В зернах', 'Описание вкуса', 'Цена',
                 'Объем упаковки']

        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)

        index = 0
        for row in result:
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            hh = 0
            for elem in row:
                self.tableWidget.setItem(
                    index, hh, QTableWidgetItem(str(elem)))
                hh += 1
            index += 1

        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())