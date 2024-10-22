from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, Date, Table, Float
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import sys

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

