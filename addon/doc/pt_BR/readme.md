# complemento DeltaTalk TTS para NVDA

Autores: Patrick Barboza [patrickbarboza774@gmail.com](mailto:patrickbarboza774@gmail.com) e Wendrill Aksenow Brandão [wendrillaksenow@gmail.com](mailto:wendrillaksenow@gmail.com)

## Descrição

DeltaTalk é o primeiro sintetizador de voz de alta qualidade, disponível para a língua portuguesa. Ele foi criado pela empresa brasileira MicroPower Software, especificamente para o leitor de tela Virtual Vision, em 1997.

Este complemento é um protótipo ainda em estágio inicial, que implementa a compatibilidade do NVDA com este sintetizador.

## Características

* Suporta configurações de voz, velocidade, tom e volume.
* Suporta a mudança da Percentagem de tom em maiúsculas
* É muito leve e responsivo
* Tem melhor controle de recursos de voz, como velocidade e tom, em comparação com a versão Sapi 4.
* A leitura é mais precisa, sem falhas, lentidão ou interrupções.

## Instalação e uso

O complemento pode ser baixado e instalado a partir da loja de complementos do NVDA. Basta pesquisar por "MicroPower DeltaTalk TTS".

Durante a instalação, o complemento tentará copiar os arquivos do DeltaTalk para a pasta do programa NVDA e poderá solicitar acesso de administrador se você estiver usando uma cópia instalada do NVDA.

Se isso não for possível, ou se você optar por não copiar os arquivos durante a instalação, o complemento tentará copiá-los antes de carregar o sintetizador, e poderá pedir acesso de administrador novamente no caso de uma cópia instalada.

Se a cópia falhar, o sintetizador não funcionará corretamente.

Note que esses arquivos serão automaticamente removidos se o complemento for desinstalado.

Após a instalação, acesse as configurações de voz do NVDA (NVDA+Ctrl+V) pressione o botão "Alterar", e selecione o sintetizador MicroPower DeltaTalk TTS.

Você também pode acessar rapidamente a caixa de diálogo "Selecionar sintetizador" com o atalho NVDA+CTRL+S.

## Dicionários de Pronúncia e Símbolos

O DeltaTalk integra um dicionário de símbolos próprio, que é ativado automaticamente durante o carregamento do complemento.

Devido à arquitetura do leitor de tela NVDA, este dicionário de símbolos é compartilhado com outros sintetizadores compatíveis, como Eloquence e eSpeak.

Se você quiser usar exclusivamente o dicionário de símbolos padrão fornecido pelo NVDA, você pode desativar o "Dicionário de Símbolos do DeltaTalk". Para isso, acesse as configurações do NVDA e, na categoria "Fala", desmarque o item correspondente na lista de Dicionários Extras para o processamento de caracteres e símbolos.

Note que essa configuração será revertida automaticamente se, ao reiniciar o NVDA, o DeltaTalk estiver definido como o sintetizador padrão (o que fará com que o dicionário seja reativado).

Além disso, o DeltaTalk inclui um dicionário de pronúncia interno, que contém mais de 100.000 regras de pronúncia para palavras da língua portuguesa. Este dicionário é essencial para o funcionamento do sintetizador, e é copiado automaticamente para a pasta do NVDA durante o processo de instalação do complemento, sendo atualizado sempre que forem detectadas modificações no arquivo original incluído no pacote.

## Dispositivos de áudio secundários e modo de áudio prioritário

A partir da versão 0.3, o complemento inclui suporte inicial ao modo de áudio prioritário (Shift+NVDA+D) e dispositivos de áudio secundários.

Tenha em mente que esta funcionalidade ainda está em fase experimental e pode apresentar problemas, portanto, está desativada por padrão.

Consulte a seção "Histórico de alterações" abaixo para saber como você pode ativar esse recurso e obter mais informações.

## Problemas conhecidos

* O sintetizador é limitado a 3 instâncias por vez. Esta limitação é imposta pela DLL do DeltaTalk e, por enquanto, não pode ser contornada.

  * Se você usar o NVDA com perfis de configuração com vozes diferentes, após a terceira alteração, o sintetizador bloqueará e não será carregado até que o NVDA seja reiniciado.
  * Da mesma forma, se você mudar manualmente para outro sintetizador e depois voltar para o DeltaTalk, este bloqueará após a terceira mudança até que o NVDA seja reiniciado.

