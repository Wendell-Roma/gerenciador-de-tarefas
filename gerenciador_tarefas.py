import json
import os
from datetime import datetime

# Variaveis Globais
lista_tarefas = []
id_contador = 1
ARQUIVO_TAREFAS = 'tarefas.json'
ARQUIVO_ARQUIVADAS = 'tarefas_arquivadas.json'

# Funções
def inicializar_arquivos():
    print("Inicializando Arquivos")
    arquivos = [ARQUIVO_TAREFAS, ARQUIVO_ARQUIVADAS]
    for arquivo in arquivos:
        if not os.path.exists(arquivo):
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump([], f)
            print(f"Arquivo '{arquivo}' criado com sucesso.")

def carregar_dados():
    print("Carregando Dados")
    global lista_tarefas
    global id_contador
    
    try:
        with open(ARQUIVO_TAREFAS, 'r', encoding='utf-8') as f:
            lista_tarefas = json.load(f)
        
        if lista_tarefas:
            maior_id = max(t['id'] for t in lista_tarefas)
            id_contador = maior_id + 1
        else:
            id_contador = 1
            
    except (FileNotFoundError, json.JSONDecodeError):
        print("Arquivo de dados vazio ou não encontrado. Iniciando nova lista.")
        lista_tarefas = []

def salvar_dados():
    print("Salvando")
    with open(ARQUIVO_TAREFAS, 'w', encoding='utf-8') as f:
        json.dump(lista_tarefas, f, indent=4, ensure_ascii=False)
    print("Dados salvos com sucesso.")

def salvar_arquivadas(tarefas_para_arquivar):
    print("Salvando Tarefas Arquivadas")
    lista_arquivada = []
    if os.path.exists(ARQUIVO_ARQUIVADAS):
        with open(ARQUIVO_ARQUIVADAS, 'r', encoding='utf-8') as f:
            try:
                lista_arquivada = json.load(f)
            except json.JSONDecodeError:
                lista_arquivada = []
    
    lista_arquivada.extend(tarefas_para_arquivar)
    
    with open(ARQUIVO_ARQUIVADAS, 'w', encoding='utf-8') as f:
        json.dump(lista_arquivada, f, indent=4, ensure_ascii=False)

# Funções ciclo de vida da tarefa
def criar_tarefa():
    print("Criando tarefa")
    global lista_tarefas
    global id_contador

    print("=== Nova Tarefa ===")
    titulo = input("Título: ")
    descricao = input("Descrição: ")
    
    prioridades_validas = ['Urgente', 'Alta', 'Média', 'Baixa']
    while True:
        prioridade = input(f"Prioridade ({', '.join(prioridades_validas)}): ").capitalize()
        if prioridade in prioridades_validas:
            break
        print("Prioridade inválida. Tente novamente.")

    origens_validas = ['E-mail', 'Telefone', 'Chamado do Sistema']
    while True:
        print("Origens disponíveis: 1-E-mail, 2-Telefone, 3-Chamado do Sistema")
        try:
            opcao_origem = int(input("Selecione a origem (número): "))
            if 1 <= opcao_origem <= 3:
                origem = origens_validas[opcao_origem - 1]
                break
            else:
                print("Opção fora do intervalo.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nova_tarefa = {
        "id": id_contador,
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "status": "Pendente",
        "origem": origem,
        "data_criacao": data_criacao,
        "data_conclusao": None
    }

    lista_tarefas.append(nova_tarefa)
    print(f"Tarefa '{titulo}' criada com sucesso! ID: {id_contador}")
    id_contador += 1

def buscar_tarefa_urgente():
    print("Buscando Tarefa Urgente")
    global lista_tarefas
    
    mapa_prioridade = {'Urgente': 1, 'Alta': 2, 'Média': 3, 'Baixa': 4}
    
    pendentes = [t for t in lista_tarefas if t['status'] == 'Pendente']
    
    if not pendentes:
        print("Não há tarefas pendentes no momento.")
        return

# Ordena baseada no mapa de prioridade
    pendentes.sort(key=lambda x: mapa_prioridade.get(x['prioridade'], 5))
    
    tarefa_selecionada = pendentes[0]
    
# Atualiza status na lista original (referência)
    for t in lista_tarefas:
        if t['id'] == tarefa_selecionada['id']:
            t['status'] = 'Fazendo'
            break
            
    print(f"=== Tarefa Selecionada para Execução ===")
    print(f"ID: {tarefa_selecionada['id']} | Título: {tarefa_selecionada['titulo']}")
    print(f"Prioridade: {tarefa_selecionada['prioridade']}")
    print("Status atualizado para 'Fazendo'.")

def atualizar_prioridade():
    print("Atualizando Prioridade")
    global lista_tarefas
    
    try:
        id_busca = int(input("Digite o ID da tarefa para atualizar: "))
        tarefa = next((t for t in lista_tarefas if t['id'] == id_busca), None)
        
        if tarefa:
            print(f"Tarefa encontrada: {tarefa['titulo']} (Atual: {tarefa['prioridade']})")
            prioridades_validas = ['Urgente', 'Alta', 'Média', 'Baixa']
            while True:
                nova_prio = input(f"Nova Prioridade ({', '.join(prioridades_validas)}): ").capitalize()
                if nova_prio in prioridades_validas:
                    tarefa['prioridade'] = nova_prio
                    print("Prioridade atualizada com sucesso.")
                    break
                print("Prioridade inválida.")
        else:
            print("Tarefa não encontrada.")
    except ValueError:
        print("O ID deve ser um número inteiro.")

