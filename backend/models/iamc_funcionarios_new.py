from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Numeric, ForeignKey, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

# Base declarativa para modelos IAMC
Base = declarative_base()

class Funcionario(Base):
    __tablename__ = 'Funcionarios'
    
    FuncionarioID = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(100), nullable=False)
    Apelido = Column(String(100), nullable=False)
    BI = Column(String(20), unique=True, nullable=False)
    DataNascimento = Column(Date, nullable=True)
    Sexo = Column(String(1), nullable=True)  # M/F/O
    EstadoCivil = Column(String(20), nullable=True)
    Email = Column(String(150), nullable=True)
    Telefone = Column(String(50), nullable=True)
    Endereco = Column(String(255), nullable=True)
    DataAdmissao = Column(Date, nullable=False)
    EstadoFuncionario = Column(String(20), nullable=True)  # Activo, Inactivo, Suspenso
    Foto = Column(String(255), nullable=True)  # Caminho para a foto tipo visa
    # Campos para cargo e departamento atuais
    CargoID = Column(Integer, ForeignKey('Cargos.CargoID'), nullable=True)
    DepartamentoID = Column(Integer, ForeignKey('Departamentos.DepartamentoID'), nullable=True)
    
    def to_dict(self):
        return {
            'FuncionarioID': self.FuncionarioID,
            'Nome': self.Nome,
            'Apelido': self.Apelido,
            'BI': self.BI,
            'DataNascimento': self.DataNascimento.isoformat() if self.DataNascimento else None,
            'Sexo': self.Sexo,
            'EstadoCivil': self.EstadoCivil,
            'Email': self.Email,
            'Telefone': self.Telefone,
            'Endereco': self.Endereco,
            'DataAdmissao': self.DataAdmissao.isoformat() if self.DataAdmissao else None,
            'EstadoFuncionario': self.EstadoFuncionario,
            'Foto': self.Foto,
            'CargoID': self.CargoID,
            'DepartamentoID': self.DepartamentoID
        }
    
    def __repr__(self):
        return f'<Funcionario {self.Nome} {self.Apelido}>'

class Departamento(Base):
    __tablename__ = 'Departamentos'
    
    DepartamentoID = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(100), nullable=False)
    Descricao = Column(String(255), nullable=True)
    
    def to_dict(self):
        return {
            'DepartamentoID': self.DepartamentoID,
            'Nome': self.Nome,
            'Descricao': self.Descricao
        }
    
    def __repr__(self):
        return f'<Departamento {self.Nome}>'

class Cargo(Base):
    __tablename__ = 'Cargos'
    
    CargoID = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(100), nullable=False)
    Descricao = Column(String(255), nullable=True)
    Nivel = Column(String(50), nullable=True)
    DepartamentoID = Column(Integer, ForeignKey('Departamentos.DepartamentoID'), nullable=True)
    
    def to_dict(self):
        return {
            'CargoID': self.CargoID,
            'Nome': self.Nome,
            'Descricao': self.Descricao,
            'Nivel': self.Nivel,
            'DepartamentoID': self.DepartamentoID
        }
    
    def __repr__(self):
        return f'<Cargo {self.Nome}>'

class HistoricoCargoFuncionario(Base):
    __tablename__ = 'HistoricoCargoFuncionario'
    
    HistoricoID = Column(Integer, primary_key=True, autoincrement=True)
    FuncionarioID = Column(Integer, ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    CargoID = Column(Integer, ForeignKey('Cargos.CargoID'), nullable=False)
    DepartamentoID = Column(Integer, ForeignKey('Departamentos.DepartamentoID'), nullable=False)
    DataInicio = Column(Date, nullable=False)
    DataFim = Column(Date, nullable=True)
    
    def to_dict(self):
        return {
            'HistoricoID': self.HistoricoID,
            'FuncionarioID': self.FuncionarioID,
            'CargoID': self.CargoID,
            'DepartamentoID': self.DepartamentoID,
            'DataInicio': self.DataInicio.isoformat() if self.DataInicio else None,
            'DataFim': self.DataFim.isoformat() if self.DataFim else None
        }
    
    def __repr__(self):
        return f'<HistoricoCargoFuncionario {self.HistoricoID}>'

class Contrato(Base):
    __tablename__ = 'Contratos'
    
    ContratoID = Column(Integer, primary_key=True, autoincrement=True)
    FuncionarioID = Column(Integer, ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    TipoContrato = Column(String(50), nullable=True)
    DataInicio = Column(Date, nullable=True)
    DataFim = Column(Date, nullable=True)
    Salario = Column(Numeric(18, 2), nullable=True)
    Moeda = Column(String(3), nullable=True)
    Estado = Column(String(20), nullable=True)  # Vigente, Terminado
    
    def to_dict(self):
        return {
            'ContratoID': self.ContratoID,
            'FuncionarioID': self.FuncionarioID,
            'TipoContrato': self.TipoContrato,
            'DataInicio': self.DataInicio.isoformat() if self.DataInicio else None,
            'DataFim': self.DataFim.isoformat() if self.DataFim else None,
            'Salario': float(self.Salario) if self.Salario else None,
            'Moeda': self.Moeda,
            'Estado': self.Estado
        }
    
    def __repr__(self):
        return f'<Contrato {self.ContratoID} - {self.TipoContrato}>'
