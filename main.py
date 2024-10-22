from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, Date, Table, Float
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget, QFormLayout, QLineEdit, QTableWidget, QMessageBox, QTableWidgetItem,
)

from layout_colorwidget import Color

db = create_engine('sqlite:///medico_paciente.db', echo=True)
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

# Tabela Medico
class Medico(Base):
    __tablename__ = 'medico'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String, nullable=False)

    consultas = relationship('Consulta', back_populates='medico')


# Tabela paciente
class Paciente(Base):
    __tablename__ = 'paciente'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)

    consultas = relationship('Consulta', back_populates='paciente')


# Tabela medicamento
class Medicamento(Base):
    __tablename__ = 'medicamento'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    descricao = Column(String(100))

    consultas = relationship('ConsultaMedicamento', back_populates='medicamento')


# Tabela consulta
class Consulta(Base):
    __tablename__ = 'consulta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String, nullable=False)
    medico_id = Column(Integer, ForeignKey('medico.id'), nullable=False)
    paciente_id = Column(Integer, ForeignKey('paciente.id'), nullable=False)

    medico = relationship('Medico', back_populates='consultas')
    paciente = relationship('Paciente', back_populates='consultas')
    medicamentos = relationship('ConsultaMedicamento', back_populates='consulta')


# Tabela de associação entre Consulta e Medicamento
class ConsultaMedicamento(Base):
    __tablename__ = 'consulta_medicamento'

    consulta_id = Column(Integer, ForeignKey('consulta.id'), primary_key=True, autoincrement=True, unique=True)
    medicamento_id = Column(Integer, ForeignKey('medicamento.id'))
    dosagem = Column(String, nullable=False)

    consulta = relationship('Consulta', back_populates='medicamentos')
    medicamento = relationship('Medicamento', back_populates='consultas')


Base.metadata.create_all(bind=db)


# Interface PyQt5
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CRUD Medico-Paciente')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Botões para leitura do banco de dados
        self.load_medico_button = QPushButton('Carregar Médicos')
        self.load_medico_button.clicked.connect(self.load_medicos)
        self.layout.addWidget(self.load_medico_button)

        self.load_paciente_button = QPushButton('Carregar Pacientes')
        self.load_paciente_button.clicked.connect(self.load_pacientes)
        self.layout.addWidget(self.load_paciente_button)

        self.load_medicamento_button = QPushButton('Carregar Medicamentos')
        self.load_medicamento_button.clicked.connect(self.load_medicamentos)
        self.layout.addWidget(self.load_medicamento_button)

        self.load_consulta_button = QPushButton('Carregar Consultas')
        self.load_consulta_button.clicked.connect(self.load_consultas)
        self.layout.addWidget(self.load_consulta_button)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        # Botões CREATE
        self.crud_section = QFormLayout()
        self.nome_input = QLineEdit()
        self.especialidade_input = QLineEdit()
        self.crud_section.addRow('Nome:', self.nome_input)
        self.crud_section.addRow('Especialidade:', self.especialidade_input)

        self.add_button = QPushButton('Adicionar Médico')
        self.add_button.clicked.connect(self.add_medico)
        self.update_button = QPushButton('Atualizar Médico')
        self.update_button.clicked.connect(self.update_medico)
        self.delete_button = QPushButton('Excluir Médico')
        self.delete_button.clicked.connect(self.delete_medico)

        self.crud_section.addWidget(self.add_button)
        self.crud_section.addWidget(self.update_button)
        self.crud_section.addWidget(self.delete_button)

        self.layout.addLayout(self.crud_section)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    # Funçoes de READ

    def load_medicos(self):
        records = session.query(Medico).all()
        self.table.setRowCount(len(records))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Nome', 'Especialidade'])

        for row, record in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(str(record.id)))
            self.table.setItem(row, 1, QTableWidgetItem(record.nome))
            self.table.setItem(row, 2, QTableWidgetItem(record.especialidade))

        QMessageBox.information(self, 'Informação', 'Médicos carregados com sucesso!')

    def load_pacientes(self):
        records = session.query(Paciente).all()
        self.table.setRowCount(len(records))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Nome', 'Idade'])

        for row, record in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(str(record.id)))
            self.table.setItem(row, 1, QTableWidgetItem(record.nome))
            self.table.setItem(row, 2, QTableWidgetItem(str(record.idade)))

        QMessageBox.information(self, 'Informação', 'Pacientes carregados com sucesso!')

    def load_medicamentos(self):
        records = session.query(Medicamento).all()
        self.table.setRowCount(len(records))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Nome', 'Descrição'])

        for row, record in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(str(record.id)))
            self.table.setItem(row, 1, QTableWidgetItem(record.nome))
            self.table.setItem(row, 2, QTableWidgetItem(record.descricao))

        QMessageBox.information(self, 'Informação', 'Medicamentos carregados com sucesso!')

    def load_consultas(self):
        records = session.query(Consulta).all()
        self.table.setRowCount(len(records))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Data', 'Médico', 'Paciente'])

        for row, record in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(str(record.id)))
            self.table.setItem(row, 1, QTableWidgetItem(record.data))
            self.table.setItem(row, 2, QTableWidgetItem(str(record.medico_id)))
            self.table.setItem(row, 3, QTableWidgetItem(str(record.paciente_id)))

        QMessageBox.information(self, 'Informação', 'Consultas carregadas com sucesso!')

    # Funções de CREATE



    def add_medico(self):
        nome = self.nome_input.text()
        especialidade = self.especialidade_input.text()

        if nome and especialidade:
            novo_medico = Medico(nome=nome, especialidade=especialidade)
            session.add(novo_medico)
            session.commit()
            QMessageBox.information(self, 'Informação', 'Médico adicionado com sucesso!')
            self.load_medicos()
        else:
            QMessageBox.warning(self, 'Atenção', 'Por favor, preencha todos os campos.')

    def update_medico(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            medico_id = int(selected_items[0].text())
            medico = session.query(Medico).filter_by(id=medico_id).first()

            nome = self.nome_input.text()
            especialidade = self.especialidade_input.text()

            if nome and especialidade:
                medico.nome = nome
                medico.especialidade = especialidade
                session.commit()
                QMessageBox.information(self, 'Informação', 'Médico atualizado com sucesso!')
                self.load_medicos()
            else:
                QMessageBox.warning(self, 'Atenção', 'Por favor, preencha todos os campos.')
        else:
            QMessageBox.warning(self, 'Atenção', 'Por favor, selecione um médico na tabela.')

    def delete_medico(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            medico_id = int(selected_items[0].text())
            medico = session.query(Medico).filter_by(id=medico_id).first()
            session.delete(medico)
            session.commit()
            QMessageBox.information(self, 'Informação', 'Médico excluído com sucesso!')
            self.load_medicos()
        else:
            QMessageBox.warning(self, 'Atenção', 'Por favor, selecione um médico na tabela.')


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
