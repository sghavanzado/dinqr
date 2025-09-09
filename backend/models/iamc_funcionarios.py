from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Numeric, ForeignKey, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from config import Config

# Base declarativa para modelos IAMC
Base = declarative_base()

# Engine específico para IAMC
iamc_engine = create_engine(
    Config.IAMC_SQLALCHEMY_DATABASE_URI,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Sessão específica para IAMC
IAMCSession = sessionmaker(bind=iamc_engine)

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
            'EstadoFuncionario': self.EstadoFuncionario
        }
    
    def __repr__(self):
        return f'<Funcionario {self.Nome} {self.Apelido}>'

class Departamento(db.Model):
    __tablename__ = 'Departamentos'
    
    DepartamentoID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(100), nullable=False)
    Descricao = db.Column(db.String(255), nullable=True)
    
    # Relacionamentos
    historico_cargos = db.relationship('HistoricoCargoFuncionario', backref='departamento', lazy=True)
    
    def to_dict(self):
        return {
            'DepartamentoID': self.DepartamentoID,
            'Nome': self.Nome,
            'Descricao': self.Descricao
        }
    
    def __repr__(self):
        return f'<Departamento {self.Nome}>'

class Cargo(db.Model):
    __tablename__ = 'Cargos'
    
    CargoID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(100), nullable=False)
    Descricao = db.Column(db.String(255), nullable=True)
    Nivel = db.Column(db.String(50), nullable=True)
    
    # Relacionamentos
    historico_cargos = db.relationship('HistoricoCargoFuncionario', backref='cargo', lazy=True)
    
    def to_dict(self):
        return {
            'CargoID': self.CargoID,
            'Nome': self.Nome,
            'Descricao': self.Descricao,
            'Nivel': self.Nivel
        }
    
    def __repr__(self):
        return f'<Cargo {self.Nome}>'

class HistoricoCargoFuncionario(db.Model):
    __tablename__ = 'HistoricoCargoFuncionario'
    
    HistoricoID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FuncionarioID = db.Column(db.Integer, db.ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    CargoID = db.Column(db.Integer, db.ForeignKey('Cargos.CargoID'), nullable=False)
    DepartamentoID = db.Column(db.Integer, db.ForeignKey('Departamentos.DepartamentoID'), nullable=False)
    DataInicio = db.Column(db.Date, nullable=False)
    DataFim = db.Column(db.Date, nullable=True)
    
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

class Contrato(db.Model):
    __tablename__ = 'Contratos'
    
    ContratoID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FuncionarioID = db.Column(db.Integer, db.ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    TipoContrato = db.Column(db.String(50), nullable=True)
    DataInicio = db.Column(db.Date, nullable=True)
    DataFim = db.Column(db.Date, nullable=True)
    Salario = db.Column(db.Numeric(18, 2), nullable=True)
    Moeda = db.Column(db.String(3), nullable=True)
    Estado = db.Column(db.String(20), nullable=True)  # Vigente, Terminado
    
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
