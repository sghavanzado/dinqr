#!/usr/bin/env python3
"""
Script para probar directamente el método dashboard_metrics
"""

from extensions import IAMCSession
from models.iamc_funcionarios_new import Funcionario, Departamento, Cargo, HistoricoCargoFuncionario, Contrato
from models.iamc_presencas_new import Presenca, Licenca
from datetime import datetime, timedelta
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)

def test_dashboard_metrics():
    """Probar métricas del dashboard RRHH paso a paso"""
    session = IAMCSession()
    try:
        print("=== TESTE DO DASHBOARD METRICS ===")
        
        # Total de funcionários
        total_funcionarios = session.query(Funcionario).count()
        print(f"Total funcionários: {total_funcionarios}")
        
        # Funcionários ativos
        funcionarios_ativos = session.query(Funcionario).filter(
            Funcionario.EstadoFuncionario == 'Activo'
        ).count()
        print(f"Funcionários ativos: {funcionarios_ativos}")
        
        # Debug: ver todos os estados únicos
        estados = session.query(Funcionario.EstadoFuncionario).distinct().all()
        print(f"Estados únicos encontrados: {[e[0] for e in estados]}")
        
        # Funcionários por estado
        funcionarios_por_estado = session.query(
            Funcionario.EstadoFuncionario.label('estado'),
            func.count(Funcionario.FuncionarioID).label('total')
        ).group_by(Funcionario.EstadoFuncionario).all()
        
        print("Funcionários por estado:")
        for item in funcionarios_por_estado:
            print(f"  Estado: {item.estado} -> Total: {item.total}")
        
        # Teste da consulta de departamentos
        try:
            print("\n=== TESTE DEPARTAMENTOS ===")
            funcionarios_por_depto = session.query(
                Departamento.Nome.label('departamento'),
                func.count(HistoricoCargoFuncionario.FuncionarioID).label('total')
            ).join(
                HistoricoCargoFuncionario, 
                Departamento.DepartamentoID == HistoricoCargoFuncionario.DepartamentoID
            ).filter(
                HistoricoCargoFuncionario.DataFim.is_(None)  # Apenas posições atuais
            ).group_by(Departamento.Nome).all()
            
            print("Funcionários por departamento:")
            for item in funcionarios_por_depto:
                print(f"  Departamento: {item.departamento} -> Total: {item.total}")
        except Exception as e:
            print(f"Erro na consulta de departamentos: {e}")
        
        # Teste da consulta problemática de contratações mensais
        try:
            print("\n=== TESTE CONTRATAÇÕES MENSAIS (PROBLEMÁTICA) ===")
            um_ano_atras = datetime.now() - timedelta(days=365)
            
            # Esta consulta está errada para SQL Server
            # contratacoes_mensais = session.query(
            #     func.date_format(Funcionario.DataAdmissao, '%Y-%m').label('mes'),
            #     func.count(Funcionario.FuncionarioID).label('total')
            # ).filter(
            #     Funcionario.DataAdmissao >= um_ano_atras
            # ).group_by(
            #     func.date_format(Funcionario.DataAdmissao, '%Y-%m')
            # ).order_by('mes').all()
            
            # Versão corrigida para SQL Server
            contratacoes_mensais = session.query(
                func.format(Funcionario.DataAdmissao, 'yyyy-MM').label('mes'),
                func.count(Funcionario.FuncionarioID).label('total')
            ).filter(
                Funcionario.DataAdmissao >= um_ano_atras
            ).group_by(
                func.format(Funcionario.DataAdmissao, 'yyyy-MM')
            ).order_by('mes').all()
            
            print("Contratações mensais:")
            for item in contratacoes_mensais:
                print(f"  Mês: {item.mes} -> Total: {item.total}")
                
        except Exception as e:
            print(f"Erro na consulta de contratações mensais: {e}")
            import traceback
            traceback.print_exc()
        
        return {
            'totalFuncionarios': total_funcionarios,
            'funcionariosAtivos': funcionarios_ativos,
            'funcionariosInativos': total_funcionarios - funcionarios_ativos,
        }
        
    except Exception as e:
        print(f"Erro geral: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        session.close()

if __name__ == '__main__':
    result = test_dashboard_metrics()
    print(f"\nResultado final: {result}")
