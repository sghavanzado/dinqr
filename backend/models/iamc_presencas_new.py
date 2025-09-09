from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Numeric, ForeignKey, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date

# Usar a mesma base declarativa
from .iamc_funcionarios_new import Base

class Presenca(Base):
    __tablename__ = 'Presencas'
    
    PresencaID = Column(Integer, primary_key=True, autoincrement=True)
    FuncionarioID = Column(Integer, ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    Data = Column(Date, nullable=False)
    HoraEntrada = Column(Time, nullable=True)
    HoraSaida = Column(Time, nullable=True)
    Observacao = Column(String(255), nullable=True)
    
    def to_dict(self):
        return {
            'PresencaID': self.PresencaID,
            'FuncionarioID': self.FuncionarioID,
            'Data': self.Data.isoformat() if self.Data else None,
            'HoraEntrada': self.HoraEntrada.isoformat() if self.HoraEntrada else None,
            'HoraSaida': self.HoraSaida.isoformat() if self.HoraSaida else None,
            'Observacao': self.Observacao
        }
    
    def __repr__(self):
        return f'<Presenca {self.PresencaID} - {self.Data}>'

class Licenca(Base):
    __tablename__ = 'Licencas'
    
    LicencaID = Column(Integer, primary_key=True, autoincrement=True)
    FuncionarioID = Column(Integer, ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    TipoLicenca = Column(String(50), nullable=True)
    DataInicio = Column(Date, nullable=True)
    DataFim = Column(Date, nullable=True)
    Estado = Column(String(20), nullable=True)
    
    def to_dict(self):
        return {
            'LicencaID': self.LicencaID,
            'FuncionarioID': self.FuncionarioID,
            'TipoLicenca': self.TipoLicenca,
            'DataInicio': self.DataInicio.isoformat() if self.DataInicio else None,
            'DataFim': self.DataFim.isoformat() if self.DataFim else None,
            'Estado': self.Estado
        }
    
    def __repr__(self):
        return f'<Licenca {self.LicencaID} - {self.TipoLicenca}>'

class Formacao(Base):
    __tablename__ = 'Formacoes'
    
    FormacaoID = Column(Integer, primary_key=True, autoincrement=True)
    FuncionarioID = Column(Integer, ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    NomeCurso = Column(String(200), nullable=True)
    Instituicao = Column(String(200), nullable=True)
    DataInicio = Column(Date, nullable=True)
    DataFim = Column(Date, nullable=True)
    Certificado = Column(Boolean, nullable=True)  # BIT no SQL Server
    
    def to_dict(self):
        return {
            'FormacaoID': self.FormacaoID,
            'FuncionarioID': self.FuncionarioID,
            'NomeCurso': self.NomeCurso,
            'Instituicao': self.Instituicao,
            'DataInicio': self.DataInicio.isoformat() if self.DataInicio else None,
            'DataFim': self.DataFim.isoformat() if self.DataFim else None,
            'Certificado': self.Certificado
        }
    
    def __repr__(self):
        return f'<Formacao {self.FormacaoID} - {self.NomeCurso}>'

class AvaliacaoDesempenho(Base):
    __tablename__ = 'AvaliacoesDesempenho'
    
    AvaliacaoID = Column(Integer, primary_key=True, autoincrement=True)
    FuncionarioID = Column(Integer, ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    DataAvaliacao = Column(Date, nullable=False)
    Avaliador = Column(String(150), nullable=True)
    Pontuacao = Column(Integer, nullable=True)  # 0-100
    Comentarios = Column(String(500), nullable=True)
    
    def to_dict(self):
        return {
            'AvaliacaoID': self.AvaliacaoID,
            'FuncionarioID': self.FuncionarioID,
            'DataAvaliacao': self.DataAvaliacao.isoformat() if self.DataAvaliacao else None,
            'Avaliador': self.Avaliador,
            'Pontuacao': self.Pontuacao,
            'Comentarios': self.Comentarios
        }
    
    def __repr__(self):
        return f'<AvaliacaoDesempenho {self.AvaliacaoID} - {self.Pontuacao}>'

class FolhaSalarial(Base):
    __tablename__ = 'FolhaSalarial'
    
    FolhaID = Column(Integer, primary_key=True, autoincrement=True)
    FuncionarioID = Column(Integer, ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    PeriodoInicio = Column(Date, nullable=False)
    PeriodoFim = Column(Date, nullable=False)
    SalarioBase = Column(Numeric(18, 2), nullable=False)
    Bonificacoes = Column(Numeric(18, 2), nullable=True, default=0)
    Descontos = Column(Numeric(18, 2), nullable=True, default=0)
    # ValorLiquido será calculado como coluna computada no banco
    DataPagamento = Column(Date, nullable=True)
    
    def to_dict(self):
        # Calcular valor líquido quando retornar os dados
        valor_liquido = 0
        if self.SalarioBase:
            valor_liquido = float(self.SalarioBase)
            if self.Bonificacoes:
                valor_liquido += float(self.Bonificacoes)
            if self.Descontos:
                valor_liquido -= float(self.Descontos)
        
        return {
            'FolhaID': self.FolhaID,
            'FuncionarioID': self.FuncionarioID,
            'PeriodoInicio': self.PeriodoInicio.isoformat() if self.PeriodoInicio else None,
            'PeriodoFim': self.PeriodoFim.isoformat() if self.PeriodoFim else None,
            'SalarioBase': float(self.SalarioBase) if self.SalarioBase else None,
            'Bonificacoes': float(self.Bonificacoes) if self.Bonificacoes else None,
            'Descontos': float(self.Descontos) if self.Descontos else None,
            'ValorLiquido': valor_liquido,
            'DataPagamento': self.DataPagamento.isoformat() if self.DataPagamento else None
        }
    
    def __repr__(self):
        return f'<FolhaSalarial {self.FolhaID} - {self.FuncionarioID}>'

class Beneficio(Base):
    __tablename__ = 'Beneficios'
    
    BeneficioID = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(100), nullable=False)
    Descricao = Column(String(255), nullable=True)
    Tipo = Column(String(50), nullable=True)  # Saúde, Transporte, Alimentação, Seguro, etc.
    
    def to_dict(self):
        return {
            'BeneficioID': self.BeneficioID,
            'Nome': self.Nome,
            'Descricao': self.Descricao,
            'Tipo': self.Tipo
        }
    
    def __repr__(self):
        return f'<Beneficio {self.Nome}>'

class FuncionarioBeneficio(Base):
    __tablename__ = 'FuncionarioBeneficio'
    
    FuncionarioBeneficioID = Column(Integer, primary_key=True, autoincrement=True)
    FuncionarioID = Column(Integer, ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    BeneficioID = Column(Integer, ForeignKey('Beneficios.BeneficioID'), nullable=False)
    DataInicio = Column(Date, nullable=False)
    DataFim = Column(Date, nullable=True)
    Estado = Column(String(20), nullable=True)  # Activo, Suspenso, Finalizado
    
    def to_dict(self):
        return {
            'FuncionarioBeneficioID': self.FuncionarioBeneficioID,
            'FuncionarioID': self.FuncionarioID,
            'BeneficioID': self.BeneficioID,
            'DataInicio': self.DataInicio.isoformat() if self.DataInicio else None,
            'DataFim': self.DataFim.isoformat() if self.DataFim else None,
            'Estado': self.Estado
        }
    
    def __repr__(self):
        return f'<FuncionarioBeneficio {self.FuncionarioBeneficioID}>'
