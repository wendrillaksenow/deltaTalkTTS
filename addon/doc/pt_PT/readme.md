# Extra DeltaTalk TTS para NVDA#

Autores: Patrick Barboza <patrickbarboza774@gmail.com> e Wendrill Aksenow Brandão <wendrillaksenow@gmail.com>

## Descrição

O DeltaTalk é o primeiro sintetizador de fala de alta qualidade, disponível para a língua portuguesa. Foi criado pela empresa brasileira MicroPower Software, especificamente para o leitor de ecrã Virtual Vision, em 1997.

Este extra é um protótipo ainda em fase inicial, que implementa a compatibilidade do NVDA com este sintetizador.

## Características

- Suporta as configurações de voz, velocidade, entoação e volume.

- Suporta a alteração da percentagem da entoação para letras maiúsculas

- É muito leve e responsivo

- Tem um melhor controlo das características de voz, tais como velocidade e entoação, em comparação com a versão Sapi 4.

- A leitura é mais precisa, sem falhas, lentidão ou interrupções.

## Instalação e utilização

Para instalar o extra, faça duplo clique no ficheiro "deltaTalk-0.1.nvda-addon".

Durante a instalação, o extra tentará copiar os ficheiros do DeltaTalk para a pasta do programa NVDA e poderá pedir acesso de administrador se estiver a utilizar uma cópia instalada do NVDA.

Se isto não for possível, ou se optar por não copiar os ficheiros durante a instalação, o extra tentará copiá-los antes de carregar o sintetizador pela primeira vez, e poderá pedir novamente acesso de administrador no caso de uma cópia instalada.

Se a cópia falhar, o sintetizador não funcionará corretamente e tentará copiar novamente os ficheiros na próxima vez que for carregado.

Após a instalação, aceda às configurações de voz do NVDA (NVDA + Ctrl + V) prima o botão "Alterar", e selecione o sintetizador MicroPower DeltaTalk TTS.

Também pode aceder rapidamente ao diálogo "Selecionar sintetizador" com o atalho NVDA+CTRL+S.

## Problemas conhecidos

- O sintetizador está limitado a 3 instâncias de cada vez. Se utilizar o NVDA com um perfil de configuração com vozes diferentes, após a terceira alteração, o sintetizador bloqueará e não será carregado até que o NVDA seja reiniciado.

- Da mesma forma, se mudar manualmente para outro sintetizador e depois voltar para o DeltaTalk, este bloqueará após a terceira mudança até que o NVDA seja reiniciado.

- A funcionalidade de diminuir o volume de outros sons enquanto o NVDA está a falar (NVDA+CTRL+D) não é atualmente suportada, a menos que esteja definida para "Diminuir sempre".

- A utilização de um dispositivo áudio secundário também não é suportada, exceto se estiver configurado como dispositivo áudio predefinido.

- Durante a leitura contínua, o cursor do sistema não segue o sintetizador. Em vez disso, vai diretamente para o fim do texto.

- Em alguns casos, o sintetizador pode bloquear completamente e permanecer sem voz até que o NVDA seja reiniciado.

## Desenvolvimento futuro

Este extra é um protótipo inicial, mas já está perfeitamente funcional. As versões futuras poderão incluir:

- Funcionamento independente, sem necessidade de copiar os ficheiros de voz DeltaTalk para a pasta do programa NVDA

- Interface de configuração dedicada no NVDA, com várias opções para personalizar a leitura do sintetizador

- Instâncias de sintetizador ilimitadas, permitindo-lhe utilizar diferentes perfis de voz e alterar livremente o sintetizador

- Integração da funcionalidade do extra "Informação Pausada", proporcionando uma leitura mais detalhada e pausada das informações dos controlos e estados quando o foco mudar.

## Agradecimentos

Este projeto foi possível graças ao apoio das ferramentas de inteligência artificial Claude, Grok e ChatGPT, que contribuíram em diferentes fases do desenvolvimento técnico e conceptual do extra.

Os autores gostariam também de agradecer aos amigos que contribuíram durante a fase de testes fechados com sugestões e relatórios de erros.

Da mesma forma, os autores agradecem a todos os que experimentarem este extra a partir de agora e pedem que quaisquer erros sejam comunicados através dos dados de contacto indicados no início deste documento.

## Histórico de alterações

### Versão 0.2

- Esta é a primeira versão pública, com algumas correções de erros importantes.

- As rotinas que copiam os ficheiros de dados do DeltaTalk para a pasta do programa NVDA foram corrigidas de modo a que o acesso administrativo só seja solicitado quando necessário. Isto elimina a necessidade de executar o NVDA como administrador ao instalar o extra.

- O ficheiro "installTasks.py" suporta agora a internacionalização para manter a consistência com o código principal do sintetizador.

- Foram adicionadas mais mensagens de log ao código principal do sintetizador para facilitar a depuração e a identificação de possíveis problemas.

- A documentação para o extra (que anteriormente era apenas um rascunho inicial) foi reescrita e atualizada.

- Os códigos antigos foram retirados do extra porque não funcionavam e eram obsoletos.

- As traduções para português do Brasil e português de Portugal foram adicionadas para as mensagens do extra.

### Versão 0.1

- Primeira versão de teste privada, com várias correções de erros que impediam o funcionamento do sintetizador.

- Foi criada uma rotina que copia os ficheiros de dados do DeltaTalk para a pasta do programa NVDA durante a instalação do extra, o que elimina a necessidade de manter instalada a versão Sapi 4.

    - Foi também adicionada uma lógica que verifica a presença destes ficheiros na pasta do programa NVDA antes de carregar o sintetizador, e copia-os novamente se estiverem em falta.

    - Note que, para que isto funcione, o NVDA deve ser executado como administrador.

- O suporte inicial para internacionalização foi adicionado ao código principal do sintetizador.