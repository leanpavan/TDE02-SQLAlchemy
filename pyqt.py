import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QMessageBox, QMainWindow, QComboBox, QLabel
from sqlalchemy.orm import sessionmaker
from main import *

# Conecta ao Banco de Dados
db = create_engine('sqlite:///medico_paciente.db', echo=True)
Session = sessionmaker(bind=db)
session = Session()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gerenciamento de Banco de Dados')
        self.setGeometry(100, 100, 600, 400)

        self.menu_widget = QWidget(self)
        self.setCentralWidget(self.menu_widget)
        self.layout = QVBoxLayout(self.menu_widget)

        # Botões de CREATE, READ, UPDATE e DELETE
        self.create_button = QPushButton('Adicionar Médico / Paciente / Medicamento / Consulta')
        self.read_button = QPushButton('Consultar Banco de Dados')
        self.update_button = QPushButton('Atualizar Dados')
        self.delete_button = QPushButton('Deletar Dados')
        # Botão de fechar aplicação
        self.exit_button = QPushButton('Sair')

        self.layout.addWidget(self.create_button)
        self.layout.addWidget(self.read_button)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.exit_button)

        # Conectar os botões com as janelas do PyQT
        self.create_button.clicked.connect(self.open_create_window)
        self.read_button.clicked.connect(self.open_read_window)
        self.exit_button.clicked.connect(self.close)

    def open_create_window(self):
        self.create_window = CreateWindow()
        self.create_window.show()

    def open_read_window(self):
        self.read_window = ReadWindow()
        self.read_window.show()


class CreateWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Adicionar dados ao Banco de Dados')
        self.setGeometry(100, 100, 600, 400)
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        self.entity_combo = QComboBox()
        self.entity_combo.addItems(['Médico', 'Paciente', 'Medicamento', 'Consulta'])
        self.layout.addWidget(QLabel('Selecionar Entidade: '))
        self.layout.addWidget(self.entity_combo)

        # Input de dados
        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.specialization_input = QLineEdit()
        self.description_input = QLineEdit()
        self.name_medico_input = QLineEdit()
        self.name_paciente_input = QLineEdit()
        self.data_consulta_input = QLineEdit()

        self.name_label = QLabel('Nome: ')
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.age_label = QLabel('Idade: ')
        self.layout.addWidget(self.age_label)
        self.layout.addWidget(self.age_input)

        self.specialization_label = QLabel('Especialidade: ')
        self.layout.addWidget(self.specialization_label)
        self.layout.addWidget(self.specialization_input)

        self.description_label = QLabel('Descrição: ')
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_input)

        self.name_medico_label = QLabel('Nome do médico: ')
        self.layout.addWidget(self.name_medico_label)
        self.layout.addWidget(self.name_medico_input)

        self.name_paciente_label = QLabel('Nome do paciente: ')
        self.layout.addWidget(self.name_paciente_label)
        self.layout.addWidget(self.name_paciente_input)

        self.data_consulta_label = QLabel('Data da consulta: ')
        self.layout.addWidget(self.data_consulta_label)
        self.layout.addWidget(self.data_consulta_input)

        # Botão Adicionar
        self.add_button = QPushButton('Adicionar ao Banco de Dados')
        self.layout.addWidget(self.add_button)

        # Alterar labels e inputs de acordo com a entidade escolhida
        self.entity_combo.currentIndexChanged.connect(self.adjust_fields)

        # Define os campos padrões
        self.adjust_fields()
        self.add_button.clicked.connect(self.add_entity)


    def adjust_fields(self):
        entity = self.entity_combo.currentText()
        print(f"Selecionado: {entity}")  # Log para verificar entidade selecionada

        if entity == 'Médico':
            self.specialization_label.show()
            self.specialization_input.show()
            self.name_medico_label.show()
            self.name_medico_input.show()
            self.name_paciente_label.hide()
            self.name_paciente_input.hide()
            self.age_label.hide()
            self.age_input.hide()
            self.name_label.hide()
            self.name_input.hide()
            self.description_label.hide()
            self.description_input.hide()
            self.data_consulta_label.hide()
            self.data_consulta_input.hide()

        elif entity == 'Paciente':
            self.age_label.show()
            self.age_input.show()
            self.name_paciente_label.show()
            self.name_paciente_input.show()
            self.name_medico_label.hide()
            self.name_medico_input.hide()
            self.name_label.hide()
            self.name_input.hide()
            self.specialization_label.hide()
            self.specialization_input.hide()
            self.description_label.hide()
            self.description_input.hide()
            self.data_consulta_label.hide()
            self.data_consulta_input.hide()

        elif entity == 'Medicamento':
            self.name_label.show()
            self.name_input.show()
            self.description_input.show()
            self.description_label.show()
            self.name_paciente_label.hide()
            self.name_paciente_input.hide()
            self.name_medico_label.hide()
            self.name_medico_input.hide()
            self.age_label.hide()
            self.age_input.hide()
            self.specialization_label.hide()
            self.specialization_input.hide()
            self.data_consulta_label.hide()
            self.data_consulta_input.hide()

        elif entity == 'Consulta':
            self.name_medico_label.show()
            self.name_medico_input.show()
            self.name_paciente_label.show()
            self.name_paciente_input.show()
            self.data_consulta_label.show()
            self.data_consulta_input.show()
            self.age_label.hide()
            self.age_input.hide()
            self.specialization_label.hide()
            self.specialization_input.hide()
            self.description_label.hide()
            self.description_input.hide()
            self.name_label.hide()
            self.name_input.hide()


    def add_entity(self):
        entity = self.entity_combo.currentText()
        try:
            if entity == 'Médico':
                name = self.name_medico_input.text()
                specialization = self.specialization_input.text()
                if name and specialization:
                    medico = Medico(nome=name, especialidade=specialization)
                    session.add(medico)
                    session.commit()

            elif entity == 'Paciente':
                name = self.name_paciente_input.text()
                age = self.age_input.text()
                if name and age:
                    paciente = Paciente(nome=name, idade=age)
                    session.add(paciente)
                    session.commit()

            elif entity == 'Medicamento':
                name = self.name_input.text()
                description = self.description_input.text()
                if name and description:
                    medicamento = Medicamento(nome=name, descricao=description)
                    session.add(medicamento)
                    session.commit()

            elif entity == 'Consulta':
                name_medico = self.name_medico_input.text()
                name_paciente = self.name_paciente_input.text()
                data_consulta = self.data_consulta_input.text()
                id_medico = session.query(Medico).filter_by(nome=name_medico).first()
                id_paciente = session.query(Paciente).filter_by(nome=name_paciente).first()
                if name_medico and name_paciente and id_medico and id_paciente:
                    consulta = Consulta(data=data_consulta, medico_id=id_medico.id, paciente_id=id_paciente.id)
                    session.add(consulta)
                    session.commit()
        except Exception as e:
            print(f"Erro ao adicionar entidade {entity}: {e}")
            QMessageBox.critical(self, 'Erro', f"Ocorreu um erro ao adicionar a entidade {entity}: {e}")


class ReadWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Realizar leitura de dados do Banco de Dados')
        self.setGeometry(100, 100, 600, 400)
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        self.entity_combo = QComboBox()
        self.entity_combo.addItems(['Médico', 'Paciente', 'Medicamento', 'Consulta'])
        self.layout.addWidget(QLabel('Selecionar Entidade: '))
        self.layout.addWidget(self.entity_combo)

        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        self.entity_combo.currentIndexChanged.connect(self.display_data)

        try:
            self.display_data()
        except Exception as e:
            print(f"Erro ao exibir dados: {e}")
            QMessageBox.critical(self, 'Erro', f"Ocorreu um erro ao exibir dados: {e}")

    def display_data(self):
        entity = self.entity_combo.currentText()
        try:
            if entity == 'Médico':
                data = session.query(Medico).all()
                self.table.setRowCount(len(data))
                self.table.setColumnCount(3)
                self.table.setHorizontalHeaderLabels(['ID', 'Nome', 'Especialidade'])

                for row, medico in enumerate(data):
                    self.table.setItem(row, 0, QTableWidgetItem(str(medico.id)))
                    self.table.setItem(row, 1, QTableWidgetItem(medico.nome))
                    self.table.setItem(row, 2, QTableWidgetItem(str(medico.especialidade)))

            elif entity == 'Paciente':
                data = session.query(Paciente).all()
                self.table.setRowCount(len(data))
                self.table.setColumnCount(3)
                self.table.setHorizontalHeaderLabels(['ID', 'Nome', 'Idade'])

                for row, paciente in enumerate(data):
                    self.table.setItem(row, 0, QTableWidgetItem(str(paciente.id)))
                    self.table.setItem(row, 1, QTableWidgetItem(paciente.nome))
                    self.table.setItem(row, 2, QTableWidgetItem(str(paciente.idade)))

            elif entity == 'Medicamento':
                data = session.query(Medicamento).all()
                self.table.setRowCount(len(data))
                self.table.setColumnCount(3)
                self.table.setHorizontalHeaderLabels(['ID', 'Nome', 'Descrição'])

                for row, medicamento in enumerate(data):
                    self.table.setItem(row, 0, QTableWidgetItem(str(medicamento.id)))
                    self.table.setItem(row, 1, QTableWidgetItem(medicamento.nome))
                    self.table.setItem(row, 2, QTableWidgetItem(medicamento.descricao))

            elif entity == 'Consulta':
                data = session.query(Consulta).all()
                self.table.setRowCount(len(data))
                self.table.setColumnCount(4)
                self.table.setHorizontalHeaderLabels(['ID', 'Data', 'ID do Médico', 'ID do Paciente'])

                for row, consulta in enumerate(data):
                    self.table.setItem(row, 0, QTableWidgetItem(str(consulta.id)))
                    self.table.setItem(row, 1, QTableWidgetItem(consulta.data))
                    self.table.setItem(row, 2, QTableWidgetItem(str(consulta.medico_id)))
                    self.table.setItem(row, 3, QTableWidgetItem(str(consulta.paciente_id)))

        except Exception as e:
            print(f"Erro ao consultar a entidade {entity}: {e}")
            QMessageBox.critical(self, 'Erro', f"Ocorreu um erro ao consultar a entidade {entity}: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())