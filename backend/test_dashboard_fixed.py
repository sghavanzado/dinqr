#!/usr/bin/env python3
"""
Script para probar el método dashboard_metrics corregido
"""

from extensions import IAMCSession
from models.iamc_funcionarios_new import Funcionario, Departamento, Cargo, HistoricoCargoFuncionario, Contrato
from models.iamc_presencas_new import Presenca, Licenca
from datetime import datetime, timedelta
from sqlalchemy import func
import logging
import json

logger = logging.getLogger(__name__)

def test_dashboard_metrics_fixed():
    """Probar métricas del dashboard RRHH corregido"""
    session = IAMCSession()
    try:
        print("=== TESTE DO DASHBOARD METRICS CORRIGIDO ===")
        
        # Total de funcionários
        total_funcionarios = session.query(Funcionario).count()
        print(f"Total funcionários: {total_funcionarios}")
        
        # Funcionários ativos
        funcionarios_ativos = session.query(Funcionario).filter(
            Funcionario.EstadoFuncionario == 'Activo'
        ).count()
        print(f"Funcionários ativos: {funcionarios_ativos}")
        
        # Funcionários por departamento
        funcionarios_por_depto = session.query(
            Departamento.Nome.label('departamento'),
            func.count(HistoricoCargoFuncionario.FuncionarioID).label('total')
        ).join(
            HistoricoCargoFuncionario, 
            Departamento.DepartamentoID == HistoricoCargoFuncionario.DepartamentoID
        ).filter(
            HistoricoCargoFuncionario.DataFim.is_(None)  # Apenas posições atuais
        ).group_by(Departamento.Nome).all()
        
        # Funcionários por estado
        funcionarios_por_estado = session.query(
            Funcionario.EstadoFuncionario.label('estado'),
            func.count(Funcionario.FuncionarioID).label('total')
        ).group_by(Funcionario.EstadoFuncionario).all()
        
        # Funcionários por sexo
        funcionarios_por_sexo = session.query(
            Funcionario.Sexo.label('sexo'),
            func.count(Funcionario.FuncionarioID).label('total')
        ).group_by(Funcionario.Sexo).all()
        
        # Contratações por mês (última abordagem corrigida)
        print("\n=== TESTE CONTRATAÇÕES MENSAIS CORRIGIDA ===")
        um_ano_atras = datetime.now() - timedelta(days=365)
        
        contratacoes_mensais = session.query(
            func.concat(
                func.cast(func.year(Funcionario.DataAdmissao), func.varchar(4)),
                '-',
                func.right(func.concat('0', func.cast(func.month(Funcionario.DataAdmissao), func.varchar(2))), 2)
            ).label('mes'),
            func.count(Funcionario.FuncionarioID).label('total')
        ).filter(
            Funcionario.DataAdmissao >= um_ano_atras
        ).group_by(
            func.year(Funcionario.DataAdmissao),
            func.month(Funcionario.DataAdmissao)
        ).order_by(
            func.year(Funcionario.DataAdmissao),
            func.month(Funcionario.DataAdmissao)
        ).all()
        
        print("Contratações mensais:")
        for item in contratacoes_mensais:
            print(f"  Mês: {item.mes} -> Total: {item.total}")
        
        # Construir resposta completa como o controlador
        metrics = {
            'totalFuncionarios': total_funcionarios,
            'funcionariosAtivos': funcionarios_ativos,
            'funcionariosInativos': total_funcionarios - funcionarios_ativos,
            'funcionariosPorDepartamento': [
                {'nome': item.departamento, 'total': item.total}
                for item in funcionarios_por_depto
            ],
            'funcionariosPorEstado': [
                {'estado': item.estado, 'total': item.total}
                for item in funcionarios_por_estado
            ],
            'funcionariosPorSexo': [
                {'sexo': item.sexo or 'Não informado', 'total': item.total}
                for item in funcionarios_por_sexo
            ],
            'contratacoesMensais': [
                {'mes': item.mes, 'total': item.total}
                for item in contratacoes_mensais
            ]
        }
        
        print("\n=== MÉTRICAS COMPLETAS ===")
        print(json.dumps(metrics, indent=2, ensure_ascii=False))
        
        return metrics
        
    except Exception as e:
        print(f"Erro geral: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        session.close()

if __name__ == '__main__':
    result = test_dashboard_metrics_fixed()
    if result:
        print(f"\n✓ Métricas calculadas com sucesso!")
        print(f"✓ Funcionários ativos: {result['funcionariosAtivos']}")
        print(f"✓ Total funcionários: {result['totalFuncionarios']}")
