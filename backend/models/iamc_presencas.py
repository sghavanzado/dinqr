from extensions import db
from datetime import datetime, date

class Presenca(db.Model):
    __tablename__ = 'Presencas'
    
    PresencaID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FuncionarioID = db.Column(db.Integer, db.ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    Data = db.Column(db.Date, nullable=False)
    HoraEntrada = db.Column(db.Time, nullable=True)
    HoraSaida = db.Column(db.Time, nullable=True)
    Observacao = db.Column(db.String(255), nullable=True)
    
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

class Licenca(db.Model):
    __tablename__ = 'Licencas'
    
    LicencaID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FuncionarioID = db.Column(db.Integer, db.ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    TipoLicenca = db.Column(db.String(50), nullable=True)
    DataInicio = db.Column(db.Date, nullable=True)
    DataFim = db.Column(db.Date, nullable=True)
    Estado = db.Column(db.String(20), nullable=True)
    
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

class Formacao(db.Model):
    __tablename__ = 'Formacoes'
    
    FormacaoID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FuncionarioID = db.Column(db.Integer, db.ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    NomeCurso = db.Column(db.String(200), nullable=True)
    Instituicao = db.Column(db.String(200), nullable=True)
    DataInicio = db.Column(db.Date, nullable=True)
    DataFim = db.Column(db.Date, nullable=True)
    Certificado = db.Column(db.Boolean, nullable=True)  # BIT no SQL Server
    
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

class AvaliacaoDesempenho(db.Model):
    __tablename__ = 'AvaliacoesDesempenho'
    
    AvaliacaoID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FuncionarioID = db.Column(db.Integer, db.ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    DataAvaliacao = db.Column(db.Date, nullable=False)
    Avaliador = db.Column(db.String(150), nullable=True)
    Pontuacao = db.Column(db.Integer, nullable=True)  # 0-100
    Comentarios = db.Column(db.String(500), nullable=True)
    
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

class FolhaSalarial(db.Model):
    __tablename__ = 'FolhaSalarial'
    
    FolhaID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FuncionarioID = db.Column(db.Integer, db.ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    PeriodoInicio = db.Column(db.Date, nullable=False)
    PeriodoFim = db.Column(db.Date, nullable=False)
    SalarioBase = db.Column(db.Numeric(18, 2), nullable=False)
    Bonificacoes = db.Column(db.Numeric(18, 2), nullable=True, default=0)
    Descontos = db.Column(db.Numeric(18, 2), nullable=True, default=0)
    # ValorLiquido será calculado como coluna computada no banco
    DataPagamento = db.Column(db.Date, nullable=True)
    
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

class Beneficio(db.Model):
    __tablename__ = 'Beneficios'
    
    BeneficioID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(100), nullable=False)
    Descricao = db.Column(db.String(255), nullable=True)
    Tipo = db.Column(db.String(50), nullable=True)  # Saúde, Transporte, Alimentação, Seguro, etc.
    
    # Relacionamentos
    funcionario_beneficios = db.relationship('FuncionarioBeneficio', backref='beneficio', lazy=True)
    
    def to_dict(self):
        return {
            'BeneficioID': self.BeneficioID,
            'Nome': self.Nome,
            'Descricao': self.Descricao,
            'Tipo': self.Tipo
        }
    
    def __repr__(self):
        return f'<Beneficio {self.Nome}>'

class FuncionarioBeneficio(db.Model):
    __tablename__ = 'FuncionarioBeneficio'
    
    FuncionarioBeneficioID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FuncionarioID = db.Column(db.Integer, db.ForeignKey('Funcionarios.FuncionarioID'), nullable=False)
    BeneficioID = db.Column(db.Integer, db.ForeignKey('Beneficios.BeneficioID'), nullable=False)
    DataInicio = db.Column(db.Date, nullable=False)
    DataFim = db.Column(db.Date, nullable=True)
    Estado = db.Column(db.String(20), nullable=True)  # Activo, Suspenso, Finalizado
    
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
        return {
            'funcionario_beneficio_id': self.funcionario_beneficio_id,
            'funcionario_id': self.funcionario_id,
            'beneficio_id': self.beneficio_id,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
            'estado': self.estado,
            'funcionario_nome': self.funcionario.nome if self.funcionario else None,
            'beneficio_nome': self.beneficio.nome if self.beneficio else None
        }
    
    def __repr__(self):
        return f'<FuncionarioBeneficio {self.funcionario.nome} - {self.beneficio.nome}>'
