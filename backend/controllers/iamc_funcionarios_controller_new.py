from flask import jsonify, request
from models.iamc_funcionarios_new import Funcionario, Departamento, Cargo, HistoricoCargoFuncionario, Contrato
from models.iamc_presencas_new import Presenca, Licenca
from extensions import IAMCSession
from utils.db_utils import obtener_conexion_local
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FuncionarioController:
    
    @staticmethod
    def listar_todos():
        """Listar todos os funcionários com paginação e nomes de Cargo e Departamento"""
        session = None
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            
            # Calcular offset
            offset = (page - 1) * per_page
            
            session = IAMCSession()
            
            # Set timeout
            from sqlalchemy import text
            session.execute(text("SET LOCK_TIMEOUT 5000"))  # 5 second timeout
            
            # Consultar funcionários com JOINs para obter nomes de Cargo e Departamento
            funcionarios_query = session.query(
                Funcionario.FuncionarioID,
                Funcionario.Nome,
                Funcionario.Apelido,
                Funcionario.Email,
                Funcionario.Telefone,
                Funcionario.DataAdmissao,
                Funcionario.EstadoFuncionario,
                Cargo.Nome.label('CargoNome'),
                Departamento.Nome.label('DepartamentoNome'),
                Funcionario.CargoID,
                Funcionario.DepartamentoID
            ).outerjoin(
                Cargo, Funcionario.CargoID == Cargo.CargoID
            ).outerjoin(
                Departamento, Funcionario.DepartamentoID == Departamento.DepartamentoID
            ).order_by(Funcionario.FuncionarioID).offset(offset).limit(per_page)
            
            funcionarios = funcionarios_query.all()
            
            # Contar total sin JOINs para mejor performance
            total = session.query(Funcionario).count()
            
            # Calcular número total de páginas
            pages = (total + per_page - 1) // per_page
            
            # Procesar datos para incluir nombres de cargo y departamento
            funcionarios_data = []
            for func in funcionarios:
                funcionarios_data.append({
                    'FuncionarioID': func.FuncionarioID,
                    'Nome': func.Nome,
                    'Apelido': func.Apelido or '',
                    'Email': func.Email or '',
                    'Telefone': func.Telefone or '',
                    'DataAdmissao': func.DataAdmissao.strftime('%d/%m/%Y') if func.DataAdmissao else '',
                    'EstadoFuncionario': func.EstadoFuncionario or 'Activo',
                    'CargoID': func.CargoID,
                    'DepartamentoID': func.DepartamentoID,
                    'CargoNome': func.CargoNome or 'Não especificado',
                    'DepartamentoNome': func.DepartamentoNome or 'Não especificado',
                    # Campos adicionales para compatibilidad
                    'nomeCompleto': f"{func.Nome or ''} {func.Apelido or ''}".strip(),
                    'id': func.FuncionarioID,
                    'cargo': {'nome': func.CargoNome or 'Não especificado'},
                    'departamento': {'nome': func.DepartamentoNome or 'Não especificado'}
                })
            
            return jsonify({
                'success': True,
                'data': funcionarios_data,
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': pages
            }), 200
        except Exception as e:
            logger.error(f"Erro ao listar funcionários: {str(e)}")
            logger.error(f"Tipo do erro: {type(e)}")
            import traceback
            logger.error(f"Traceback completo: {traceback.format_exc()}")
            
            # Return empty list as fallback
            return jsonify({
                'success': False, 
                'error': 'Database IAMC não acessível',
                'data': [],
                'total': 0,
                'page': 1,
                'per_page': 20,
                'pages': 0
            }), 200  # Return 200 to avoid frontend errors
        finally:
            if session:
                try:
                    session.close()
                except:
                    pass
    
    @staticmethod
    def listar_funcionarios_com_qr():
        """Listar funcionários que têm códigos QR gerados, com nomes de Cargo e Departamento"""
        session = IAMCSession()
        try:
            # Primeiro, obter os IDs de funcionários que têm QR codes
            # Conectar à base de dados local para obter os QR codes
            conn_local = obtener_conexion_local()
            cursor_local = conn_local.cursor()
            cursor_local.execute("SELECT contact_id FROM qr_codes")
            qr_generated_ids = [row[0] for row in cursor_local.fetchall()]
            conn_local.close()
            
            if not qr_generated_ids:
                return jsonify({
                    'success': True,
                    'data': []
                }), 200
            
            # Consultar funcionários com JOINs para obter nomes de Cargo e Departamento
            funcionarios_query = session.query(
                Funcionario.FuncionarioID,
                Funcionario.Nome,
                Funcionario.Apelido,
                Funcionario.Email,
                Funcionario.Telefone,
                Cargo.Nome.label('CargoNome'),
                Departamento.Nome.label('DepartamentoNome'),
                Funcionario.CargoID,
                Funcionario.DepartamentoID
            ).outerjoin(
                Cargo, Funcionario.CargoID == Cargo.CargoID
            ).outerjoin(
                Departamento, Funcionario.DepartamentoID == Departamento.DepartamentoID
            ).filter(
                Funcionario.FuncionarioID.in_(qr_generated_ids)
            ).order_by(Funcionario.FuncionarioID)
            
            funcionarios = funcionarios_query.all()
            
            # Procesar dados
            result = []
            for func in funcionarios:
                result.append({
                    'id': func.FuncionarioID,  # Para compatibilidade com frontend
                    'funcionarioId': func.FuncionarioID,
                    'nome': func.Nome,
                    'apelido': func.Apelido,
                    'email': func.Email,
                    'telefone': func.Telefone,
                    'cargo': func.CargoNome,
                    'cargoId': func.CargoID,
                    'departamento': func.DepartamentoNome,
                    'departamentoId': func.DepartamentoID,
                    'qrGenerated': True
                })
            
            logger.info(f"Funcionários com QR encontrados: {len(result)}")
            
            return jsonify({
                'success': True,
                'data': result
            }), 200
            
        except Exception as e:
            logger.error(f"Erro ao listar funcionários com QR: {str(e)}")
            logger.error(f"Tipo do erro: {type(e)}")
            import traceback
            logger.error(f"Traceback completo: {traceback.format_exc()}")
            return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500
        finally:
            session.close()
    
    @staticmethod
    def obter_por_id(funcionario_id):
        """Obter funcionário por ID"""
        session = IAMCSession()
        try:
            funcionario = session.query(Funcionario).filter(Funcionario.FuncionarioID == funcionario_id).first()
            if not funcionario:
                return jsonify({'success': False, 'error': 'Funcionário não encontrado'}), 404
                
            return jsonify({
                'success': True,
                'funcionario': funcionario.to_dict()
            }), 200
        except Exception as e:
            logger.error(f"Erro ao obter funcionário: {str(e)}")
            return jsonify({'success': False, 'error': 'Funcionário não encontrado'}), 404
        finally:
            session.close()
    
    @staticmethod
    def criar():
        """Criar novo funcionário"""
        session = IAMCSession()
        try:
            dados = request.get_json()
            
            # Support both camelCase (frontend) and PascalCase (backend)
            nome = dados.get('nome') or dados.get('Nome')
            apelido = dados.get('apelido') or dados.get('Apelido')
            bi = dados.get('bi') or dados.get('BI')
            
            # Validar campos obrigatórios
            if not nome or not apelido or not bi:
                return jsonify({
                    'success': False, 
                    'error': 'Nome, apelido e BI são obrigatórios'
                }), 400
            
            # Verificar se BI já existe
            existing = session.query(Funcionario).filter(Funcionario.BI == bi).first()
            if existing:
                return jsonify({
                    'success': False,
                    'error': 'Já existe um funcionário com este BI'
                }, 400)
            
            # Handle date fields from camelCase
            data_nascimento = dados.get('dataNascimento') or dados.get('DataNascimento')
            data_admissao = dados.get('dataAdmissao') or dados.get('DataAdmissao')
            
            # Handle cargo and departamento fields
            cargo_id = dados.get('cargoID') or dados.get('CargoID')
            departamento_id = dados.get('departamentoID') or dados.get('DepartamentoID')
            
            funcionario = Funcionario(
                Nome=nome,
                Apelido=apelido,
                BI=bi,
                DataNascimento=datetime.strptime(data_nascimento, '%Y-%m-%d').date() if data_nascimento else None,
                Sexo=dados.get('sexo') or dados.get('Sexo'),
                EstadoCivil=dados.get('estadoCivil') or dados.get('EstadoCivil'),
                Email=dados.get('email') or dados.get('Email'),
                Telefone=dados.get('telefone') or dados.get('Telefone'),
                Endereco=dados.get('endereco') or dados.get('Endereco'),
                DataAdmissao=datetime.strptime(data_admissao, '%Y-%m-%d').date() if data_admissao else datetime.now().date(),
                EstadoFuncionario=dados.get('estadoFuncionario') or dados.get('EstadoFuncionario', 'Activo'),
                Foto=dados.get('foto') or dados.get('Foto'),  # Caminho da foto (será definido via upload)
                CargoID=cargo_id,
                DepartamentoID=departamento_id
            )
            
            session.add(funcionario)
            session.commit()
            
            return jsonify({
                'success': True,
                'data': funcionario.to_dict(),
                'message': 'Funcionário criado com sucesso'
            }), 201
            
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao criar funcionário: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao criar funcionário'}), 500
        finally:
            session.close()
    
    @staticmethod
    def atualizar(funcionario_id):
        """Atualizar funcionário"""
        session = IAMCSession()
        try:
            funcionario = session.query(Funcionario).filter(Funcionario.FuncionarioID == funcionario_id).first()
            if not funcionario:
                return jsonify({'success': False, 'error': 'Funcionário não encontrado'}), 404
                
            dados = request.get_json()
            
            # Atualizar campos se fornecidos (support both camelCase and PascalCase)
            if dados.get('Nome') or dados.get('nome'):
                funcionario.Nome = dados.get('Nome') or dados.get('nome')
            if dados.get('Apelido') or dados.get('apelido'):
                funcionario.Apelido = dados.get('Apelido') or dados.get('apelido')
            if dados.get('BI') or dados.get('bi'):
                # Verificar se o novo BI não está em uso por outro funcionário
                new_bi = dados.get('BI') or dados.get('bi')
                existing = session.query(Funcionario).filter(
                    Funcionario.BI == new_bi, 
                    Funcionario.FuncionarioID != funcionario_id
                ).first()
                if existing:
                    return jsonify({
                        'success': False,
                        'error': 'Já existe um funcionário com este BI'
                    }), 400
                funcionario.BI = new_bi
            if dados.get('DataNascimento') or dados.get('dataNascimento'):
                data_nasc = dados.get('DataNascimento') or dados.get('dataNascimento')
                funcionario.DataNascimento = datetime.strptime(data_nasc, '%Y-%m-%d').date() if data_nasc else None
            if dados.get('Sexo') or dados.get('sexo'):
                funcionario.Sexo = dados.get('Sexo') or dados.get('sexo')
            if dados.get('EstadoCivil') or dados.get('estadoCivil'):
                funcionario.EstadoCivil = dados.get('EstadoCivil') or dados.get('estadoCivil')
            if dados.get('Email') or dados.get('email'):
                funcionario.Email = dados.get('Email') or dados.get('email')
            if dados.get('Telefone') or dados.get('telefone'):
                funcionario.Telefone = dados.get('Telefone') or dados.get('telefone')
            if dados.get('Endereco') or dados.get('endereco'):
                funcionario.Endereco = dados.get('Endereco') or dados.get('endereco')
            if dados.get('EstadoFuncionario') or dados.get('estadoFuncionario'):
                funcionario.EstadoFuncionario = dados.get('EstadoFuncionario') or dados.get('estadoFuncionario')
            if dados.get('Foto') or dados.get('foto'):
                funcionario.Foto = dados.get('Foto') or dados.get('foto')
            if dados.get('CargoID') or dados.get('cargoID'):
                funcionario.CargoID = dados.get('CargoID') or dados.get('cargoID')
            if dados.get('DepartamentoID') or dados.get('departamentoID'):
                funcionario.DepartamentoID = dados.get('DepartamentoID') or dados.get('departamentoID')
            
            session.commit()
            
            return jsonify({
                'success': True,
                'data': funcionario.to_dict(),
                'message': 'Funcionário atualizado com sucesso'
            }), 200
            
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao atualizar funcionário: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao atualizar funcionário'}), 500
        finally:
            session.close()
    
    @staticmethod
    def eliminar(funcionario_id):
        """Eliminar funcionário"""
        session = IAMCSession()
        try:
            funcionario = session.query(Funcionario).filter(Funcionario.FuncionarioID == funcionario_id).first()
            if not funcionario:
                return jsonify({'success': False, 'error': 'Funcionário não encontrado'}), 404
            
            session.delete(funcionario)
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Funcionário eliminado com sucesso'
            }), 200
            
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao eliminar funcionário: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao eliminar funcionário'}), 500
        finally:
            session.close()

    @staticmethod
    def upload_foto(funcionario_id):
        """Upload da foto do funcionário (tipo visa)"""
        from flask import request, current_app
        from werkzeug.utils import secure_filename
        import os
        import uuid
        from PIL import Image
        
        session = IAMCSession()
        try:
            # Verificar se funcionário existe
            funcionario = session.query(Funcionario).filter(Funcionario.FuncionarioID == funcionario_id).first()
            if not funcionario:
                return jsonify({'success': False, 'error': 'Funcionário não encontrado'}), 404
            
            # Verificar se arquivo foi enviado
            if 'foto' not in request.files:
                return jsonify({'success': False, 'error': 'Nenhum arquivo enviado'}), 400
            
            arquivo = request.files['foto']
            if arquivo.filename == '':
                return jsonify({'success': False, 'error': 'Nenhum arquivo selecionado'}), 400
            
            # Verificar extensão do arquivo
            extensoes_permitidas = {'png', 'jpg', 'jpeg'}
            if '.' not in arquivo.filename or arquivo.filename.rsplit('.', 1)[1].lower() not in extensoes_permitidas:
                return jsonify({'success': False, 'error': 'Tipo de arquivo não permitido. Use PNG, JPG ou JPEG'}), 400
            
            # Gerar nome único para o arquivo
            extensao = arquivo.filename.rsplit('.', 1)[1].lower()
            nome_arquivo = f"funcionario_{funcionario_id}_{uuid.uuid4().hex[:8]}.{extensao}"
            nome_seguro = secure_filename(nome_arquivo)
            
            # Definir diretório de upload
            upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'fotos_funcionarios')
            os.makedirs(upload_dir, exist_ok=True)
            
            caminho_arquivo = os.path.join(upload_dir, nome_seguro)
            
            # Salvar arquivo temporariamente
            arquivo.save(caminho_arquivo)
            
            # Processar imagem para formato tipo visa (3x4 cm, aproximadamente 354x472 pixels a 300 DPI)
            try:
                with Image.open(caminho_arquivo) as img:
                    # Converter para RGB se necessário
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Redimensionar mantendo proporção e cortando para 3:4
                    target_width, target_height = 354, 472
                    img_ratio = img.width / img.height
                    target_ratio = target_width / target_height
                    
                    if img_ratio > target_ratio:
                        # Imagem muito larga, cortar nas laterais
                        new_width = int(img.height * target_ratio)
                        left = (img.width - new_width) // 2
                        img = img.crop((left, 0, left + new_width, img.height))
                    else:
                        # Imagem muito alta, cortar na parte superior/inferior
                        new_height = int(img.width / target_ratio)
                        top = (img.height - new_height) // 2
                        img = img.crop((0, top, img.width, top + new_height))
                    
                    # Redimensionar para tamanho final
                    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    
                    # Salvar imagem processada
                    img.save(caminho_arquivo, 'JPEG', quality=90)
                    
            except Exception as img_error:
                # Remover arquivo em caso de erro no processamento
                if os.path.exists(caminho_arquivo):
                    os.remove(caminho_arquivo)
                return jsonify({'success': False, 'error': f'Erro ao processar imagem: {str(img_error)}'}), 400
            
            # Remover foto anterior se existir
            if funcionario.Foto:
                foto_anterior = os.path.join(upload_dir, os.path.basename(funcionario.Foto))
                if os.path.exists(foto_anterior):
                    try:
                        os.remove(foto_anterior)
                    except:
                        pass  # Ignorar erro ao remover arquivo anterior
            
            # Atualizar funcionário com caminho da nova foto
            funcionario.Foto = nome_seguro
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Foto do funcionário atualizada com sucesso',
                'foto_url': f'/api/iamc/uploads/fotos_funcionarios/{nome_seguro}',
                'funcionario': funcionario.to_dict()
            }), 200
            
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao fazer upload da foto: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao fazer upload da foto'}), 500
        finally:
            session.close()
    
    @staticmethod
    def obter_foto(funcionario_id):
        """Obter informações da foto do funcionário"""
        session = IAMCSession()
        try:
            funcionario = session.query(Funcionario).filter(Funcionario.FuncionarioID == funcionario_id).first()
            if not funcionario:
                return jsonify({'success': False, 'error': 'Funcionário não encontrado'}), 404
            
            if not funcionario.Foto:
                return jsonify({'success': False, 'error': 'Funcionário não possui foto'}), 404
            
            return jsonify({
                'success': True,
                'foto_url': f'/api/iamc/uploads/fotos_funcionarios/{funcionario.Foto}',
                'funcionario_id': funcionario_id,
                'nome': f'{funcionario.Nome} {funcionario.Apelido}'
            }), 200
            
        except Exception as e:
            logger.error(f"Erro ao obter foto: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao obter foto'}), 500
        finally:
            session.close()
    
    @staticmethod
    def remover_foto(funcionario_id):
        """Remover foto do funcionário"""
        import os
        
        session = IAMCSession()
        try:
            funcionario = session.query(Funcionario).filter(Funcionario.FuncionarioID == funcionario_id).first()
            if not funcionario:
                return jsonify({'success': False, 'error': 'Funcionário não encontrado'}), 404
            
            if not funcionario.Foto:
                return jsonify({'success': False, 'error': 'Funcionário não possui foto'}), 404
            
            # Remover arquivo físico
            upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'fotos_funcionarios')
            caminho_arquivo = os.path.join(upload_dir, funcionario.Foto)
            
            if os.path.exists(caminho_arquivo):
                try:
                    os.remove(caminho_arquivo)
                except:
                    pass  # Ignorar erro ao remover arquivo
            
            # Remover referência do banco
            funcionario.Foto = None
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Foto do funcionário removida com sucesso',
                'funcionario': funcionario.to_dict()
            }), 200
            
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao remover foto: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao remover foto'}), 500
        finally:
            session.close()

    @staticmethod
    def dashboard_metrics():
        """Obter métricas do dashboard RRHH"""
        session = IAMCSession()
        try:
            # Total de funcionários
            total_funcionarios = session.query(Funcionario).count()
            
            # Funcionários ativos
            funcionarios_ativos = session.query(Funcionario).filter(
                Funcionario.EstadoFuncionario == 'Activo'
            ).count()
            
            # Funcionários por departamento
            from sqlalchemy import func
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
            
            # Contratações por mês (simplificado)
            contratacoes_mensais = []
            
            return jsonify({
                'success': True,
                'metrics': {
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
                    'contratacoesMensais': contratacoes_mensais
                }
            }), 200
            
        except Exception as e:
            logger.error(f"Erro ao obter métricas do dashboard: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({'success': False, 'error': 'Erro ao obter métricas'}), 500
        finally:
            session.close()

    @staticmethod
    def verificar_status():
        """Verificar status da conexão e dados IAMC"""
        session = None
        try:
            # Try to create session with timeout
            session = IAMCSession()
            
            # Set a query timeout 
            from sqlalchemy import text
            session.execute(text("SET LOCK_TIMEOUT 5000"))  # 5 second timeout
            
            # Verificar conexão e contar registros
            total_funcionarios = session.query(Funcionario).count()
            total_departamentos = session.query(Departamento).count()
            total_cargos = session.query(Cargo).count()
            
            # Funcionários por estado
            from sqlalchemy import func
            funcionarios_por_estado = session.query(
                Funcionario.EstadoFuncionario,
                func.count(Funcionario.FuncionarioID)
            ).group_by(Funcionario.EstadoFuncionario).all()
            
            return jsonify({
                'success': True,
                'status': 'Conectado',
                'dados': {
                    'totalFuncionarios': total_funcionarios,
                    'totalDepartamentos': total_departamentos,
                    'totalCargos': total_cargos,
                    'funcionariosPorEstado': {
                        estado: total for estado, total in funcionarios_por_estado
                    }
                },
                'timestamp': datetime.now().isoformat()
            }), 200
            
        except Exception as e:
            logger.error(f"Erro ao verificar status IAMC: {str(e)}")
            # Return a basic status even if database is not accessible
            return jsonify({
                'success': False,
                'status': 'Erro de conexão - Database IAMC não acessível',
                'error': str(e),
                'dados': {
                    'totalFuncionarios': 0,
                    'totalDepartamentos': 0,
                    'totalCargos': 0,
                    'funcionariosPorEstado': {}
                },
                'timestamp': datetime.now().isoformat()
            }), 200  # Return 200 instead of 500 to avoid frontend errors
        finally:
            if session:
                try:
                    session.close()
                except:
                    pass

    @staticmethod
    def listar_funcionarios_com_qr():
        """Listar funcionários que têm códigos QR gerados, com nomes de Cargo e Departamento"""
        session = IAMCSession()
        try:
            # Primeiro, obter os IDs de funcionários que têm QR codes
            # Conectar à base de dados local para obter os QR codes
            from utils.db_utils import obtener_conexion_local
            conn_local = obtener_conexion_local()
            cursor_local = conn_local.cursor()
            cursor_local.execute("SELECT contact_id FROM qr_codes")
            qr_generated_ids = [row[0] for row in cursor_local.fetchall()]
            conn_local.close()
            
            if not qr_generated_ids:
                return jsonify({
                    'success': True,
                    'data': []
                }), 200
            
            # Consultar funcionários com JOINs para obter nomes de Cargo e Departamento
            funcionarios_query = session.query(
                Funcionario.FuncionarioID,
                Funcionario.Nome,
                Funcionario.Apelido,
                Funcionario.Email,
                Funcionario.Telefone,
                Cargo.Nome.label('CargoNome'),
                Departamento.Nome.label('DepartamentoNome'),
                Funcionario.CargoID,
                Funcionario.DepartamentoID
            ).outerjoin(
                Cargo, Funcionario.CargoID == Cargo.CargoID
            ).outerjoin(
                Departamento, Funcionario.DepartamentoID == Departamento.DepartamentoID
            ).filter(
                Funcionario.FuncionarioID.in_(qr_generated_ids)
            ).order_by(Funcionario.FuncionarioID)
            
            funcionarios = funcionarios_query.all()
            
            # Procesar dados
            result = []
            for func in funcionarios:
                result.append({
                    'id': func.FuncionarioID,  # Para compatibilidade com frontend
                    'funcionarioId': func.FuncionarioID,
                    'nome': func.Nome,
                    'apelido': func.Apelido,
                    'email': func.Email,
                    'telefone': func.Telefone,
                    'cargo': func.CargoNome,
                    'cargoId': func.CargoID,
                    'departamento': func.DepartamentoNome,
                    'departamentoId': func.DepartamentoID,
                    'qrGenerated': True
                })
            
            logger.info(f"Funcionários com QR encontrados: {len(result)}")
            
            return jsonify({
                'success': True,
                'data': result
            }), 200
            
        except Exception as e:
            logger.error(f"Erro ao listar funcionários com QR: {str(e)}")
            logger.error(f"Tipo do erro: {type(e)}")
            import traceback
            logger.error(f"Traceback completo: {traceback.format_exc()}")
            return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500
        finally:
            session.close()

class DepartamentoController:
    
    @staticmethod
    def listar_todos():
        """Listar todos os departamentos"""
        session = None
        try:
            session = IAMCSession()
            
            # Set timeout
            from sqlalchemy import text
            session.execute(text("SET LOCK_TIMEOUT 5000"))
            
            departamentos = session.query(Departamento).all()
            return jsonify({
                'success': True,
                'data': [d.to_dict() for d in departamentos]
            }), 200
        except Exception as e:
            logger.error(f"Erro ao listar departamentos: {str(e)}")
            # Return empty list as fallback
            return jsonify({
                'success': False, 
                'error': 'Database IAMC não acessível',
                'data': []
            }), 200
        finally:
            if session:
                try:
                    session.close()
                except:
                    pass
    
    @staticmethod
    def obter_por_id(departamento_id):
        """Obter departamento por ID"""
        session = IAMCSession()
        try:
            departamento = session.query(Departamento).filter(Departamento.DepartamentoID == departamento_id).first()
            if not departamento:
                return jsonify({'success': False, 'error': 'Departamento não encontrado'}), 404
                
            return jsonify({
                'success': True,
                'data': departamento.to_dict()
            }), 200
        except Exception as e:
            logger.error(f"Erro ao obter departamento: {str(e)}")
            return jsonify({'success': False, 'error': 'Departamento não encontrado'}), 404
        finally:
            session.close()
    
    @staticmethod
    def criar():
        """Criar novo departamento"""
        session = IAMCSession()
        try:
            dados = request.get_json()
            
            # Support both camelCase (frontend) and PascalCase (backend)
            nome = dados.get('nome') or dados.get('Nome')
            descricao = dados.get('descricao') or dados.get('Descricao')
            
            if not nome:
                return jsonify({
                    'success': False, 
                    'error': 'Nome é obrigatório'
                }), 400
            
            departamento = Departamento(
                Nome=nome,
                Descricao=descricao
            )
            
            session.add(departamento)
            session.commit()
            
            return jsonify({
                'success': True,
                'data': departamento.to_dict(),
                'message': 'Departamento criado com sucesso'
            }), 201
            
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao criar departamento: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao criar departamento'}), 500
        finally:
            session.close()
    
    @staticmethod
    def atualizar(departamento_id):
        """Atualizar departamento"""
        session = IAMCSession()
        try:
            departamento = session.query(Departamento).filter(Departamento.DepartamentoID == departamento_id).first()
            if not departamento:
                return jsonify({'success': False, 'error': 'Departamento não encontrado'}), 404
                
            dados = request.get_json()
            
            # Support both camelCase (frontend) and PascalCase (backend)
            if 'nome' in dados or 'Nome' in dados:
                departamento.Nome = dados.get('nome') or dados.get('Nome')
            if 'descricao' in dados or 'Descricao' in dados:
                departamento.Descricao = dados.get('descricao') or dados.get('Descricao')
            
            session.commit()
            
            return jsonify({
                'success': True,
                'data': departamento.to_dict(),
                'message': 'Departamento atualizado com sucesso'
            }), 200
            
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao atualizar departamento: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao atualizar departamento'}), 500
        finally:
            session.close()
    
    @staticmethod
    def eliminar(departamento_id):
        """Eliminar departamento"""
        session = IAMCSession()
        try:
            departamento = session.query(Departamento).filter(Departamento.DepartamentoID == departamento_id).first()
            if not departamento:
                return jsonify({'success': False, 'error': 'Departamento não encontrado'}), 404
            
            session.delete(departamento)
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Departamento eliminado com sucesso'
            }), 200
            
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao eliminar departamento: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao eliminar departamento'}), 500
        finally:
            session.close()
    
    # === MÉTODOS PARA CARGOS ===
    @staticmethod
    def listar_cargos():
        """Listar todos os cargos"""
        session = None
        try:
            session = IAMCSession()
            
            # Set timeout
            from sqlalchemy import text
            session.execute(text("SET LOCK_TIMEOUT 5000"))
            
            cargos = session.query(Cargo).order_by(Cargo.CargoID).all()
            return jsonify({
                'success': True,
                'data': [c.to_dict() for c in cargos],
                'total': len(cargos)
            }), 200
        except Exception as e:
            logger.error(f"Erro ao listar cargos: {str(e)}")
            # Return empty list as fallback
            return jsonify({
                'success': False, 
                'error': 'Database IAMC não acessível',
                'data': [],
                'total': 0
            }), 200
        finally:
            if session:
                try:
                    session.close()
                except:
                    pass
    
    @staticmethod
    def obter_cargo_por_id(cargo_id):
        """Obter cargo por ID"""
        session = IAMCSession()
        try:
            cargo = session.query(Cargo).filter(Cargo.CargoID == cargo_id).first()
            if not cargo:
                return jsonify({'success': False, 'error': 'Cargo não encontrado'}), 404
                
            return jsonify({
                'success': True,
                'data': cargo.to_dict()
            }), 200
        except Exception as e:
            logger.error(f"Erro ao obter cargo: {str(e)}")
            return jsonify({'success': False, 'error': 'Cargo não encontrado'}), 404
        finally:
            session.close()
    
    @staticmethod
    def criar_cargo():
        """Criar novo cargo"""
        session = IAMCSession()
        try:
            dados = request.get_json()
            
            # Support both camelCase (frontend) and PascalCase (backend)
            nome = dados.get('nome') or dados.get('Nome')
            
            if not nome:
                return jsonify({
                    'success': False, 
                    'error': 'Nome é obrigatório'
                }), 400
            
            cargo = Cargo(
                Nome=nome,
                Descricao=dados.get('descricao') or dados.get('Descricao'),
                Nivel=dados.get('nivel') or dados.get('Nivel'),
                DepartamentoID=dados.get('departamentoId') or dados.get('DepartamentoID')
            )
            
            session.add(cargo)
            session.commit()
            
            return jsonify({
                'success': True,
                'data': cargo.to_dict(),
                'message': 'Cargo criado com sucesso'
            }), 201
            
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao criar cargo: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao criar cargo'}), 500
        finally:
            session.close()
    
    @staticmethod
    def atualizar_cargo(cargo_id):
        """Atualizar cargo"""
        session = IAMCSession()
        try:
            cargo = session.query(Cargo).filter(Cargo.CargoID == cargo_id).first()
            if not cargo:
                return jsonify({'success': False, 'error': 'Cargo não encontrado'}), 404
            
            dados = request.get_json()
            
            # Support both camelCase (frontend) and PascalCase (backend)
            if 'nome' in dados or 'Nome' in dados:
                cargo.Nome = dados.get('nome') or dados.get('Nome')
            if 'descricao' in dados or 'Descricao' in dados:
                cargo.Descricao = dados.get('descricao') or dados.get('Descricao')
            if 'nivel' in dados or 'Nivel' in dados:
                cargo.Nivel = dados.get('nivel') or dados.get('Nivel')
            if 'departamentoId' in dados or 'DepartamentoID' in dados:
                cargo.DepartamentoID = dados.get('departamentoId') or dados.get('DepartamentoID')
            
            session.commit()
            
            return jsonify({
                'success': True,
                'data': cargo.to_dict(),
                'message': 'Cargo atualizado com sucesso'
            }), 200
            
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao atualizar cargo: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao atualizar cargo'}), 500
        finally:
            session.close()
    
    @staticmethod
    def eliminar_cargo(cargo_id):
        """Eliminar cargo"""
        session = IAMCSession()
        try:
            cargo = session.query(Cargo).filter(Cargo.CargoID == cargo_id).first()
            if not cargo:
                return jsonify({'success': False, 'error': 'Cargo não encontrado'}), 404
            
            session.delete(cargo)
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Cargo eliminado com sucesso'
            }), 200
            
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao eliminar cargo: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao eliminar cargo'}), 500
        finally:
            session.close()
