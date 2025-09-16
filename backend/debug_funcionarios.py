#!/usr/bin/env python3
"""
Script para diagnosticar el problema de conteo de funcionarios activos
"""

from extensions import IAMCSession
from models.iamc_funcionarios_new import Funcionario
from sqlalchemy import func

def main():
    session = IAMCSession()
    try:
        print('=== ANÁLISIS DE ESTADOS EN LA TABLA FUNCIONARIOS ===')
        funcionarios = session.query(Funcionario.FuncionarioID, Funcionario.Nome, Funcionario.EstadoFuncionario).all()
        
        print(f'Total de funcionarios en la tabla: {len(funcionarios)}')
        print()
        
        if funcionarios:
            print('Funcionarios y sus estados:')
            for f in funcionarios:
                estado_repr = repr(f.EstadoFuncionario)  # Para ver espacios en blanco y caracteres especiales
                print(f'ID: {f.FuncionarioID}, Nome: {f.Nome}, Estado: {estado_repr}')
            
            print()
            print('=== CONTAGEM POR ESTADO ===')
            # Contar por estado
            estados = session.query(
                Funcionario.EstadoFuncionario,
                func.count(Funcionario.FuncionarioID)
            ).group_by(Funcionario.EstadoFuncionario).all()
            
            for estado, count in estados:
                estado_repr = repr(estado)
                print(f'Estado {estado_repr}: {count} funcionarios')
            
            print()
            print('=== TESTE DE FILTROS ===')
            # Testar diferentes variações do filtro
            test_filters = ['Activo', 'Ativo', 'ACTIVO', 'ATIVO', 'activo', 'ativo']
            for test_filter in test_filters:
                count = session.query(Funcionario).filter(Funcionario.EstadoFuncionario == test_filter).count()
                print(f'Funcionarios com estado = \'{test_filter}\': {count}')
                
                # Teste case-insensitive
                count_ilike = session.query(Funcionario).filter(Funcionario.EstadoFuncionario.ilike(test_filter)).count()
                print(f'Funcionarios com estado ILIKE \'{test_filter}\': {count_ilike}')
            
            print()
            print('=== TESTE DE TRIM (remover espaços) ===')
            count_trimmed = session.query(Funcionario).filter(
                func.ltrim(func.rtrim(Funcionario.EstadoFuncionario)) == 'Activo'
            ).count()
            print(f'Funcionarios com estado trimmed = \'Activo\': {count_trimmed}')
            
            count_trimmed_ativo = session.query(Funcionario).filter(
                func.ltrim(func.rtrim(Funcionario.EstadoFuncionario)) == 'Ativo'
            ).count()
            print(f'Funcionarios com estado trimmed = \'Ativo\': {count_trimmed_ativo}')
            
            print()
            print('=== TESTE DO CONTROLADOR ATUAL ===')
            # Simular exatamente o que o controlador faz
            from controllers.iamc_funcionarios_controller_new import get_dashboard_metrics
            metrics = get_dashboard_metrics()
            print(f'Métricas do controlador: {metrics}')
        
        else:
            print('Nenhum funcionario encontrado na tabela!')
            
    except Exception as e:
        print(f'Erro: {e}')
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == '__main__':
    main()
