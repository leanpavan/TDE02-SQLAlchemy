from main import *

def create_medico (nome, especialidade):
    medico = Medico(nome=nome, especialidade=especialidade)
    session.add(medico)
    session.commit()
    print(f"Médico {nome} cadastrado com sucesso!")

def create_paciente (nome, idade):
    paciente = Paciente(nome=nome, idade=idade)
    session.add(paciente)
    session.commit()
    print(f"Paciente {nome} cadastrado com sucesso!")

def create_consulta (data, nome_medico, nome_paciente):
    id_medico = session.query(Medico).filter_by(nome=nome_medico).first()
    id_paciente = session.query(Paciente).filter_by(nome=nome_paciente).first()
    consulta = Consulta(data=data, medico_id=id_medico.id, paciente_id=id_paciente.id)
    session.add(consulta)
    session.commit()
    print(f"Consulta de {nome_paciente} com {nome_medico} cadastrado com sucesso!")

while True:
    print(f"1 - CREATE")
    print(f"0 - EXIT")
    escolha = input("Digite sua escolha: ")
    if escolha == "1":
        print(f"1 - CREATE Medico")
        print(f"2 - CREATE Paciente")
        print(f"3 - CREATE Consulta")
        print(f"0 - Voltar")
        create_input = input("Digite sua escolha: ")
        match create_input:
            case "1":
                nome = input("Digite o nome do Médico: ")
                especialidade = input("Digite a especialidade do médico: ")
                create_medico(nome, especialidade)
            case "2":
                nome = input("Digite o nome do Paciente: ")
                idade = input("Digite a idade do Paciente: ")
                create_paciente(nome, idade)
            case "3":
                nome_paciente = input("Digite o nome do Paciente: ")
                nome_medico = input("Digite o nome do Medico: ")
                data_consulta = input("Digite o data da consulta: ")
                create_consulta(data_consulta, nome_medico, nome_paciente)
            case "0":
                continue
    elif (escolha == "0"):
        break


from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QComboBox, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QPushButton
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Setup the database connection and session
db = create_engine('sqlite:///medico_paciente.db', echo=True)
Session = sessionmaker(bind=db)
session = Session()
Base = declarative_base()
