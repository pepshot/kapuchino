import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.table()
        self.pushButton.clicked.connect(self.new_window)
        self.pushButton_2.clicked.connect(self.edit_zapis)

    def edit_zapis(self):
        self.a = Edition()
        self.a.show()
        self.close()

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

    def new_window(self):
        self.a = Donw()
        self.a.show()
        self.close()


class Donw(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm1.ui', self)
        self.pushButton.clicked.connect(self.table)

    def table(self):
        name = self.lineEdit.text()
        step_proj = self.spinBox.text()
        molot_v_zern = self.lineEdit_2.text()
        vkus = self.lineEdit_3.text()
        zena = self.lineEdit_4.text()
        upakovka = self.lineEdit_5.text()

        con = sqlite3.connect('coffee.db')
        cur = con.cursor()

        result = cur.execute(f"""insert into infa_cof(sort,
        projarka, molotiyzerna, vkus, zena, obuem)
        values ('{name}', '{step_proj}', '{molot_v_zern}', '{vkus}', '{zena}',
        '{upakovka}')""")

        con.commit()
        con.close()

        self.a = MyWidget()
        self.a.show()
        self.close()


class Edition(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm2.ui', self)
        self.pushButton.clicked.connect(self.table)

        self.donwland_names()
        self.label_7.hide()

        self.comboBox.activated.connect(self.edit)

    def edit(self):
        if self.comboBox.currentText() != 'Выберите сорт Кофе':
            con = sqlite3.connect('coffee.db')
            cur = con.cursor()

            result = cur.execute(f"""select * from infa_cof
            where sort == '{self.comboBox.currentText()}'""").fetchall()

            con.close()

            row = result[0]
            self.spinBox.setValue(row[2])
            self.lineEdit_2.setText(row[3])
            self.lineEdit_3.setText(row[4])
            self.lineEdit_4.setText(str(row[5]))
            self.lineEdit_5.setText(str(row[6]))
        else:
            self.spinBox.setValue(0)
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()

    def donwland_names(self):
        self.comboBox.addItem('Выберите сорт Кофе')
        con = sqlite3.connect('coffee.db')
        cur = con.cursor()

        result = cur.execute(f"""select sort from infa_cof""").fetchall()

        genres = []
        for gen in result:
            genres.append(gen[0])
        con.close()

        self.comboBox.addItems(genres)

    def table(self):
        sort = self.comboBox.currentText()
        proj = self.spinBox.text()
        molot_v_zern = self.lineEdit_2.text()
        vkus = self.lineEdit_3.text()
        zena = self.lineEdit_4.text()
        upakovka = self.lineEdit_5.text()

        con = sqlite3.connect('coffee.db')
        cur = con.cursor()

        result = cur.execute(f"""update infa_cof
                set projarka = '{proj}', molotiyzerna = '{molot_v_zern}',
                vkus = '{vkus}', zena = '{zena}', obuem = '{upakovka}'
                where sort = '{sort}'""")

        con.commit()
        con.close()

        self.a = MyWidget()
        self.a.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())