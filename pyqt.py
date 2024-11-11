import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QMessageBox, QMainWindow, QComboBox, QLabel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import text
from main import *

# Conecta ao Banco de Dados
db = create_engine('sqlite:///medico_paciente.db', echo=True)
Session = sessionmaker(bind=db)
session = Session()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 300, 150)
        self.setStyleSheet('background-color: #1C1D21; color: #FFFFFF')

        # Layout do login
        layout = QFormLayout()
        self.setLayout(layout)

        # Campos de usuário e senha
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Usuário')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Senha')
        self.password_input.setEchoMode(QLineEdit.Password)

        # Botão de login
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)

        # Adiciona os widgets ao layout
        layout.addRow(QLabel('Usuário:'), self.username_input)
        layout.addRow(QLabel('Senha:'), self.password_input)
        layout.addWidget(self.login_button)

    def login(self):
        # Recebe o usuário e senha
        username = self.username_input.text()
        password = self.password_input.text()

        # Consulta para verificar o login
        user = session.query(Usuario).filter_by(nome=username, senha=password).first()

        if user:
            self.user_permission = user.permissao  # Salva a permissão do usuário
            QMessageBox.information(self, 'Sucesso', 'Login realizado com sucesso!')
            self.close()
            # Abre a janela principal
            self.main_window = MainWindow(self.user_permission)
            self.main_window.show()
        else:
            QMessageBox.critical(self, 'Erro', 'Usuário ou senha inválidos.')

class MainWindow(QMainWindow):
    def __init__(self, user_permission):
        super().__init__()
        self.setWindowTitle('Gerenciamento de Banco de Dados')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet('background-color: #1C1D21')

        # Salvar permissão do usuário
        self.user_permission = user_permission

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

        if self.user_permission == 0:
            self.update_button.setDisabled(True)
            self.delete_button.setDisabled(True)

        # Colorir os botões
        self.create_button.setStyleSheet("background-color: #A288A6")
        self.read_button.setStyleSheet("background-color: #A288A6")
        self.update_button.setStyleSheet("background-color: #A288A6")
        self.delete_button.setStyleSheet("background-color: #A288A6")
        self.exit_button.setStyleSheet("background-color: #F1E3E4")

        self.layout.addWidget(self.create_button)
        self.layout.addWidget(self.read_button)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.exit_button)

        # Conectar os botões com as janelas do PyQT
        self.create_button.clicked.connect(self.open_create_window)
        self.read_button.clicked.connect(self.open_read_window)
        self.update_button.clicked.connect(self.open_update_window)
        self.delete_button.clicked.connect(self.open_delete_window)
        self.exit_button.clicked.connect(self.close)

    def open_create_window(self):
        self.create_window = CreateWindow()
        self.create_window.show()

    def open_read_window(self):
        self.read_window = ReadWindow()
        self.read_window.show()

    def open_update_window(self):
        self.update_window = UpdateWindow(self.user_permission)
        self.update_window.show()

    def open_delete_window(self):
        self.delete_window = DeleteWindow(self.user_permission)
        self.delete_window.show()


class CreateWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Adicionar dados ao Banco de Dados')
        self.setGeometry(100, 100, 600, 400)
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)
        self.setStyleSheet('background-color: #F1E3E4')

        # Seleção de Entidade
        self.entity_combo = QComboBox()
        self.entity_combo.addItems(['Médico', 'Paciente', 'Medicamento', 'Consulta'])
        self.layout.addWidget(QLabel('Selecionar Entidade: '))
        self.layout.addWidget(self.entity_combo)

        # Campos de entrada
        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.specialization_input = QLineEdit()
        self.description_input = QLineEdit()
        self.name_medico_input = QLineEdit()
        self.name_paciente_input = QLineEdit()
        self.data_consulta_input = QLineEdit()

        # Labels
        self.name_label = QLabel('Nome:')
        self.age_label = QLabel('Idade:')
        self.specialization_label = QLabel('Especialidade:')
        self.description_label = QLabel('Descrição:')
        self.name_medico_label = QLabel('Nome do Médico:')
        self.name_paciente_label = QLabel('Nome do Paciente:')
        self.data_consulta_label = QLabel('Data da Consulta:')

        # Adicionando os campos de entrada ao layout
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.age_label)
        self.layout.addWidget(self.age_input)
        self.layout.addWidget(self.specialization_label)
        self.layout.addWidget(self.specialization_input)
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_input)
        self.layout.addWidget(self.name_medico_label)
        self.layout.addWidget(self.name_medico_input)
        self.layout.addWidget(self.name_paciente_label)
        self.layout.addWidget(self.name_paciente_input)
        self.layout.addWidget(self.data_consulta_label)
        self.layout.addWidget(self.data_consulta_input)

        # Botão para adicionar ao banco de dados
        self.add_button = QPushButton('Adicionar ao Banco de Dados')
        self.layout.addWidget(self.add_button)

        # Ajusta os campos conforme a entidade selecionada
        self.entity_combo.currentIndexChanged.connect(self.adjust_fields)

        self.adjust_fields()
        self.add_button.clicked.connect(self.add_entity)

    def adjust_fields(self):
        entity = self.entity_combo.currentText()

        # Esconde todos os campos
        self.name_label.show()
        self.name_input.show()
        self.age_label.hide()
        self.age_input.hide()
        self.specialization_label.hide()
        self.specialization_input.hide()
        self.description_label.hide()
        self.description_input.hide()
        self.name_medico_label.hide()
        self.name_medico_input.hide()
        self.name_paciente_label.hide()
        self.name_paciente_input.hide()
        self.data_consulta_label.hide()
        self.data_consulta_input.hide()

        if entity == 'Médico':
            self.specialization_label.show()
            self.specialization_input.show()
        elif entity == 'Paciente':
            self.age_label.show()
            self.age_input.show()
        elif entity == 'Medicamento':
            self.description_label.show()
            self.description_input.show()
        elif entity == 'Consulta':
            self.name_medico_label.show()
            self.name_medico_input.show()
            self.name_paciente_label.show()
            self.name_paciente_input.show()
            self.data_consulta_label.show()
            self.data_consulta_input.show()

    def add_entity(self):
        entity = self.entity_combo.currentText()

        try:

            session.begin() # Inicia transação

            if entity == 'Médico':
                name = self.name_input.text()
                specialization = self.specialization_input.text()
                if name and specialization:
                    medico = Medico(nome=name, especialidade=specialization)
                    session.add(medico)
                    session.commit()
                    QMessageBox.information(self, 'Sucesso', 'Médico adicionado com sucesso!')
                else:
                    QMessageBox.warning(self, 'Erro', 'Preencha todos os campos.')
            elif entity == 'Paciente':
                name = self.name_input.text()
                age = self.age_input.text()
                if name and age:
                    paciente = Paciente(nome=name, idade=age)
                    session.add(paciente)
                    session.commit()
                    QMessageBox.information(self, 'Sucesso', 'Paciente adicionado com sucesso!')
                else:
                    QMessageBox.warning(self, 'Erro', 'Preencha todos os campos.')
            elif entity == 'Medicamento':
                description = self.description_input.text()
                if description:
                    medicamento = Medicamento(descricao=description)
                    session.add(medicamento)
                    session.commit()
                    QMessageBox.information(self, 'Sucesso', 'Medicamento adicionado com sucesso!')
                else:
                    QMessageBox.warning(self, 'Erro', 'Preencha todos os campos.')
            elif entity == 'Consulta':
                name_medico = self.name_medico_input.text()
                name_paciente = self.name_paciente_input.text()
                data_consulta = self.data_consulta_input.text()
                if name_medico and name_paciente and data_consulta:
                    consulta = Consulta(nome_medico=name_medico, nome_paciente=name_paciente, data_consulta=data_consulta)
                    session.add(consulta)
                    session.commit()
                    QMessageBox.information(self, 'Sucesso', 'Consulta adicionada com sucesso!')
                else:
                    QMessageBox.warning(self, 'Erro', 'Preencha todos os campos.')
        except SQLAlchemyError as e:
            session.rollback() # Reverte transação caso um erro ocorra
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao adicionar o registro: {str(e)}')
        finally:
            session.close() # Fecha a sessão


class ReadWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Realizar leitura de dados do Banco de Dados')
        self.setGeometry(100, 100, 600, 400)
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)
        self.setStyleSheet('background-color: #F1E3E4')

        self.entity_combo = QComboBox()
        self.entity_combo.addItems(['Médico', 'Paciente', 'Medicamento', 'Consulta'])
        self.layout.addWidget(QLabel('Selecionar Entidade: '))
        self.layout.addWidget(self.entity_combo)

        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        # Campo de entrada para consulta avançada
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText('Digite a consulta SQL...')
        self.layout.addWidget(self.query_input)

        # Botão para executar consulta avançada
        self.query_button = QPushButton('Executar Consulta')
        self.layout.addWidget(self.query_button)

        self.entity_combo.currentIndexChanged.connect(self.display_data)
        self.query_button.clicked.connect(self.advanced_query)

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

    def advanced_query(self):
        query_text = self.query_input.text()
        try:
            # Executa a consulta SQL
            result = session.execute(text(query_text))

            # Obtém os nomes das colunas a partir do objeto result
            headers = [column[0] for column in result.cursor.description] if result.cursor.description else []

            # Limpa a tabela
            results = result.fetchall()
            self.table.setRowCount(len(results))
            self.table.setColumnCount(len(headers))

            # Exibe os resultados na tabela
            if results:
                self.table.setHorizontalHeaderLabels(headers)

                # Preenche os dados na tabela
                for row_idx, row in enumerate(results):
                    for col_idx, value in enumerate(row):
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
            else:
                QMessageBox.information(self, 'Sem resultados', 'Nenhum dado encontrado para a consulta.')

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao executar a consulta: {e}')



class UpdateWindow(QMainWindow):
    def __init__(self, user_permission):
        super().__init__()
        self.setWindowTitle("Atualizar Banco de Dados")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet('background-color: #F1E3E4')

        # Salvar permissão do usuário
        self.user_permission = user_permission

        # Layout principal
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        # Seleção de entidade e ID
        self.entity_combo = QComboBox()
        self.entity_combo.addItems(['Médico', 'Paciente', 'Medicamento', 'Consulta'])
        self.layout.addWidget(QLabel('Selecionar Entidade: '))
        self.layout.addWidget(self.entity_combo)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID do registro para atualizar")
        self.layout.addWidget(self.id_input)

        # Campos de entrada
        self.name_input = QLineEdit()
        self.specialization_input = QLineEdit()
        self.age_input = QLineEdit()
        self.description_input = QLineEdit()
        self.data_input = QLineEdit()

        # Labels e campos de entrada
        self.name_label = QLabel('Nome:')
        self.specialization_label = QLabel('Especialidade:')
        self.age_label = QLabel('Idade:')
        self.description_label = QLabel('Descrição:')
        self.data_label = QLabel('Data da Consulta:')

        # Adiciona os campos ao layout
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.specialization_label)
        self.layout.addWidget(self.specialization_input)
        self.layout.addWidget(self.age_label)
        self.layout.addWidget(self.age_input)
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_input)
        self.layout.addWidget(self.data_label)
        self.layout.addWidget(self.data_input)

        # Botão de atualização
        self.update_button = QPushButton('Atualizar')
        self.layout.addWidget(self.update_button)

        # Conectar o evento de seleção de entidade para ajustar os campos
        self.entity_combo.currentIndexChanged.connect(self.adjust_fields)

        # Conectar evento de clique do botão
        self.update_button.clicked.connect(self.update_entity)

        # Ajusta os campos inicialmente
        self.adjust_fields()

    def adjust_fields(self):
        entity = self.entity_combo.currentText()

        # Esconde todos os campos primeiro
        self.name_label.hide()
        self.name_input.hide()
        self.specialization_label.hide()
        self.specialization_input.hide()
        self.age_label.hide()
        self.age_input.hide()
        self.description_label.hide()
        self.description_input.hide()
        self.data_label.hide()
        self.data_input.hide()

        # Exibe os campos conforme a entidade selecionada
        if entity == 'Médico':
            self.name_label.show()
            self.name_input.show()
            self.specialization_label.show()
            self.specialization_input.show()

        elif entity == 'Paciente':
            self.name_label.show()
            self.name_input.show()
            self.age_label.show()
            self.age_input.show()

        elif entity == 'Medicamento':
            self.name_label.show()
            self.name_input.show()
            self.description_label.show()
            self.description_input.show()

        elif entity == 'Consulta':
            self.data_label.show()
            self.data_input.show()

    def update_entity(self):
        if self.user_permission == 0:
            QMessageBox.warning(self, 'Permissão negada', 'Você não tem permissão para atualizar dados.')
            return

        entity = self.entity_combo.currentText()
        entity_id = self.id_input.text()

        try:
            session.begin()

            if entity == 'Médico':
                medico = session.query(Medico).get(entity_id)
                if medico:
                    medico.nome = self.name_input.text()
                    medico.especialidade = self.specialization_input.text()
                    session.commit()

            elif entity == 'Paciente':
                paciente = session.query(Paciente).get(entity_id)
                if paciente:
                    paciente.nome = self.name_input.text()
                    paciente.idade = self.age_input.text()
                    session.commit()

            elif entity == 'Medicamento':
                medicamento = session.query(Medicamento).get(entity_id)
                if medicamento:
                    medicamento.nome = self.name_input.text()
                    medicamento.descricao = self.description_input.text()
                    session.commit()

            elif entity == 'Consulta':
                consulta = session.query(Consulta).get(entity_id)
                if consulta:
                    consulta.data = self.data_input.text()
                    session.commit()

            QMessageBox.information(self, 'Sucesso', f'{entity} atualizado com sucesso!')
        except SQLAlchemyError as e:
            session.rollback()
            QMessageBox.critical(self, 'Erro', f'Erro ao atualizar {entity}: {e}')
        finally:
            session.close()


