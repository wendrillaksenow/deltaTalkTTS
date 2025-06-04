# complemento DeltaTalk TTS para NVDA#

Autores: Patrick Barboza <patrickbarboza774@gmail.com> e Wendrill Aksenow Brandão <wendrillaksenow@gmail.com>

## Descrição

DeltaTalk é o primeiro sintetizador de voz de alta qualidade, disponível para a língua portuguesa. Ele foi criado pela empresa brasileira MicroPower Software, especificamente para o leitor de tela Virtual Vision, em 1997.

Este complemento é um protótipo ainda em estágio inicial, que implementa a compatibilidade do NVDA com este sintetizador.

## Características

- Suporta configurações de voz, velocidade, tom e volume.

- Suporta a mudança da Percentagem de tom em maiúsculas

- É muito leve e responsivo

- Tem melhor controle de recursos de voz, como velocidade e tom, em comparação com a versão Sapi 4.

- A leitura é mais precisa, sem falhas, lentidão ou interrupções.

## Instalação e uso

Para instalar o complemento, clique duas vezes no arquivo "deltaTalk-0.1.nvda-addon".

Durante a instalação, o complemento tentará copiar os arquivos do DeltaTalk para a pasta do programa NVDA e poderá solicitar acesso de administrador se você estiver usando uma cópia instalada do NVDA.

Se isso não for possível, ou se você optar por não copiar os arquivos durante a instalação, o complemento tentará copiá-los antes de carregar o sintetizador pela primeira vez, e poderá pedir acesso de administrador novamente no caso de uma cópia instalada.

Se a cópia falhar, o sintetizador não funcionará corretamente e tentará copiar os arquivos novamente na próxima vez que for carregado.

Após a instalação, acesse as configurações de voz do NVDA (NVDA + Ctrl + V) pressione o botão "Alterar", e selecione o sintetizador MicroPower DeltaTalk TTS.

Você também pode acessar rapidamente a caixa de diálogo "Selecionar sintetizador" com o atalho NVDA+CTRL+S.

## Problemas conhecidos

- O sintetizador é limitado a 3 instâncias por vez. Se você usar o NVDA com perfis de configuração com vozes diferentes, após a terceira alteração, o sintetizador travará e não será carregado até que o NVDA seja reiniciado.

- Da mesma forma, se você mudar manualmente para outro sintetizador e depois voltar para o DeltaTalk, ele travará após a terceira mudança até que o NVDA seja reiniciado.

- O recurso de reduzir o volume de outros sons enquanto o NVDA está falando (NVDA + CTRL + D) não é suportado atualmente, a menos que esteja definido como "Sempre reduzir".

- O uso de um dispositivo de áudio secundário também não é suportado, exceto se configurado como o dispositivo de áudio padrão.

- Durante a leitura contínua, o cursor do sistema não segue o sintetizador. Em vez disso, vai direto para o final do texto.

- Em alguns casos, o sintetizador pode travar completamente e permanecer sem voz até que o NVDA seja reiniciado.

## Desenvolvimento futuro

Este complemento é um protótipo inicial, mas já está perfeitamente funcional. As versões futuras podem incluir:

- Operação independente, sem necessidade de copiar os arquivos de voz do DeltaTalk para a pasta do programa NVDA

- Interface de configuração dedicada no NVDA, com várias opções para personalizar a leitura do sintetizador

- Instâncias de sintetizador ilimitadas, permitindo que você use diferentes perfis de voz e altere livremente o sintetizador

- Integração da funcionalidade do complemento "Informação Pausada", proporcionando uma leitura mais detalhada e pausada das informações dos controles e estados quando o foco mudar.

## Agradecimentos

Esse projeto foi possível graças ao apoio das ferramentas de inteligência artificial Claude, Grok e ChatGPT, que contribuíram em diferentes fases do desenvolvimento técnico e conceitual do complemento.

Os autores também gostariam de agradecer aos amigos que contribuíram durante a fase de testes fechados com sugestões e relatórios de bugs.

Da mesma forma, os autores agradecem a todos que experimentarem este complemento a partir de agora e pedem que quaisquer bugs sejam relatados usando os dados de contato indicados no início deste documento.

## Histórico de alterações

### Versão 0.2

- Este é o primeiro lançamento público, com algumas correções de bugs importantes.

- As rotinas que copiam os arquivos de dados do DeltaTalk para a pasta do programa NVDA foram corrigidas para que o acesso administrativo seja solicitado apenas quando necessário. Isso elimina a necessidade de executar o NVDA como administrador ao instalar o complemento.

- O arquivo "installTasks.py" agora suporta internacionalização para manter a consistência com o código principal do sintetizador.

- Mais mensagens de log foram adicionadas ao código principal do sintetizador para facilitar a depuração e a identificação de possíveis problemas.

- A documentação do complemento (que antes era apenas um rascunho inicial) foi reescrita e atualizada.

- Os códigos antigos foram removidos do complemento porque não funcionavam e estavam obsoletos.

- Traduções para o português brasileiro e europeu foram adicionadas às mensagens do complemento.

### Versão 0.1

- Primeira versão de teste privada, com diversas correções de bugs que impediam o funcionamento do sintetizador.

- Foi criada uma rotina que copia os arquivos de dados do DeltaTalk para a pasta do programa NVDA durante a instalação do complemento, eliminando a necessidade de manter a versão Sapi 4 instalada.

    - Também foi adicionada uma lógica que verifica a presença desses arquivos na pasta do programa NVDA antes de carregar o sintetizador e os copia novamente caso estejam ausentes.

    - Observe que, para que isso funcione, o NVDA deve ser executado como administrador.

- O suporte inicial à internacionalização foi adicionado ao código principal do sintetizador.