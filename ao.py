from flask import Flask, jsonify, make_response, request
from estrutura_banco_de_dados import Autor, Postagem, app, db    
import jwt
from datetime import datetime, timedelta
from functools import wraps

def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'mensagem': 'Token não foi incluído!'}), 401

        try:
            resultado = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            autor = Autor.query.filter_by(id_autor=resultado['id_autor']).first()
        except:
            return jsonify({'mensagem': 'Token é inválido'}), 401

        return f(autor, *args, **kwargs)

    return decorated

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login inválido', 401, {'WW-Authenticate': 'Basic realm="Login obrigatório"'})
    
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario or auth.password != usuario.senha:
        return make_response('Login inválido', 401, {'WW-Authenticate': 'Basic realm="Login obrigatório"'})
    
    token = jwt.encode({'id_autor': usuario.id_autor, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
    return jsonify({'token': token})

@app.route('/')
@token_obrigatorio
def obter_postagens(autor):
    postagens = Postagem.query.all()
    return jsonify([{'titulo': postagem.titulo, 'conteudo': postagem.conteudo} for postagem in postagens])

@app.route('/postagem/<int:indice>', methods=['GET'])
@token_obrigatorio
def obter_postagem_por_indice(autor, indice):
    postagem = Postagem.query.get(indice)
    if not postagem:
        return jsonify({'mensagem': 'Postagem não encontrada'}), 404
    return jsonify({'titulo': postagem.titulo, 'conteudo': postagem.conteudo})

@app.route('/postagem', methods=['POST'])
@token_obrigatorio
def nova_postagem(autor):
    dados = request.get_json()
    postagem = Postagem(titulo=dados['titulo'], conteudo=dados['conteudo'])
    db.session.add(postagem)
    db.session.commit()
    return jsonify({'mensagem': 'Postagem criada com sucesso'}), 201

@app.route('/postagem/<int:indice>', methods=['PUT'])
@token_obrigatorio
def alterar_postagem(autor, indice):
    dados = request.get_json()
    postagem = Postagem.query.get(indice)
    if not postagem:
        return jsonify({'mensagem': 'Postagem não encontrada'}), 404
    postagem.titulo = dados['titulo']
    postagem.conteudo = dados['conteudo']
    db.session.commit()
    return jsonify({'mensagem': 'Postagem atualizada com sucesso'})

@app.route('/postagem/<int:indice>', methods=['DELETE'])
@token_obrigatorio
def excluir_postagem(autor, indice):
    postagem = Postagem.query.get(indice)
    if not postagem:
        return jsonify({'mensagem': 'Postagem não encontrada'}), 404
    db.session.delete(postagem)
    db.session.commit()
    return jsonify({'mensagem': 'Postagem excluída com sucesso'})

@app.route('/autores')
@token_obrigatorio
def obter_autores(autor):
    autores = Autor.query.all()
    return jsonify([{'id_autor': autor.id_autor, 'nome': autor.nome, 'email': autor.email} for autor in autores])

@app.route('/autores/<int:id_autor>', methods=['GET'])
@token_obrigatorio
def obter_autor_por_id(autor, id_autor):
    autor = Autor.query.get(id_autor)
    if not autor:
        return jsonify({'mensagem': 'Autor não encontrado'}), 404
    return jsonify({'id_autor': autor.id_autor, 'nome': autor.nome, 'email': autor.email})

@app.route('/autores', methods=['POST'])
@token_obrigatorio
def novo_autor(autor):
    dados = request.get_json()
    autor = Autor(nome=dados['nome'], senha=dados['senha'], email=dados['email'])
    db.session.add(autor)
    db.session.commit()
    return jsonify({'mensagem': 'Autor criado com sucesso'}), 201

@app.route('/autores/<int:id_autor>', methods=['PUT'])
@token_obrigatorio
def alterar_autor(autor, id_autor):
    dados = request.get_json()
    autor = Autor.query.get(id_autor)
    if not autor:
        return jsonify({'mensagem': 'Autor não encontrado'}), 404
    autor.nome = dados['nome']
    autor.email = dados['email']
    autor.senha = dados['senha']
    db.session.commit()
    return jsonify({'mensagem': 'Autor atualizado com sucesso'})

@app.route('/autores/<int:id_autor>', methods=['DELETE'])
@token_obrigatorio
def excluir_autor(autor, id_autor):
    autor = Autor.query.get(id_autor)
    if not autor:
        return jsonify({'mensagem': 'Autor não encontrado'}), 404
    db.session.delete(autor)
    db.session.commit()
    return jsonify({'mensagem': 'Autor excluído com sucesso'})

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)

