from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.database import usuarios
from bson import ObjectId
from bson.errors import InvalidId
import bcrypt

auth_bp = Blueprint('auth', __name__)


def _campos_validos(data, campos):
    """Verifica se os campos obrigatórios existem e são strings não-vazias."""
    if not data:
        return False
    for campo in campos:
        valor = data.get(campo)
        if not isinstance(valor, str) or not valor.strip():
            return False
    return True


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if not _campos_validos(data, ['email', 'senha']):
        return jsonify({'erro': 'Dados inválidos'}), 400

    usuario = usuarios.find_one({'email': data['email']})

    credenciais_invalidas = jsonify({'erro': 'Credenciais inválidas'}), 401

    if not usuario:
        return credenciais_invalidas

    senha_correta = bcrypt.checkpw(
        data['senha'].encode('utf-8'),
        usuario['senha'].encode('utf-8')
    )

    if not senha_correta:
        return credenciais_invalidas

    token = create_access_token(identity=str(usuario['_id']), additional_claims={
        'role': usuario['role']
    })

    return jsonify({
        'token': token,
        'role': usuario['role'],
        'nome': usuario['nome']
    }), 200


@auth_bp.route('/cadastrar-funcionario', methods=['POST'])
@jwt_required()
def cadastrar_funcionario():
    user_id = get_jwt_identity()
    usuario_atual = usuarios.find_one({'_id': ObjectId(user_id)})
    if not usuario_atual or usuario_atual['role'] != 'admin':
        return jsonify({'erro': 'Acesso negado'}), 403

    data = request.get_json(silent=True)
    if not _campos_validos(data, ['nome', 'email', 'senha']):
        return jsonify({'erro': 'Dados inválidos'}), 400

    if usuarios.find_one({'email': data['email']}):
        return jsonify({'erro': 'Email já cadastrado'}), 400

    senha_hash = bcrypt.hashpw(
        data['senha'].encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    usuarios.insert_one({
        'nome': data['nome'],
        'email': data['email'],
        'senha': senha_hash,
        'role': 'funcionario'
    })

    return jsonify({'mensagem': 'Funcionário cadastrado com sucesso'}), 201


@auth_bp.route('/funcionarios', methods=['GET'])
@jwt_required()
def listar_funcionarios():
    user_id = get_jwt_identity()
    usuario_atual = usuarios.find_one({'_id': ObjectId(user_id)})
    if not usuario_atual or usuario_atual['role'] != 'admin':
        return jsonify({'erro': 'Acesso negado'}), 403

    lista = list(usuarios.find({'role': 'funcionario'}, {'senha': 0}))
    for u in lista:
        u['_id'] = str(u['_id'])

    return jsonify(lista), 200


@auth_bp.route('/funcionarios/<id>', methods=['DELETE'])
@jwt_required()
def deletar_funcionario(id):
    user_id = get_jwt_identity()
    usuario_atual = usuarios.find_one({'_id': ObjectId(user_id)})
    if not usuario_atual or usuario_atual['role'] != 'admin':
        return jsonify({'erro': 'Acesso negado'}), 403

    try:
        oid = ObjectId(id)
    except InvalidId:
        return jsonify({'erro': 'ID inválido'}), 400

    resultado = usuarios.delete_one({'_id': oid, 'role': 'funcionario'})
    if resultado.deleted_count == 0:
        return jsonify({'erro': 'Funcionário não encontrado'}), 404

    return jsonify({'mensagem': 'Funcionário removido'}), 200
