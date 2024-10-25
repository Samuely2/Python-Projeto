import requests
import unittest

class TestStringMethods(unittest.TestCase):

    BASE_URL = 'http://127.0.0.1:8000'

    def test_000_alunos_retorna_lista(self):
        r = requests.get(f'{self.BASE_URL}/alunos')
        if r.status_code == 404:
            self.fail("Você não definiu a página /alunos no seu servidor")

        try:
            obj_retornado = r.json()
        except:
            self.fail("Esperava um JSON, mas você retornou outra coisa")

        self.assertEqual(type(obj_retornado), list)

    def test_001_adiciona_alunos(self):
        r1 = requests.post(f'{self.BASE_URL}/alunos', json={'nome': 'fernando', 'id': 1})
        r2 = requests.post(f'{self.BASE_URL}/alunos', json={'nome': 'roberto', 'id': 2})

        r_lista = requests.get(f'{self.BASE_URL}/alunos')
        lista_retornada = r_lista.json()

        achei_fernando = any(aluno['nome'] == 'fernando' for aluno in lista_retornada)
        achei_roberto = any(aluno['nome'] == 'roberto' for aluno in lista_retornada)

        if not achei_fernando:
            self.fail('Aluno Fernando não apareceu na lista de alunos')
        if not achei_roberto:
            self.fail('Aluno Roberto não apareceu na lista de alunos')

    def test_002_aluno_por_id(self):
        requests.post(f'{self.BASE_URL}/alunos', json={'nome': 'mario', 'id': 20})
        resposta = requests.get(f'{self.BASE_URL}/alunos/20')
        dict_retornado = resposta.json()
        
        self.assertEqual(type(dict_retornado), dict)
        self.assertIn('nome', dict_retornado)
        self.assertEqual(dict_retornado['nome'], 'mario')

    def test_003_reseta(self):
        requests.post(f'{self.BASE_URL}/alunos', json={'nome': 'cicero', 'id': 29})
        r_lista = requests.get(f'{self.BASE_URL}/alunos')
        self.assertTrue(len(r_lista.json()) > 0)

        r_reset = requests.post(f'{self.BASE_URL}/reseta')
        self.assertEqual(r_reset.status_code, 200)

        r_lista_depois = requests.get(f'{self.BASE_URL}/alunos')
        self.assertEqual(len(r_lista_depois.json()), 0)

    def test_004_deleta(self):
        requests.post(f'{self.BASE_URL}/reseta')
        self.assertEqual(requests.post(f'{self.BASE_URL}/reseta').status_code, 200)

        requests.post(f'{self.BASE_URL}/alunos', json={'nome': 'cicero', 'id': 29})
        requests.post(f'{self.BASE_URL}/alunos', json={'nome': 'lucas', 'id': 28})
        requests.post(f'{self.BASE_URL}/alunos', json={'nome': 'marta', 'id': 27})

        r_lista = requests.get(f'{self.BASE_URL}/alunos')
        lista_retornada = r_lista.json()
        self.assertEqual(len(lista_retornada), 3)

        requests.delete(f'{self.BASE_URL}/alunos/28')
        r_lista2 = requests.get(f'{self.BASE_URL}/alunos')
        lista_retornada2 = r_lista2.json()
        self.assertEqual(len(lista_retornada2), 2)

        acheiMarta = any(aluno['nome'] == 'marta' for aluno in lista_retornada)
        acheiCicero = any(aluno['nome'] == 'cicero' for aluno in lista_retornada)
        if not acheiMarta or not acheiCicero:
            self.fail("Você parece ter deletado o aluno errado!")

        requests.delete(f'{self.BASE_URL}/alunos/27')
        r_lista3 = requests.get(f'{self.BASE_URL}/alunos')
        lista_retornada3 = r_lista3.json()
        self.assertEqual(len(lista_retornada3), 1)

        if lista_retornada3[0]['nome'] != 'cicero':
            self.fail("Você parece ter deletado o aluno errado!")

    def test_005_edita(self):
        requests.post(f'{self.BASE_URL}/reseta')
        self.assertEqual(requests.post(f'{self.BASE_URL}/reseta').status_code, 200)

        requests.post(f'{self.BASE_URL}/alunos', json={'nome': 'lucas', 'id': 28})
        r_antes = requests.get(f'{self.BASE_URL}/alunos/28')
        self.assertEqual(r_antes.json()['nome'], 'lucas')

        requests.put(f'{self.BASE_URL}/alunos/28', json={'nome': 'lucas mendes'})
        r_depois = requests.get(f'{self.BASE_URL}/alunos/28')
        self.assertEqual(r_depois.json()['nome'], 'lucas mendes')
        self.assertEqual(r_depois.json()['id'], 28)

    def test_006a_id_inexistente_no_put(self):
        requests.post(f'{self.BASE_URL}/reseta')
        self.assertEqual(requests.post(f'{self.BASE_URL}/reseta').status_code, 200)

        r = requests.put(f'{self.BASE_URL}/alunos/15', json={'nome': 'bowser', 'id': 15})
        self.assertIn(r.status_code, [400, 404])
        self.assertEqual(r.json()['erro'], 'aluno nao encontrado')

    def test_006b_id_inexistente_no_get(self):
        requests.post(f'{self.BASE_URL}/reseta')
        self.assertEqual(requests.post(f'{self.BASE_URL}/reseta').status_code, 200)

        r = requests.get(f'{self.BASE_URL}/alunos/15')
        self.assertIn(r.status_code, [400, 404])
        self.assertEqual(r.json()['erro'], 'aluno nao encontrado')

    def test_006c_id_inexistente_no_delete(self):
        requests.post(f'{self.BASE_URL}/reseta')
        self.assertEqual(requests.post(f'{self.BASE_URL}/reseta').status_code, 200)

        r = requests.delete(f'{self.BASE_URL}/alunos/15')
        self.assertIn(r.status_code, [400, 404])
        self.assertEqual(r.json()['erro'], 'aluno nao encontrado')

    def test_007_id_ja_utilizada(self):
        requests.post(f'{self.BASE_URL}/reseta')
        requests.post(f'{self.BASE_URL}/alunos', json={'nome': 'aluno1', 'id': 1})
        
        r = requests.post(f'{self.BASE_URL}/alunos', json={'nome': 'aluno2', 'id': 1})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'id ja utilizada')

    def test_008a_aluno_sem_nome(self):
        r = requests.post(f'{self.BASE_URL}/alunos', json={'id': 1})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'aluno sem nome')

    def test_008b_aluno_sem_nome_no_put(self):
        requests.post(f'{self.BASE_URL}/alunos', json={'nome': 'aluno', 'id': 1})
        r = requests.put(f'{self.BASE_URL}/alunos/1', json={})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'aluno sem nome')


if __name__ == '__main__':
    unittest.main()
