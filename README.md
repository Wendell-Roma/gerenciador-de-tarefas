Gerenciador de Tarefas (CLI)

Uma solução robusta em linha de comando para gestão de produtividade pessoal baseada em prioridades. 

Sobre o Projeto
Este projeto foi desenvolvido como uma atividade prática para estruturação de soluções em Python. O objetivo é simular um cenário real de desenvolvimento de software, transformando requisitos de negócio numa aplicação funcional.
O sistema permite gerir o ciclo de vida de tarefas (criação, execução, conclusão e exclusão), com foco num algoritmo de priorização automática e persistência de dados via ficheiros JSON.

Funcionalidades Principais
CRUD Completo: Criação, Leitura (Relatórios), Atualização (Prioridade) e Exclusão (Lógica) de tarefas.
Priorização Inteligente: Ao solicitar uma tarefa, o sistema entrega automaticamente a mais urgente (Urgente > Alta > Média > Baixa).
Persistência de Dados: Todas as informações são salvas automaticamente em tarefas.json, garantindo que nada se perca ao fechar o programa.
Fluxo de Status: As tarefas transitam entre Pendente → Fazendo → Concluída.
Arquivamento Automático: Um sistema de limpeza move tarefas excluídas ou concluídas há mais de 7 dias para um histórico separado (tarefas_arquivadas.json), mantendo a lista principal organizada.
Validação de Dados: O sistema previne erros de digitação e entradas inválidas.

Estrutura de Arquivos
O projeto cria e gerencia automaticamente os seguintes arquivos na mesma pasta do script:
1. Gerenciador_tarefas.py > O código-fonte principal contendo toda a lógica do sistema.
2. Tarefas.json > Banco de dados das tarefas ativas (criado automaticamente).
3. Tarefas_arquivadas.json > Histórico de tarefas antigas ou excluídas (criado automaticamente).

Pré-requisitos
Para executar este projeto, precisas apenas ter o Python 3.x instalado na tua máquina.
Verifica a tua versão com o comando: python --version

Como Executar
1. Clone o repositório ou baixe o arquivo gerenciador_tarefas.py.
2. Abra o terminal (CMD, PowerShell ou Terminal do Linux/Mac).
3. Navegue até a pasta onde o arquivo está salvo.
4. Execute o comando: python gerenciador_tarefas.py

Regras de Negócio Implementadas1. 
1. Ciclo de Prioridade
O sistema não permite que o utilizador escolha aleatoriamente qual tarefa fazer em seguida. Ele impõe a disciplina de execução baseada na urgência cadastrada.
2. Regra de Arquivamento (Limpeza)
Ao executar a opção de Processar Arquivamento/Limpeza no menu, o sistema aplica a seguinte lógica:
Tarefas com status "Excluída": São movidas imediatamente para o arquivo morto.
Tarefas com status "Concluída": Só são movidas se a data de conclusão for superior a 7 dias atrás.

Tecnologias Utilizadas
Linguagem: Python 3
Armazenamento: JSON (Biblioteca padrão json)
Manipulação de Datas: Biblioteca padrão datetime
Sistema Operacional: Biblioteca padrão os
