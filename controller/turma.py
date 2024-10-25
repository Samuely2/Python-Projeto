from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models.turma import TurmaNaoEncontrada, listar_turmas, turma_por_id, adicionar_turma, atualizar_turma, excluir_turma

turma_blueprint = Blueprint('turma', __name__)

# ROTA PRINCIPAL PARA TURMAS
@turma_blueprint.route('/turma', methods=["GET"])
def main():
    return 'Rotas para turma'

# ROTA PARA LISTAR TODAS AS TURMAS
@turma_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = listar_turmas()
    return render_template("turmas.html", turmas=turmas)

# ROTA PARA OBTER UMA TURMA ESPECÍFICA POR ID
@turma_blueprint.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('turma_id.html', turma=turma)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404

# ROTA PARA EXIBIR FORMULÁRIO DE CRIAÇÃO DE UMA NOVA TURMA
@turma_blueprint.route('/turmas/adicionar', methods=['GET'])
def adicionar_turma_page():
    return render_template('criarTurma.html')

# ROTA PARA CRIAR UMA NOVA TURMA
@turma_blueprint.route('/turmas', methods=['POST'])
def create_turma():
    descricao = request.form['descricao']
    professor_id = request.form['professor_id']
    ativo = request.form.get('ativo') == 'on'
    nova_turma = {
        'descricao': descricao,
        'professor_id': professor_id,
        'ativo': ativo
    }
    adicionar_turma(nova_turma)
    return redirect(url_for('turma.get_turmas'))

# ROTA PARA EXIBIR FORMULÁRIO PARA EDITAR UMA TURMA
@turma_blueprint.route('/turmas/<int:id_turma>/editar', methods=['GET'])
def editar_turma_page(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('turma_update.html', turma=turma)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404

# ROTA PARA EDITAR UMA TURMA
@turma_blueprint.route('/turmas/<int:id_turma>', methods=['POST'])
def update_turma(id_turma):
    try:
        novos_dados = {
            'descricao': request.form['descricao'],
            'professor_id': request.form['professor_id'],
            'ativo': request.form.get('ativo') == 'on'
        }
        atualizar_turma(id_turma, novos_dados)
        return redirect(url_for('turma.get_turma', id_turma=id_turma))
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404

# ROTA PARA DELETAR UMA TURMA
@turma_blueprint.route('/turmas/delete/<int:id_turma>', methods=['POST'])
def delete_turma(id_turma):
    try:
        excluir_turma(id_turma)
        return redirect(url_for('turma.get_turmas'))
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404
