"""
SIGA - Sistema Integral de Gestión de Accesos
Modelos de Control de Prestadores

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Modelos de datos para el control de prestadores de servicios.
"""

from extensions import db
from datetime import datetime


class Local(db.Model):
    """Tabla de locales/lugares"""
    __tablename__ = 'locales'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    # Relaciones
    prestadores = db.relationship('Prestador', back_populates='local', lazy='dynamic')
    
    def __repr__(self):
        return f'<Local {self.nome}>'


class Empresa(db.Model):
    """Tabla de empresas"""
    __tablename__ = 'empresas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(30))
    email = db.Column(db.String(50))
    obs = db.Column(db.Text)
    
    # Relaciones
    prestadores = db.relationship('Prestador', back_populates='empresa', lazy='dynamic')
    
    def __repr__(self):
        return f'<Empresa {self.nome}>'


class CentroNeg(db.Model):
    """Tabla de centros de negocio"""
    __tablename__ = 'centroneg'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    # Relaciones
    historiales = db.relationship('Historial', back_populates='centro_neg', lazy='dynamic')
    
    def __repr__(self):
        return f'<CentroNeg {self.nome}>'


class Function(db.Model):
    """Tabla de funciones/cargos"""
    __tablename__ = 'functions'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    
    # Relaciones
    historiales = db.relationship('Historial', back_populates='funcao', lazy='dynamic')
    
    def __repr__(self):
        return f'<Function {self.nome}>'


class TipoService(db.Model):
    """Tabla de tipos de servicio"""
    __tablename__ = 'tiposervice'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    
    # Relaciones
    historiales = db.relationship('Historial', back_populates='tipo_servico', lazy='dynamic')
    
    def __repr__(self):
        return f'<TipoService {self.nome}>'


class LocalService(db.Model):
    """Tabla de locales de servicio"""
    __tablename__ = 'localservice'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    
    # Relaciones
    historiales = db.relationship('Historial', back_populates='local_serv', lazy='dynamic')
    
    def __repr__(self):
        return f'<LocalService {self.nome}>'


class AreaService(db.Model):
    """Tabla de áreas de servicio"""
    __tablename__ = 'areaservice'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    
    # Relaciones
    historiales = db.relationship('Historial', back_populates='area', lazy='dynamic')
    
    def __repr__(self):
        return f'<AreaService {self.nome}>'


class Prestador(db.Model):
    """Tabla principal de prestadores"""
    __tablename__ = 'prestadores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    filiacao = db.Column(db.String(100))
    data_nas = db.Column(db.Date)
    local_id = db.Column(db.Integer, db.ForeignKey('locales.id'), nullable=True)
    nacionalidade = db.Column(db.String(25))
    bi_pass = db.Column(db.String(20))
    emissao = db.Column(db.Date)
    validade = db.Column(db.Date)
    local_resid = db.Column(db.String(50))
    telefono = db.Column(db.String(30))
    email = db.Column(db.String(50))
    lock = db.Column(db.Boolean, default=False)
    obs = db.Column(db.Text)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=True)
    
    # Relaciones
    local = db.relationship('Local', back_populates='prestadores')
    empresa = db.relationship('Empresa', back_populates='prestadores')
    historiales = db.relationship('Historial', back_populates='prestador', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convertir el prestador a diccionario"""
        return {
            'id': self.id,
            'nome': self.nome,
            'filiacao': self.filiacao,
            'data_nas': self.data_nas.isoformat() if self.data_nas else None,
            'local_id': self.local_id,
            'local_nome': self.local.nome if self.local else None,
            'nacionalidade': self.nacionalidade,
            'bi_pass': self.bi_pass,
            'emissao': self.emissao.isoformat() if self.emissao else None,
            'validade': self.validade.isoformat() if self.validade else None,
            'local_resid': self.local_resid,
            'telefono': self.telefono,
            'email': self.email,
            'lock': self.lock,
            'obs': self.obs,
            'empresa_id': self.empresa_id,
            'empresa_nome': self.empresa.nome if self.empresa else None
        }
    
    def __repr__(self):
        return f'<Prestador {self.nome}>'


class Historial(db.Model):
    """Tabla de historial de prestaciones"""
    __tablename__ = 'historial'
    
    id_hist = db.Column(db.Integer, primary_key=True)
    id_prest = db.Column(db.Integer, db.ForeignKey('prestadores.id'), nullable=False)
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    id_centro_neg = db.Column(db.Integer, db.ForeignKey('centroneg.id'), nullable=False)
    id_funcao = db.Column(db.Integer, db.ForeignKey('functions.id'), nullable=False)
    data_ini_prest = db.Column(db.Date, nullable=False)
    horario = db.Column(db.String(20))
    data_fim_prest = db.Column(db.Date)
    motivo = db.Column(db.String(100))
    id_tipo_servico = db.Column(db.Integer, db.ForeignKey('tiposervice.id'), nullable=False)
    id_local_serv = db.Column(db.Integer, db.ForeignKey('localservice.id'), nullable=False)
    andar = db.Column(db.String(10))
    conflito = db.Column(db.Boolean, default=False)
    quando = db.Column(db.Date)
    motivo_conflito = db.Column(db.String(100))
    id_areas = db.Column(db.Integer, db.ForeignKey('areaservice.id'), nullable=False)
    tempo = db.Column(db.String(20))
    
    # Relaciones
    prestador = db.relationship('Prestador', back_populates='historiales')
    empresa = db.relationship('Empresa', backref='historiales')
    centro_neg = db.relationship('CentroNeg', back_populates='historiales')
    funcao = db.relationship('Function', back_populates='historiales')
    tipo_servico = db.relationship('TipoService', back_populates='historiales')
    local_serv = db.relationship('LocalService', back_populates='historiales')
    area = db.relationship('AreaService', back_populates='historiales')
    
    def to_dict(self):
        """Convertir el historial a diccionario"""
        return {
            'id_hist': self.id_hist,
            'id_prest': self.id_prest,
            'id_empresa': self.id_empresa,
            'id_centro_neg': self.id_centro_neg,
            'id_funcao': self.id_funcao,
            'data_ini_prest': self.data_ini_prest.isoformat() if self.data_ini_prest else None,
            'horario': self.horario,
            'data_fim_prest': self.data_fim_prest.isoformat() if self.data_fim_prest else None,
            'motivo': self.motivo,
            'id_tipo_servico': self.id_tipo_servico,
            'id_local_serv': self.id_local_serv,
            'andar': self.andar,
            'conflito': self.conflito,
            'quando': self.quando.isoformat() if self.quando else None,
            'motivo_conflito': self.motivo_conflito,
            'id_areas': self.id_areas,
            'tempo': self.tempo
        }
    
    def __repr__(self):
        return f'<Historial {self.id_hist}>'
