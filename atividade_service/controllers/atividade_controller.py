from flask import Blueprint, jsonify, request
from models import atividade_model
from clients.pessoa_service_client import PessoaServiceClient

atividade_bp = Blueprint('atividade_bp', __name__)

@atividade_bp.route('/', methods=['GET'])
def listar_atividades():
    atividades = atividade_model.listar_atividades()
    return jsonify(atividades)

@atividade_bp.route('/<int:id_atividade>', methods=['GET'])
def obter_atividade(id_atividade):
    try:
        atividade = atividade_model.obter_atividade(id_atividade)
        return jsonify(atividade)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

@atividade_bp.route('/', methods=['POST'])
def criar_atividade():
    data = request.get_json()
    id_disciplina = data.get('id_disciplina')
    enunciado = data.get('enunciado')
    respostas = data.get('respostas', [])
    
    nova_atividade = atividade_model.criar_atividade(id_disciplina, enunciado, respostas)
    return jsonify(nova_atividade), 201

@atividade_bp.route('/<int:id_atividade>/', methods=['PUT'])
def atualizar_atividade(id_atividade):
    data = request.get_json()
    id_disciplina = data.get('id_disciplina')
    enunciado = data.get('enunciado')
    respostas = data.get('respostas', [])
    
    try:
        atividade_atualizada = atividade_model.atualizar_atividade(id_atividade, id_disciplina, enunciado, respostas)
        return jsonify(atividade_atualizada)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

@atividade_bp.route('/<int:id_atividade>/', methods=['DELETE'])
def excluir_atividade(id_atividade):
    try:
        atividade_model.excluir_atividade(id_atividade)
        return jsonify({'message': 'Atividade excluída com sucesso'}), 204
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404
