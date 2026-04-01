from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.database import produtos
from bson import ObjectId
import datetime

produtos_bp = Blueprint('produtos', __name__)

def serializar(produto):
    produto['_id'] = str(produto['_id'])
    return produto

@produtos_bp.route('/', methods=['GET'])
@jwt_required()
def listar():
    lista = [serializar(p) for p in produtos.find()]
    return jsonify(lista), 200

@produtos_bp.route('/<id>', methods=['GET'])
@jwt_required()
def buscar(id):
    produto = produtos.find_one({'_id': ObjectId(id)})
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    return jsonify(serializar(produto)), 200

@produtos_bp.route('/', methods=['POST'])
@jwt_required()
def criar():
    data = request.get_json()
    novo = {
        'nome': data['nome'],
        'descricao': data.get('descricao', ''),
        'preco': data['preco'],
        'categoria': data['categoria'],
        'disponivel': data.get('disponivel', True),
        'criado_em': datetime.datetime.utcnow(),
        'atualizado_em': datetime.datetime.utcnow()
    }
    resultado = produtos.insert_one(novo)
    novo['_id'] = str(resultado.inserted_id)
    return jsonify(novo), 201

@produtos_bp.route('/<id>', methods=['PUT'])
@jwt_required()
def editar(id):
    data = request.get_json()
    data['atualizado_em'] = datetime.datetime.utcnow()
    resultado = produtos.update_one(
        {'_id': ObjectId(id)},
        {'$set': data}
    )
    if resultado.matched_count == 0:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    return jsonify({'mensagem': 'Produto atualizado'}), 200

@produtos_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def deletar(id):
    resultado = produtos.delete_one({'_id': ObjectId(id)})
    if resultado.deleted_count == 0:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    return jsonify({'mensagem': 'Produto removido'}), 200