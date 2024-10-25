from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models.professor import ProfessorNaoEncontrado, listar_professores, professor_por_id, adicionar_professor, atualizar_professor, excluir_professor

professor_blueprint = Blueprint('professor', __name__)

# ROTA PRINCIPAL PARA PROFESSORES
@professor_blueprint.route('/professores', methods=["GET"])
def main():
     return render_template("professores/professores.html")

# ROTA PARA LISTAR TODOS OS PROFESSORES
@professor_blueprint.route('/professores', methods=['GET'])
def get_professores():
    professores = listar_professores()
    return render_template("professores/professores.html", professores=professores)

# ROTA PARA OBTER UM PROFESSOR ESPECÍFICO POR ID
@professor_blueprint.route('/professores/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('professores/professor_id.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

# ROTA PARA EXIBIR FORMULÁRIO DE CRIAÇÃO DE UM NOVO PROFESSOR
@professor_blueprint.route('/professores/adicionar', methods=['GET'])
def adicionar_professor_page():
    return render_template('professores/criarProfessor.html')

# ROTA PARA CRIAR UM NOVO PROFESSOR
@professor_blueprint.route('/professores', methods=['POST'])
def create_professor():
    nome = request.form['nome']
    idade = request.form['idade']
    materia = request.form['materia']
    observacoes = request.form['observacoes']
    novo_professor = {
        'nome': nome,
        'idade': idade,
        'materia': materia,
        'observacoes': observacoes
    }
    adicionar_professor(novo_professor)
    return redirect(url_for('professor.get_professores'))

# ROTA PARA EXIBIR FORMULÁRIO PARA EDITAR UM PROFESSOR
@professor_blueprint.route('/professores/<int:id_professor>/editar', methods=['GET'])
def editar_professor_page(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('professores/professor_update.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

# ROTA PARA EDITAR UM PROFESSOR
@professor_blueprint.route('/professores/<int:id_professor>', methods=['POST'])
def update_professor(id_professor):
    try:
        novos_dados = {
            'nome': request.form['nome'],
            'idade': request.form['idade'],
            'materia': request.form['materia'],
            'observacoes': request.form['observacoes']
        }
        atualizar_professor(id_professor, novos_dados)
        return redirect(url_for('professor.get_professor', id_professor=id_professor))
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

# ROTA PARA DELETAR UM PROFESSOR
@professor_blueprint.route('/professores/delete/<int:id_professor>', methods=['POST'])
def delete_professor(id_professor):
    try:
        excluir_professor(id_professor)
        return redirect(url_for('professor.get_professores'))
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404