def concluir_tarefa():
    print("Concluindo Tarefa")
    global lista_tarefas
    
    try:
        id_busca = int(input("Digite o ID da tarefa para concluir: "))
        tarefa = next((t for t in lista_tarefas if t['id'] == id_busca), None)
        
        if tarefa:
            if tarefa['status'] in ['Concluída', 'Excluída', 'Arquivado']:
                print(f"Esta tarefa já está com status: {tarefa['status']}")
                return

            tarefa['status'] = 'Concluída'
            tarefa['data_conclusao'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Tarefa {id_busca} concluída com sucesso!")
        else:
            print("Tarefa não encontrada.")
    except ValueError:
        print("O ID deve ser um número inteiro.")

def excluir_tarefa():
    print("Excluindo Tarefa")
    global lista_tarefas
    
    try:
        id_busca = int(input("Digite o ID da tarefa para excluir: "))
        tarefa = next((t for t in lista_tarefas if t['id'] == id_busca), None)
        
        if tarefa:
            tarefa['status'] = 'Excluída'
            print(f"Tarefa {id_busca} marcada como excluída.")
        else:
            print("Tarefa não encontrada.")
    except ValueError:
        print("O ID deve ser um número inteiro.")

def processar_arquivamento():
    print("Processando Arquivos")
    global lista_tarefas
    
    tarefas_ativas = []
    tarefas_para_mover = []
    
    agora = datetime.now()
    
    for tarefa in lista_tarefas:
        mover = False
        
        if tarefa['status'] == 'Excluída':
            mover = True
        
        elif tarefa['status'] == 'Concluída' and tarefa['data_conclusao']:
            dt_conclusao = datetime.strptime(tarefa['data_conclusao'], "%Y-%m-%d %H:%M:%S")
            diferenca = agora - dt_conclusao
            if diferenca.days > 7:
                tarefa['status'] = 'Arquivado'
                mover = True
        
        if mover:
            tarefas_para_mover.append(tarefa)
        else:
            tarefas_ativas.append(tarefa)
    
    if tarefas_para_mover:
        salvar_arquivadas(tarefas_para_mover)
        lista_tarefas = tarefas_ativas
        print(f"{len(tarefas_para_mover)} tarefas foram movidas para o arquivo morto.")
    else:
        print("Nenhuma tarefa precisou ser arquivada no momento.")

# Relatorios
def gerar_relatorio():
    print("Gerando Relatorio")
    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    print(f"\n{'ID':<4} | {'Título':<20} | {'Prioridade':<10} | {'Status':<10} | {'Info Extra'}")
    print("-" * 80)
    
    for t in lista_tarefas:
        info_extra = ""
        if t['status'] == 'Concluída' and t['data_conclusao']:
            dt_criacao = datetime.strptime(t['data_criacao'], "%Y-%m-%d %H:%M:%S")
            dt_conclusao = datetime.strptime(t['data_conclusao'], "%Y-%m-%d %H:%M:%S")
            tempo = dt_conclusao - dt_criacao
            info_extra = f"Tempo: {tempo}"
        else:
            info_extra = f"Criada em: {t['data_criacao']}"

        print(f"{t['id']:<4} | {t['titulo'][:20]:<20} | {t['prioridade']:<10} | {t['status']:<10} | {info_extra}")

def gerar_relatorio_arquivados():
    print("Gerando Relatorio Arquivadas")
    if not os.path.exists(ARQUIVO_ARQUIVADAS):
        print("Arquivo de histórico não encontrado.")
        return

    try:
        with open(ARQUIVO_ARQUIVADAS, 'r', encoding='utf-8') as f:
            arquivadas = json.load(f)

        exibiveis = [t for t in arquivadas if t['status'] == 'Arquivado']
        
        if not exibiveis:
            print("Nenhuma tarefa arquivada por tempo encontrada (Excluídas são ocultas).")
            return

        print("\n--- Relatório de Arquivados (Concluídas Antigas) ---")
        for t in exibiveis:
            print(f"[ID Original: {t['id']}] {t['titulo']} - Concluída em: {t['data_conclusao']}")

    except json.JSONDecodeError:
        print("Erro ao ler arquivo de histórico.")

# Menu
def menu():
    while True:
        print("\n=== Gerenciador de Tarefas ===")
        print("1. Criar Nova Tarefa")
        print("2. Verificar/Pegar Tarefa (Urgência)")
        print("3. Atualizar Prioridade")
        print("4. Concluir Tarefa")
        print("5. Excluir Tarefa (Lógica)")
        print("6. Processar Arquivamento/Limpeza")
        print("7. Relatório de Tarefas Ativas")
        print("8. Relatório de Arquivados")
        print("9. Sair e Salvar")
        
        opcao = int(input("Escolha uma opção: "))
            
        if opcao == 1:
            criar_tarefa()
        elif opcao == 2:
            buscar_tarefa_urgente()
        elif opcao == 3:
            atualizar_prioridade()
        elif opcao == 4:
            concluir_tarefa()
        elif opcao == 5:
            excluir_tarefa()
        elif opcao == 6:
            processar_arquivamento()
        elif opcao == 7:
            gerar_relatorio()
        elif opcao == 8:
            gerar_relatorio_arquivados()
        elif opcao == 9:
            salvar_dados()
            print("Encerrando o sistema...")
            exit()
        else:
            print("Opção inválida. Escolha entre 1 e 9.")

if __name__ == "__main__":
    inicializar_arquivos()
    carregar_dados()
    menu()