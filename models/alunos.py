from config import db

class Aluno(db.Model):
    __tablename__ = 'alunos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    data_nascimento = db.Column(db.Date)
    nota_primeiro_semestre = db.Column(db.Float)
    nota_segundo_semestre = db.Column(db.Float)
    media_final = db.Column(db.Float)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'))
    
    turma = db.relationship('Turma', back_populates='alunos')

    def __init__(self, nome, idade=None, data_nascimento=None, nota_primeiro_semestre=None, nota_segundo_semestre=None, turma_id=None):
        self.nome = nome
        self.idade = idade
        self.data_nascimento = data_nascimento
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.media_final = None if not (nota_primeiro_semestre and nota_segundo_semestre) else (nota_primeiro_semestre + nota_segundo_semestre) / 2
        self.turma_id = turma_id 

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'data_nascimento': self.data_nascimento,
            'nota_primeiro_semestre': self.nota_primeiro_semestre,
            'nota_segundo_semestre': self.nota_segundo_semestre,
            'media_final': self.media_final,
            'turma_id': self.turma_id
        }

    
class AlunoNaoEncontrado(Exception):
    pass

def aluno_por_id(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    return aluno.to_dict()

def listar_alunos():
    alunos = Aluno.query.all()
    return [aluno.to_dict() for aluno in alunos]

def adicionar_aluno(aluno_data):
    novo_aluno = Aluno(
        nome=aluno_data['nome'],
        idade=aluno_data.get('idade'),
        data_nascimento=aluno_data.get('data_nascimento'),
        nota_primeiro_semestre=aluno_data.get('nota_primeiro_semestre'),
        nota_segundo_semestre=aluno_data.get('nota_segundo_semestre'),
        turma_id=aluno_data.get('turma_id')
    )
    db.session.add(novo_aluno)
    db.session.commit()


def atualizar_aluno(id_aluno, novos_dados):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    aluno.nome = novos_dados.get('nome', aluno.nome)
    aluno.idade = novos_dados.get('idade', aluno.idade)
    aluno.data_nascimento = novos_dados.get('data_nascimento', aluno.data_nascimento)
    aluno.nota_primeiro_semestre = novos_dados.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
    aluno.nota_segundo_semestre = novos_dados.get('nota_segundo_semestre', aluno.nota_segundo_semestre)
    aluno.media_final = (aluno.nota_primeiro_semestre + aluno.nota_segundo_semestre) / 2 if (aluno.nota_primeiro_semestre and aluno.nota_segundo_semestre) else None
    aluno.turma_id = novos_dados.get('turma_id', aluno.turma_id)
    db.session.commit()

def excluir_aluno(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    db.session.delete(aluno)
    db.session.commit()


