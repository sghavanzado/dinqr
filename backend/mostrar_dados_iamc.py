#!/usr/bin/env python3
"""
Script para mostrar o estado atual dos dados IAMC.
"""

from flask import Flask
from models.iamc_funcionarios_new import (
    Departamento, Cargo, Funcionario, HistoricoCargoFuncionario
)
from models.iamc_presencas_new import (
    Presenca, FolhaSalarial, Beneficio, FuncionarioBeneficio
)
from config import Config
from extensions import init_iamc_db, IAMCSession

def mostrar_dados_existentes():
    """
    Mostra todos os dados existentes no banco IAMC.
    """
    try:
        # Inicializar Flask app
        app = Flask(__name__)
        app.config.from_object(Config)
        
        with app.app_context():
            # Inicializar conexão IAMC
            success = init_iamc_db(app)
            if not success:
                print("❌ Erro ao inicializar IAMC")
                return False
            
            session = IAMCSession()
            
            print("📊 Estado Atual dos Dados IAMC")
            print("=" * 50)
            
            # Departamentos
            print("\n🏢 DEPARTAMENTOS:")
            departamentos = session.query(Departamento).all()
            print(f"   Total: {len(departamentos)}")
            for dept in departamentos:
                print(f"   • {dept.DepartamentoID}: {dept.Nome}")
            
            # Cargos
            print("\n👔 CARGOS:")
            cargos = session.query(Cargo).all()
            print(f"   Total: {len(cargos)}")
            for cargo in cargos:
                print(f"   • {cargo.CargoID}: {cargo.Nome} ({cargo.Nivel})")
            
            # Funcionários
            print("\n👥 FUNCIONÁRIOS:")
            funcionarios = session.query(Funcionario).all()
            print(f"   Total: {len(funcionarios)}")
            for func in funcionarios:
                print(f"   • {func.FuncionarioID}: {func.Nome} {func.Apelido} ({func.Email})")
            
            # Histórico de Cargos
            print("\n🔗 HISTÓRICO CARGO-FUNCIONÁRIO:")
            historicos = session.query(HistoricoCargoFuncionario).all()
            print(f"   Total: {len(historicos)}")
            for hist in historicos:
                print(f"   • Funcionário {hist.FuncionarioID} -> Cargo {hist.CargoID} / Dept {hist.DepartamentoID}")
            
            # Presenças
            print("\n⏰ PRESENÇAS:")
            presencas = session.query(Presenca).all()
            print(f"   Total: {len(presencas)}")
            for pres in presencas[:3]:  # Mostrar apenas os primeiros 3
                print(f"   • Funcionário {pres.FuncionarioID}: {pres.Data} ({pres.HoraEntrada}-{pres.HoraSaida})")
            if len(presencas) > 3:
                print(f"   ... e mais {len(presencas) - 3} registros")
            
            # Benefícios
            print("\n🎁 BENEFÍCIOS:")
            beneficios = session.query(Beneficio).all()
            print(f"   Total: {len(beneficios)}")
            for ben in beneficios:
                print(f"   • {ben.BeneficioID}: {ben.Nome} ({ben.Tipo})")
            
            # Funcionário-Benefícios
            print("\n🔗 FUNCIONÁRIO-BENEFÍCIOS:")
            func_beneficios = session.query(FuncionarioBeneficio).all()
            print(f"   Total: {len(func_beneficios)}")
            for fb in func_beneficios:
                print(f"   • Funcionário {fb.FuncionarioID} -> Benefício {fb.BeneficioID} ({fb.Estado})")
            
            # Folha Salarial
            print("\n💰 FOLHAS SALARIAIS:")
            folhas = session.query(FolhaSalarial).all()
            print(f"   Total: {len(folhas)}")
            for folha in folhas:
                print(f"   • Funcionário {folha.FuncionarioID}: {folha.PeriodoInicio} a {folha.PeriodoFim}")
                print(f"     Salário Base: {folha.SalarioBase}, Bonificações: {folha.Bonificacoes}, Descontos: {folha.Descontos}")
            
            print("\n" + "=" * 50)
            print("✅ Consulta concluída!")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro ao consultar dados: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        session.close()

if __name__ == "__main__":
    mostrar_dados_existentes()