* Durante a leitura contínua, o cursor do sistema não segue o sintetizador. Em vez disso, vai direto para o final do texto.
* Em alguns casos, o sintetizador pode travar completamente e permanecer sem voz até que o NVDA seja reiniciado.

## Desenvolvimento futuro

Este complemento é um protótipo inicial, mas já está perfeitamente funcional. As versões futuras podem incluir:

* Operação independente, sem necessidade de copiar os arquivos de voz do DeltaTalk para a pasta do programa NVDA
* Interface de configuração dedicada no NVDA, com várias opções para personalizar a leitura do sintetizador
* Instâncias de sintetizador ilimitadas, permitindo que você use diferentes perfis de voz e altere livremente o sintetizador
* Integração da funcionalidade do complemento "Informação Pausada", proporcionando uma leitura mais detalhada e pausada das informações dos controles e estados quando o foco mudar.

## Agradecimentos

Esse projeto foi possível graças ao apoio das ferramentas de inteligência artificial Claude, Grok e ChatGPT, que contribuíram em diferentes fases do desenvolvimento técnico e conceitual do complemento.

Os autores também gostariam de agradecer aos amigos que contribuíram durante a fase de testes fechados com sugestões e relatórios de bugs.

Da mesma forma, os autores agradecem a todos que experimentarem este complemento a partir de agora e pedem que quaisquer bugs sejam relatados usando os dados de contato indicados no início deste documento.

## Histórico de alterações

### Versão 0.3

* Foi implementada uma lógica que verifica o dicionário de pronúncia interno do sintetizador (Brport.lng) e o copia automaticamente para a pasta do programa NVDA se forem detectadas alterações no arquivo original incluído no pacote do complemento.
* Um dicionário de símbolos integrado foi incluído para o DeltaTalk, permitindo que ele interprete os sinais de pontuação à sua maneira.
* O complemento agora utiliza "log" (importado de "logHandler") em vez de "logging", para uma melhor integração com o NVDA.
* Foi incluído suporte experimental para reprodução de áudio usando o sistema "nvwave", com geração de áudio em blocos múltiplos e reprodução assíncrona.
* Isso ativa o suporte inicial para dispositivos de áudio secundários e o modo de áudio prioritário (Shift+NVDA+D).
* Este recurso ainda está desativado por padrão e pode ser ativado para testes alterando a linha "self.\_use\_nvwave = False" para "True" no código do complemento.
* Rotinas foram implementadas para remover os arquivos de dados do DeltaTalk da pasta do programa NVDA se o complemento for desinstalado. Note que privilégios de administrador podem ser necessários.

### Versão 0.2

* Este é o primeiro lançamento público, com algumas correções de bugs importantes.
* As rotinas que copiam os arquivos de dados do DeltaTalk para a pasta do programa NVDA foram corrigidas para que o acesso administrativo seja solicitado apenas quando necessário. Isso elimina a necessidade de executar o NVDA como administrador ao instalar o complemento.
* O arquivo "installTasks.py" agora suporta internacionalização para manter a consistência com o código principal do sintetizador.
* Mais mensagens de log foram adicionadas ao código principal do sintetizador para facilitar a depuração e a identificação de possíveis problemas.
* A documentação do complemento (que antes era apenas um rascunho inicial) foi reescrita e atualizada.
* Os códigos antigos foram removidos do complemento porque não funcionavam e estavam obsoletos.
* Traduções para o português brasileiro e europeu foram adicionadas às mensagens do complemento.

### Versão 0.1

* Primeira versão de teste privada, com diversas correções de bugs que impediam o funcionamento do sintetizador.
* Foi criada uma rotina que copia os arquivos de dados do DeltaTalk para a pasta do programa NVDA durante a instalação do complemento, eliminando a necessidade de manter a versão Sapi 4 instalada.

  * Também foi adicionada uma lógica que verifica a presença desses arquivos na pasta do programa NVDA antes de carregar o sintetizador e os copia novamente caso estejam ausentes.
  * Observe que, para que isso funcione, o NVDA deve ser executado como administrador.

* O suporte inicial à internacionalização foi adicionado ao código principal do sintetizador.
