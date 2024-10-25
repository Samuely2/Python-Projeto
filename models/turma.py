from config import db

class Turma(db.Model):
    __tablename__ = 'turmas'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))
    ativo = db.Column(db.Boolean, default=True)
    
    professor = db.relationship('Professor', back_populates='turmas')
    alunos = db.relationship('Aluno', back_populates='turma', cascade="all, delete-orphan")

    def __init__(self, descricao, professor_id, ativo=True):
        self.descricao = descricao
        self.professor_id = professor_id
        self.ativo = ativo

class TurmaNaoEncontrada(Exception):
    pass

def turma_por_id(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    return {
        'id': turma.id,
        'descricao': turma.descricao,
        'ativo': turma.ativo,
        'professor_id': turma.professor_id,
        'professor_nome': turma.professor.nome if turma.professor else None,
        'alunos': [{'id': aluno.id, 'nome': aluno.nome} for aluno in turma.alunos]
    }

def listar_turmas():
    turmas = Turma.query.all()
    return [{
        'id': turma.id,
        'descricao': turma.descricao,
        'ativo': turma.ativo,
        'professor_id': turma.professor_id,
        'professor_nome': turma.professor.nome if turma.professor else None
    } for turma in turmas]

def adicionar_turma(turma_data):
    nova_turma = Turma(
        descricao=turma_data['descricao'],
        professor_id=turma_data['professor_id'],
        ativo=turma_data.get('ativo', True)
    )
    db.session.add(nova_turma)
    db.session.commit()

def atualizar_turma(id_turma, novos_dados):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    turma.descricao = novos_dados.get('descricao', turma.descricao)
    turma.professor_id = novos_dados.get('professor_id', turma.professor_id)
    turma.ativo = novos_dados.get('ativo', turma.ativo)
    db.session.commit()

def excluir_turma(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    db.session.delete(turma)
    db.session.commit()
