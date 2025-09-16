#!/usr/bin/env python3
"""
Script para probar el método dashboard metrics sin Flask context
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extensions import IAMCSession
from models.iamc_funcionarios_new import Funcionario, Departamento, Cargo, HistoricoCargoFuncionario, Contrato
from models.iamc_presencas_new import Presenca, Licenca
from datetime import datetime, timedelta
from sqlalchemy import func
import json

def dashboard_metrics_test():
    """Obter métricas do dashboard RRHH sem Flask context"""
    session = IAMCSession()
    try:
        # Total de funcionários
        total_funcionarios = session.query(Funcionario).count()
        
        # Funcionários ativos
        funcionarios_ativos = session.query(Funcionario).filter(
            Funcionario.EstadoFuncionario == 'Activo'
        ).count()
        
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
        
        # Contratações por mês - simplificado
        contratacoes_mensais = []
        
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
        
        return {'success': True, 'metrics': metrics}
        
    except Exception as e:
        print(f"Erro ao obter métricas do dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': 'Erro ao obter métricas'}
    finally:
        session.close()

def main():
    print("=== TESTE DASHBOARD METRICS SEM FLASK CONTEXT ===")
    result = dashboard_metrics_test()
    
    if result['success']:
        metrics = result['metrics']
        print(f"\n✓ SUCCESS! Status: {result['success']}")
        print(f"✓ Total Funcionários: {metrics['totalFuncionarios']}")
        print(f"✓ Funcionários Ativos: {metrics['funcionariosAtivos']}")
        print(f"✓ Funcionários Inativos: {metrics['funcionariosInativos']}")
        
        print(f"\n✓ Funcionários por Departamento:")
        for dept in metrics['funcionariosPorDepartamento']:
            print(f"  - {dept['nome']}: {dept['total']}")
            
        print(f"\n✓ Funcionários por Estado:")
        for estado in metrics['funcionariosPorEstado']:
            print(f"  - {estado['estado']}: {estado['total']}")
            
        print(f"\n✓ Funcionários por Sexo:")
        for sexo in metrics['funcionariosPorSexo']:
            print(f"  - {sexo['sexo']}: {sexo['total']}")
            
        print(f"\n=== RESPOSTA COMPLETA ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"❌ ERROR: {result['error']}")

if __name__ == '__main__':
    main()