class DeleteWindow(QMainWindow):
    def __init__(self, user_permission):
        super().__init__()
        self.setWindowTitle("Deletar dados do Banco de Dados")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet('background-color: #F1E3E4')

        # Salvar permissão do usuário
        self.user_permission = user_permission

        # Layout principal
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        # Seleção de entidade e ID
        self.entity_combo = QComboBox()
        self.entity_combo.addItems(['Médico', 'Paciente', 'Medicamento', 'Consulta'])
        self.layout.addWidget(QLabel('Selecionar Entidade: '))
        self.layout.addWidget(self.entity_combo)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID do registro para deletar")
        self.layout.addWidget(self.id_input)

        # Botão de exclusão
        self.delete_button = QPushButton('Deletar')
        self.layout.addWidget(self.delete_button)

        # Conectar evento de clique do botão
        self.delete_button.clicked.connect(self.delete_entity)

    def delete_entity(self):
        if self.user_permission == 0:
            QMessageBox.warning(self, 'Permissão negada', 'Você não tem permissão para deletar dados.')
            return

        entity = self.entity_combo.currentText()
        entity_id = self.id_input.text()

        try:
            session.begin()

            if entity == 'Médico':
                medico = session.query(Medico).get(entity_id)
                if medico:
                    session.delete(medico)
                    session.commit()

            elif entity == 'Paciente':
                paciente = session.query(Paciente).get(entity_id)
                if paciente:
                    session.delete(paciente)
                    session.commit()

            elif entity == 'Medicamento':
                medicamento = session.query(Medicamento).get(entity_id)
                if medicamento:
                    session.delete(medicamento)
                    session.commit()

            elif entity == 'Consulta':
                consulta = session.query(Consulta).get(entity_id)
                if consulta:
                    session.delete(consulta)
                    session.commit()

            QMessageBox.information(self, 'Sucesso', f'{entity} deletado com sucesso!')
        except SQLAlchemyError as e:
            session.rollback()
            QMessageBox.critical(self, 'Erro', f'Erro ao deletar {entity}: {e}')
        finally:
            session.close()


# SELECT nome, especialidade FROM Medico;

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())