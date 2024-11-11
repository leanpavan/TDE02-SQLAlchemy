from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, Date, Table, Float
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import IntegrityError
import sys

db = create_engine('sqlite:///medico_paciente.db', echo=True)
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

# Tabela Usuario
class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    permissao = Column(Boolean, nullable=False)  # True para permissões administrativas, False caso contrário



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

# # Dados para tabela Medico
# medico1 = Medico(nome="Dr. João", especialidade="Cardiologia")
# medico2 = Medico(nome="Dra. Maria", especialidade="Dermatologia")
#
# # Dados para tabela Paciente
# paciente1 = Paciente(nome="Carlos Silva", idade=45)
# paciente2 = Paciente(nome="Ana Paula", idade=30)
#
# # Dados para tabela Medicamento
# medicamento1 = Medicamento(nome="Aspirina", descricao="Anti-inflamatório")
# medicamento2 = Medicamento(nome="Ibuprofeno", descricao="Analgésico e anti-inflamatório")
#
# # Dados para tabela Consulta
# consulta1 = Consulta(data="2023-10-01", medico=medico1, paciente=paciente1)
# consulta2 = Consulta(data="2023-10-02", medico=medico2, paciente=paciente2)
#
# # Dados para tabela ConsultaMedicamento
# consulta_medicamento1 = ConsultaMedicamento(consulta=consulta1, medicamento=medicamento1, dosagem="100mg")
# consulta_medicamento2 = ConsultaMedicamento(consulta=consulta2, medicamento=medicamento2, dosagem="200mg")
#
# # Dados para tabela Usuario
# usuario1 = Usuario(nome="admin", senha="admin123", permissao=True)
# usuario2 = Usuario(nome="user1", senha="user123", permissao=False)
#
# # Adicionando os dados à sessão
# try:
#     session.add_all([
#         medico1, medico2,
#         paciente1, paciente2,
#         medicamento1, medicamento2,
#         consulta1, consulta2,
#         consulta_medicamento1, consulta_medicamento2,
#         usuario1, usuario2
#     ])
#     session.commit()
#     print("Dados inseridos com sucesso!")
# except IntegrityError as e:
#     session.rollback()
#     print(f"Erro de integridade: {e}")

