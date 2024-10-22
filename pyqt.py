import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from sqlalchemy.orm import sessionmaker
import main

class CrudApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.session = session

    def initUI(self):
        self.setWindowTitle('CRUD Application')
        layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.city_input = QLineEdit()
        self.form_layout.addRow('Nome:', self.name_input)
        self.form_layout.addRow('Idade:', self.age_input)
        self.form_layout.addRow('Cidade:', self.city_input)

        self.add_button = QPushButton('Adicionar')
        self.update_button = QPushButton('Atualizar')
        self.delete_button = QPushButton('Deletar')
        self.load_button = QPushButton('Carregar Dados')

        self.add_button.clicked.connect(self.add_data)
        self.update_button.clicked.connect(self.update_data)
        self.delete_button.clicked.connect(self.delete_data)
        self.load_button.clicked.connect(self.load_data)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Nome', 'Idade', 'Cidade'])
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)

        layout.addLayout(self.form_layout)
        layout.addWidget(self.add_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def add_data(self):
        nome = self.name_input.text()
        idade = self.age_input.text()
        cidade = self.city_input.text()
        novo_paciente = Paciente(nome=nome, idade=idade, cidade=cidade)
        self.session.add(novo_paciente)
        self.session.commit()
        self.load_data()
        QMessageBox.information(self, 'Success', 'Dados adicionados com sucesso!')

    def update_data(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, 'Warning', 'Nenhuma linha selecionada')
            return

        id = self.table.item(selected_row, 0).text()
        nome = self.name_input.text()
        idade = self.age_input.text()
        cidade = self.city_input.text()
        paciente = self.session.query(Paciente).filter_by(id=id).first()
        paciente.nome = nome
        paciente.idade = idade
        paciente.cidade = cidade
        self.session.commit()
        self.load_data()
        QMessageBox.information(self, 'Success', 'Dados atualizados com sucesso!')

    def delete_data(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, 'Warning', 'Nenhuma linha selecionada')
            return

        id = self.table.item(selected_row, 0).text()
        paciente = self.session.query(Paciente).filter_by(id=id).first()
        self.session.delete(paciente)
        self.session.commit()
        self.load_data()
        QMessageBox.information(self, 'Success', 'Dados deletados com sucesso!')

    def load_data(self):
        self.table.setRowCount(0)
        pacientes = self.session.query(Paciente).all()
        for paciente in pacientes:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(paciente.id)))
            self.table.setItem(row_position, 1, QTableWidgetItem(paciente.nome))
            self.table.setItem