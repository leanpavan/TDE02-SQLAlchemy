from main import *

# Criação de Usuários
usuarios = [
    Usuario(nome="admin", senha="admin123", permissao=1),
    Usuario(nome="user", senha="user123", permissao=0)
]
session.add_all(usuarios)

# Populando a tabela Medico com mais médicos
medicos = [
    Medico(nome="Dr. João Silva", especialidade="Cardiologia"),
    Medico(nome="Dra. Maria Oliveira", especialidade="Pediatria"),
    Medico(nome="Dr. Carlos Eduardo", especialidade="Ortopedia"),
    Medico(nome="Dra. Juliana Andrade", especialidade="Neurologia"),
    Medico(nome="Dr. Rafael Souza", especialidade="Gastroenterologia")
]
session.add_all(medicos)

# Populando a tabela Paciente com mais pacientes
pacientes = [
    Paciente(nome="Carlos Souza", idade=45),
    Paciente(nome="Ana Pereira", idade=12),
    Paciente(nome="Mariana Silva", idade=30),
    Paciente(nome="Joaquim Santos", idade=60),
    Paciente(nome="Fernanda Costa", idade=25)
]
session.add_all(pacientes)

# Populando a tabela Medicamento com mais medicamentos
medicamentos = [
    Medicamento(nome="Aspirina", descricao="Anti-inflamatório e analgésico"),
    Medicamento(nome="Amoxicilina", descricao="Antibiótico"),
    Medicamento(nome="Paracetamol", descricao="Analgésico e antitérmico"),
    Medicamento(nome="Ibuprofeno", descricao="Anti-inflamatório"),
    Medicamento(nome="Omeprazol", descricao="Protetor gástrico")
]
session.add_all(medicamentos)

# Populando a tabela Consulta com mais consultas
consultas = [
    Consulta(data="2023-10-10", medico=medicos[0], paciente=pacientes[0]),
    Consulta(data="2023-11-05", medico=medicos[1], paciente=pacientes[1]),
    Consulta(data="2023-12-15", medico=medicos[2], paciente=pacientes[2]),
    Consulta(data="2024-01-08", medico=medicos[3], paciente=pacientes[3]),
    Consulta(data="2024-02-20", medico=medicos[4], paciente=pacientes[4]),
    Consulta(data="2024-03-10", medico=medicos[0], paciente=pacientes[3]),
    Consulta(data="2024-04-18", medico=medicos[2], paciente=pacientes[1])
]
session.add_all(consultas)

# Populando a tabela de associação ConsultaMedicamento com mais associações
consulta_medicamentos = [
    ConsultaMedicamento(consulta=consultas[0], medicamento=medicamentos[0], dosagem="500mg"),
    ConsultaMedicamento(consulta=consultas[1], medicamento=medicamentos[1], dosagem="250mg"),
    ConsultaMedicamento(consulta=consultas[2], medicamento=medicamentos[2], dosagem="650mg"),
    ConsultaMedicamento(consulta=consultas[3], medicamento=medicamentos[3], dosagem="400mg"),
    ConsultaMedicamento(consulta=consultas[4], medicamento=medicamentos[4], dosagem="20mg"),
    ConsultaMedicamento(consulta=consultas[5], medicamento=medicamentos[2], dosagem="500mg"),
    ConsultaMedicamento(consulta=consultas[6], medicamento=medicamentos[1], dosagem="750mg")
]
session.add_all(consulta_medicamentos)

# Confirmando as transações
session.commit()

print("Dados inseridos com sucesso!")