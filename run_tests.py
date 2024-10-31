import requests
import unittest

class TestAPI(unittest.TestCase):

    BASE_URL = 'http://127.0.0.1:8000'

    def setUp(self):
        """Reseta o banco de dados antes de cada teste."""
        r_reset = requests.post(f'{self.BASE_URL}/reseta')
        self.assertEqual(r_reset.status_code, 200)

    def tearDown(self):
        """Reseta o banco de dados após cada teste."""
        requests.post(f'{self.BASE_URL}/reseta')

    # Testes para Alunos
    def test_000_alunos_retorna_lista(self):
        r = requests.get(f'{self.BASE_URL}/alunos')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)

    def test_001_adiciona_aluno_nome_em_branco(self):
        r = requests.post(f'{self.BASE_URL}/alunos', json={'nome': '', 'id': 1})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'aluno sem nome')

    def test_002_recupera_todos_os_alunos(self):
        for i in range(1, 6):
            requests.post(f'{self.BASE_URL}/alunos', json={'nome': f'Aluno {i}', 'id': i})

        r_lista = requests.get(f'{self.BASE_URL}/alunos')
        self.assertEqual(r_lista.status_code, 200)
        lista_retornada = r_lista.json()
        self.assertEqual(len(lista_retornada), 5)

    # Testes para Professores
    def test_100_professores_retorna_lista(self):
        r = requests.get(f'{self.BASE_URL}/professores')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)

    def test_101_adiciona_professor_nome_em_branco(self):
        r = requests.post(f'{self.BASE_URL}/professores', json={'nome': '', 'id': 1})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'professor sem nome')

    def test_102_adiciona_professor_id_inexistente(self):
        r = requests.post(f'{self.BASE_URL}/professores', json={'nome': 'Prof. Carlos', 'id': 1})
        self.assertEqual(r.status_code, 200)
        r_id_inexistente = requests.post(f'{self.BASE_URL}/professores', json={'nome': 'Prof. Carlos', 'id': 1})
        self.assertEqual(r_id_inexistente.status_code, 400)
        self.assertEqual(r_id_inexistente.json()['erro'], 'id ja utilizada')

    def test_103_edita_professor_inexistente(self):
        r = requests.put(f'{self.BASE_URL}/professores/99', json={'nome': 'Prof. João'})
        self.assertIn(r.status_code, [400, 404])
        self.assertEqual(r.json()['erro'], 'professor nao encontrado')

    def test_104_deleta_professor_inexistente(self):
        r = requests.delete(f'{self.BASE_URL}/professores/99')
        self.assertIn(r.status_code, [400, 404])
        self.assertEqual(r.json()['erro'], 'professor nao encontrado')

    # Testes para Turmas
    def test_200_turmas_retorna_lista(self):
        r = requests.get(f'{self.BASE_URL}/turmas')
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)

    def test_201_adiciona_turma_nome_em_branco(self):
        r = requests.post(f'{self.BASE_URL}/turmas', json={'nome': '', 'id': 1})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'turma sem nome')

    def test_202_adiciona_turma_id_inexistente(self):
        r = requests.post(f'{self.BASE_URL}/turmas', json={'nome': 'Turma A', 'id': 1})
        self.assertEqual(r.status_code, 200)
        r_id_inexistente = requests.post(f'{self.BASE_URL}/turmas', json={'nome': 'Turma A', 'id': 1})
        self.assertEqual(r_id_inexistente.status_code, 400)
        self.assertEqual(r_id_inexistente.json()['erro'], 'id ja utilizada')

    def test_203_edita_turma_inexistente(self):
        r = requests.put(f'{self.BASE_URL}/turmas/99', json={'nome': 'Turma B'})
        self.assertIn(r.status_code, [400, 404])
        self.assertEqual(r.json()['erro'], 'turma nao encontrada')

    def test_204_deleta_turma_inexistente(self):
        r = requests.delete(f'{self.BASE_URL}/turmas/99')
        self.assertIn(r.status_code, [400, 404])
        self.assertEqual(r.json()['erro'], 'turma nao encontrada')

if __name__ == '__main__':
    unittest.main()
