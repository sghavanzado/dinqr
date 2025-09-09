from flask import jsonify, request
from models.iamc_funcionarios_new import Funcionario, Departamento, Cargo, HistoricoCargoFuncionario, Contrato
from models.iamc_presencas_new import Presenca, Licenca
from extensions import IAMCSession
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FuncionarioController:
    
    @staticmethod
    def listar_todos():
        """Listar todos os funcionários com paginação"""
        session = IAMCSession()
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            
            # Calcular offset
            offset = (page - 1) * per_page
            
            # Consultar funcionários com ORDER BY obrigatório para SQL Server
            funcionarios = session.query(Funcionario).order_by(Funcionario.FuncionarioID).offset(offset).limit(per_page).all()
            total = session.query(Funcionario).count()
            
            return jsonify({
                'success': True,
                'funcionarios': [f.to_dict() for f in funcionarios],
                'total': total,
                'page': page,
                'per_page': per_page
            }), 200
        except Exception as e:
            logger.error(f"Erro ao listar funcionários: {str(e)}")
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
            
            # Validar campos obrigatórios
            if not dados.get('Nome') or not dados.get('Apelido') or not dados.get('BI'):
                return jsonify({
                    'success': False, 
                    'error': 'Nome, apelido e BI são obrigatórios'
                }), 400
            
            # Verificar se BI já existe
            existing = session.query(Funcionario).filter(Funcionario.BI == dados.get('BI')).first()
            if existing:
                return jsonify({
                    'success': False,
                    'error': 'Já existe um funcionário com este BI'
                }), 400
            
            funcionario = Funcionario(
                Nome=dados.get('Nome'),
                Apelido=dados.get('Apelido'),
                BI=dados.get('BI'),
                DataNascimento=datetime.strptime(dados.get('DataNascimento'), '%Y-%m-%d').date() if dados.get('DataNascimento') else None,
                Sexo=dados.get('Sexo'),
                EstadoCivil=dados.get('EstadoCivil'),
                Email=dados.get('Email'),
                Telefone=dados.get('Telefone'),
                Endereco=dados.get('Endereco'),
                DataAdmissao=datetime.strptime(dados.get('DataAdmissao'), '%Y-%m-%d').date() if dados.get('DataAdmissao') else datetime.now().date(),
                EstadoFuncionario=dados.get('EstadoFuncionario', 'Activo'),
                Foto=dados.get('Foto')  # Caminho da foto (será definido via upload)
            )
            
            session.add(funcionario)
            session.commit()
            
            return jsonify({
                'success': True,
                'funcionario': funcionario.to_dict(),
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
            
            # Atualizar campos se fornecidos
            if 'Nome' in dados:
                funcionario.Nome = dados['Nome']
            if 'Apelido' in dados:
                funcionario.Apelido = dados['Apelido']
            if 'BI' in dados:
                # Verificar se o novo BI não está em uso por outro funcionário
                existing = session.query(Funcionario).filter(
                    Funcionario.BI == dados['BI'], 
                    Funcionario.FuncionarioID != funcionario_id
                ).first()
                if existing:
                    return jsonify({
                        'success': False,
                        'error': 'Já existe um funcionário com este BI'
                    }), 400
                funcionario.BI = dados['BI']
            if 'DataNascimento' in dados:
                funcionario.DataNascimento = datetime.strptime(dados['DataNascimento'], '%Y-%m-%d').date() if dados['DataNascimento'] else None
            if 'Sexo' in dados:
                funcionario.Sexo = dados['Sexo']
            if 'EstadoCivil' in dados:
                funcionario.EstadoCivil = dados['EstadoCivil']
            if 'Email' in dados:
                funcionario.Email = dados['Email']
            if 'Telefone' in dados:
                funcionario.Telefone = dados['Telefone']
            if 'Endereco' in dados:
                funcionario.Endereco = dados['Endereco']
            if 'EstadoFuncionario' in dados:
                funcionario.EstadoFuncionario = dados['EstadoFuncionario']
            if 'Foto' in dados:
                funcionario.Foto = dados['Foto']
            
            session.commit()
            
            return jsonify({
                'success': True,
                'funcionario': funcionario.to_dict(),
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

class DepartamentoController:
    
    @staticmethod
    def listar_todos():
        """Listar todos os departamentos"""
        session = IAMCSession()
        try:
            departamentos = session.query(Departamento).all()
            return jsonify({
                'success': True,
                'departamentos': [d.to_dict() for d in departamentos]
            }), 200
        except Exception as e:
            logger.error(f"Erro ao listar departamentos: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500
        finally:
            session.close()
    
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
                'departamento': departamento.to_dict()
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
            
            if not dados.get('Nome'):
                return jsonify({
                    'success': False, 
                    'error': 'Nome é obrigatório'
                }), 400
            
            departamento = Departamento(
                Nome=dados.get('Nome'),
                Descricao=dados.get('Descricao')
            )
            
            session.add(departamento)
            session.commit()
            
            return jsonify({
                'success': True,
                'departamento': departamento.to_dict(),
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
            
            if 'Nome' in dados:
                departamento.Nome = dados['Nome']
            if 'Descricao' in dados:
                departamento.Descricao = dados['Descricao']
            
            session.commit()
            
            return jsonify({
                'success': True,
                'departamento': departamento.to_dict(),
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
