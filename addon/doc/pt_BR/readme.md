# MicroPower DeltaTalk TTS - complemento para NVDA

Autores: Patrick Barboza [patrickbarboza774@gmail.com](mailto:patrickbarboza774@gmail.com) e Wendrill Aksenow Brandão [wendrillaksenow@gmail.com](mailto:wendrillaksenow@gmail.com)

Este complemento implementa a compatibilidade do NVDA com o sintetizador MicroPower DeltaTalk. Ele inclui dois módulos integrados, que serão descritos em detalhes abaixo.

## Sintetizador DeltaTalk

### Descrição

DeltaTalk é o primeiro sintetizador de voz de alta qualidade, disponível para a língua portuguesa. Ele foi criado pela empresa brasileira MicroPower Software, especificamente para o leitor de tela Virtual Vision, em 1997.

### Características

- Suporta configurações de voz, velocidade, tom e volume.
- Suporta a mudança da Percentagem de tom em maiúsculas
- É muito leve e responsivo
- Tem melhor controle de recursos de voz, como velocidade e tom, em comparação com a versão Sapi 4.
- A leitura é mais precisa, sem falhas, lentidão ou interrupções.

### Instalação e uso

O complemento pode ser baixado e instalado a partir da loja de complementos do NVDA. Basta pesquisar por "MicroPower DeltaTalk TTS".

Após a instalação, acesse as configurações de voz do NVDA (NVDA+Ctrl+V) pressione o botão "Alterar", e selecione o sintetizador MicroPower DeltaTalk TTS.

Você também pode acessar rapidamente a caixa de diálogo "Selecionar sintetizador" com o atalho NVDA+CTRL+S.

A partir da versão 0.4, não é mais necessário copiar os arquivos de dados do DeltaTalk para a pasta do programa NVDA. Eles serão carregados da pasta do próprio complemento.

Embora não possamos garantir, alguns dos problemas relatados por certos usuários supostamente foram resolvidos com esta solução. No entanto, alguns problemas mais específicos podem persistir.

Por ser um componente antigo (com quase 30 anos de idade), o sintetizador pode ser instável ou ter problemas que dificultam ou até impossibilitam seu funcionamento em computadores mais modernos. Descobrimos isso recentemente e tudo o que podemos fazer é pedir aos usuários que tenham paciência e evitem usá-lo com a velocidade máxima, o que pode aliviar esses problemas um pouco.

### Dicionários de Pronúncia e Símbolos

O DeltaTalk integra um dicionário de símbolos próprio, que é ativado automaticamente durante o carregamento do complemento.

Devido à arquitetura do leitor de tela NVDA, este dicionário de símbolos é compartilhado com outros sintetizadores compatíveis, como Eloquence e eSpeak.

Se você quiser usar exclusivamente o dicionário de símbolos padrão fornecido pelo NVDA, você pode desativar o "Dicionário de Símbolos do DeltaTalk". Para isso, acesse as configurações do NVDA e, na categoria "Fala", desmarque o item correspondente na lista de Dicionários Extras para o processamento de caracteres e símbolos.

Note que essa configuração será revertida automaticamente se, ao reiniciar o NVDA, o DeltaTalk estiver definido como o sintetizador padrão (o que fará com que o dicionário seja reativado).

Além disso, o DeltaTalk inclui um dicionário de pronúncia interno, que contém mais de 100.000 regras de pronúncia para palavras da língua portuguesa. Este dicionário está incluído no pacote do complemento e é essencial para o funcionamento do sintetizador. Ele será atualizado regularmente com novas regras de pronúncia à medida que o complemento for atualizado.

### Dispositivos de áudio secundários e modo de áudio prioritário

A partir da versão 0.3, o complemento inclui suporte inicial ao modo de áudio prioritário (Shift+NVDA+D) e dispositivos de áudio secundários.

Tenha em mente que esta funcionalidade ainda está em fase experimental e pode apresentar problemas, portanto, está desativada por padrão.

Consulte a seção "Histórico de alterações" abaixo para saber como você pode ativar esse recurso e obter mais informações.

### Modo Virtual Vision

A funcionalidade do complemento "Informação Pausada" agora está integrada ao DeltaTalk como o "Modo Virtual Vision".

Veja mais sobre esse recurso na seção "Modo Virtual Vision" abaixo.

### Opções de configuração

O DeltaTalk agora inclui uma categoria no diálogo de configurações do NVDA que permite ajustar algumas das opções de operação do complemento.

Inicialmente, apenas uma opção para ativar ou desativar o uso experimental do modo NVWave para reprodução de áudio e um botão para ajustar as opções do novo "Modo Virtual Vision" estão disponíveis. No futuro, serão adicionadas mais algumas opções que permitirão ajustar o modo de leitura e o funcionamento do próprio sintetizador.

### Problemas conhecidos

- O sintetizador é limitado a 3 instâncias por vez. Esta limitação é imposta pela DLL do DeltaTalk e, por enquanto, não pode ser contornada.

    - Se você usar o NVDA com perfis de configuração com vozes diferentes, após a terceira alteração, o sintetizador bloqueará e não será carregado até que o NVDA seja reiniciado.
    - Da mesma forma, se você mudar manualmente para outro sintetizador e depois voltar para o DeltaTalk, este bloqueará após a terceira mudança até que o NVDA seja reiniciado.

- Durante a leitura contínua, o cursor do sistema não segue o sintetizador. Em vez disso, vai direto para o final do texto.
- Em alguns casos, o sintetizador pode travar completamente e permanecer sem voz até que o NVDA seja reiniciado.

### Desenvolvimento futuro

Este complemento é um protótipo inicial, mas já está perfeitamente funcional. As versões futuras podem incluir:

- Instâncias de sintetizador ilimitadas, permitindo que você use diferentes perfis de voz e altere livremente o sintetizador
- Opções de configuração que permitirão controlar o funcionamento interno do sintetizador.

### Agradecimentos

Esse projeto foi possível graças ao apoio das ferramentas de inteligência artificial Claude, Grok e ChatGPT, que contribuíram em diferentes fases do desenvolvimento técnico e conceitual do complemento.

Os autores também gostariam de agradecer aos amigos que contribuíram durante a fase de testes fechados com sugestões e relatórios de bugs.

Da mesma forma, os autores agradecem a todos que experimentarem este complemento a partir de agora e pedem que quaisquer bugs sejam relatados usando os dados de contato indicados no início deste documento.

Por último, mas não menos importante, agradecemos profundamente ao Denis Renato da Costa e à MicroPower Software, que gentilmente nos forneceram o DeltaTalk SDK e suas APIs de desenvolvimento, sem os quais nada disso seria possível.

### Histórico de alterações

#### Versão 0.4

- A funcionalidade do antigo complemento "Informação Pausada" foi integrada ao DeltaTalk como um plugin global chamado "Modo Virtual Vision".

    - A versão atual é idêntica à última versão do complemento original, mas será atualizada regularmente.
    - O arquivo installTasks.py agora inclui uma rotina que verifica a presença do antigo complemento e o remove se estiver instalado.

- Um novo painel de configurações foi criado para o DeltaTalk e adicionado ao diálogo de configurações do NVDA. Este painel será expandido com novas opções de configuração ao longo do tempo.
- O complemento agora funciona de forma completamente independente, eliminando a necessidade de copiar os arquivos de dados do DeltaTalk para a pasta do programa NVDA.

    - As rotinas correspondentes para copiar e remover esses arquivos foram removidas do código principal do complemento e do arquivo installTasks.py.
    - Isso deve resolver a maioria dos problemas relatados por alguns usuários, mas não podemos garantir que eles serão realmente solucionados.

#### Versão 0.3

- Foi implementada uma lógica que verifica o dicionário de pronúncia interno do sintetizador (Brport.lng) e o copia automaticamente para a pasta do programa NVDA se forem detectadas alterações no arquivo original incluído no pacote do complemento.
- Um dicionário de símbolos integrado foi incluído para o DeltaTalk, permitindo que ele interprete os sinais de pontuação à sua maneira.
- O complemento agora utiliza "log" (importado de "logHandler") em vez de "logging", para uma melhor integração com o NVDA.
- Foi incluído suporte experimental para reprodução de áudio usando o sistema "nvwave", com geração de áudio em blocos múltiplos e reprodução assíncrona.
    - Isso ativa o suporte inicial para dispositivos de áudio secundários e o modo de áudio prioritário (Shift+NVDA+D).
    - Este recurso ainda está desativado por padrão e pode ser ativado para teste através da nova opção "Usar NVWave para reprodução de áudio" no diálogo de configurações do NVDA, na categoria "DeltaTalk".
- As mensagens de erro do DeltaTalk agora usam traduções mais amigáveis, além dos códigos de erro internos da DLL.
- Rotinas foram implementadas para remover os arquivos de dados do DeltaTalk da pasta do programa NVDA se o complemento for desinstalado. Note que privilégios de administrador podem ser necessários.

#### Versão 0.2

- Este é o primeiro lançamento público, com algumas correções de bugs importantes.
- As rotinas que copiam os arquivos de dados do DeltaTalk para a pasta do programa NVDA foram corrigidas para que o acesso administrativo seja solicitado apenas quando necessário. Isso elimina a necessidade de executar o NVDA como administrador ao instalar o complemento.
- O arquivo "installTasks.py" agora suporta internacionalização para manter a consistência com o código principal do sintetizador.
- Mais mensagens de log foram adicionadas ao código principal do sintetizador para facilitar a depuração e a identificação de possíveis problemas.
- A documentação do complemento (que antes era apenas um rascunho inicial) foi reescrita e atualizada.
- Os códigos antigos foram removidos do complemento porque não funcionavam e estavam obsoletos.
- Traduções para o português brasileiro e europeu foram adicionadas às mensagens do complemento.

#### Versão 0.1

- Primeira versão de teste privada, com diversas correções de bugs que impediam o funcionamento do sintetizador.
- Foi criada uma rotina que copia os arquivos de dados do DeltaTalk para a pasta do programa NVDA durante a instalação do complemento, eliminando a necessidade de manter a versão Sapi 4 instalada.

    - Também foi adicionada uma lógica que verifica a presença desses arquivos na pasta do programa NVDA antes de carregar o sintetizador e os copia novamente caso estejam ausentes.
    - Observe que, para que isso funcione, o NVDA deve ser executado como administrador.

- O suporte inicial à internacionalização foi adicionado ao código principal do sintetizador.

## Modo Virtual Vision

### Descrição

O modo Virtual Vision (originalmente 'Informação Pausada') é uma extensão que insere pausas ao ler informações de controle, proporcionando uma leitura mais detalhada e pausada das informações dos controles e estados quando o foco muda entre os elementos da interface.

Essa funcionalidade foi inspirada no leitor de tela brasileiro "Virtual Vision", conhecido por sua forma lenta de anunciar informações, melhorando a compreensão do usuário.

Este módulo está integrado com o DeltaTalk para garantir uma experiência de leitura completa, semelhante à do Virtual Vision.

Se você deseja usá-lo com outros sintetizadores, pode instalar o antigo complemento "Informação Pausada", que é perfeitamente compatível com qualquer sintetizador utilizado pelo NVDA. Note que, por razões de compatibilidade, não é recomendado ter ambos os complementos instalados.

Você também deve lembrar que o antigo complemento "Informação Pausada" foi descontinuado e não receberá futuras atualizações, portanto, pode perder a compatibilidade com novas versões do NVDA.

### Nota importante

A leitura pausada é baseada apenas no nível de pontuação. Hífens são adicionados para pausar a leitura das informações. Se o nível de pontuação for definido acima de "alguns", os hífens serão lidos em voz alta.

Da mesma forma, se os símbolos (especificamente o hífen) não forem ajustados corretamente na caixa de diálogo de pronúncia de pontuação/símbolos, as pausas poderão não ocorrer.

Para garantir que as pausas funcionem conforme o esperado, vá para a caixa de diálogo de pronúncia de pontuação/símbolos e certifique-se de que o hífen esteja configurado para ser enviado ao sintetizador quando estiver abaixo do nível do símbolo.

### Características

- Anúncio de tipos e estados de controle: O complemento anuncia o tipo de controle (por exemplo, "caixa de seleção", "botão de opção", "menu", "caixa de edição") e o seu estado (por exemplo, "marcado", "pressionado" , "indisponível", "ocupado").
- O anúncio é feito de forma pausada, semelhante ao que era feito pelo leitor de tela Virtual Vision.

### Uso

Após a instalação do complemento MicroPower DeltaTalk para NVDA, o Modo Virtual Vision funciona automaticamente, permitindo uma leitura mais detalhada e pausada das informações sobre os tipos e estados dos controles, desde que o sintetizador DeltaTalk esteja ativo. Nenhuma configuração adicional é necessária.

### Opções de configuração

Como mencionado, nenhuma configuração adicional é necessária ao usar esta extensão. As configurações padrão e a integração com o sintetizador DeltaTalk oferecem uma experiência de leitura de tela e navegação no Windows muito semelhante à do Virtual Vision.

No entanto, várias opções de configuração estão disponíveis, permitindo que você ajuste o funcionamento da extensão de acordo com sua preferência ou necessidade.

Para acessar as configurações do Modo Virtual Vision, abra o diálogo de configurações do NVDA, vá para a categoria "DeltaTalk" e pressione o botão "Modo Virtual Vision...". As seguintes opções estão disponíveis:

- Ativar o modo Virtual Vision: Se você desmarcar esta opção, a extensão será completamente desativada e todas as outras opções de configuração ficarão indisponíveis. Você também pode ativar/desativar o Modo Virtual Vision usando o atalho NVDA+Shift+V. Esse atalho pode ser modificado a partir do diálogo "Definir Comandos" do NVDA, na categoria "DeltaTalk". Observe que o complemento irá desativar automaticamente o Modo Virtual Vision quando você mudar para outro sintetizador e o ativará novamente ao retornar ao DeltaTalk.
- Permitir traduções personalizadas para os nomes dos tipos de controle e estados: Se esta opção estiver marcada, a extensão usará um dicionário interno para traduzir os nomes dos tipos e estados dos controles. Caso contrário, as traduções internas do NVDA serão utilizadas.
- Extensão de mensagens: Este grupo de botões de opção controla a quantidade de informações a serem faladas.
    - Curtas: Somente informações essenciais de navegação do NVDA serão faladas.
    - Médias: Além das informações essenciais de navegação do NVDA, a extensão adicionará mais algumas informações. Por exemplo, quando um objeto possui uma tecla de atalho associada, você ouvirá "atalho" antes que a tecla de atalho seja anunciada. Você também ouvirá a informação "valor" antes de anunciar o valor dos controles deslizantes e das barras de rolagem.
    - Longas: a extensão adicionará outro conjunto de informações além dos anteriores. Ao navegar pelos itens de uma lista, itens da árvore ou itens de menu, você ouvirá as informações correspondentes de acordo com o tipo de item. A extensão também irá notificá-lo sempre que uma janela for ativada. Esta é a configuração padrão.
    - Personalizadas: Com esta opção você pode controlar individualmente todas as informações anunciadas pela extensão.

#### Configurações para o nível personalizado

Ao definir o nível de extensão de mensagens como "Personalizado", você pode ajustar individualmente todas as informações anunciadas. Por exemplo, você pode desativar as informações que não deseja ou não precisa que sejam anunciadas. Você pode fazer isso através do botão "Configurar". Este botão só está disponível quando o nível de extensão de mensagens personalizado é selecionado. Clicar neste botão abre um diálogo de configuração para o nível personalizado, com as seguintes opções:

- Selecione os controles a serem anunciados: Nesta lista é possível ativar ou desativar todos os tipos de controles suportados pelo Modo Virtual Vision. Para controles desativados, apenas o nome e o estado (se aplicável) serão anunciados.

- Outras mensagens adicionais: Este grupo de controles contém as seguintes opções:
    - Anunciar janelas ativas: Anuncia sempre que uma janela é ativada.
    - Anunciar "atalho" antes das teclas de atalho dos objetos: Quando um objeto possui uma tecla de atalho associada, anuncia a informação "atalho" antes que a tecla de atalho correspondente seja anunciada.
    - Anunciar "valor" antes dos valores do controle deslizante e da barra de rolagem: ao focar em um controle deslizante ou barra de rolagem, anuncia a informação "valor" antes que o valor seja anunciado.

### Problemas conhecidos

- Em páginas da web, a leitura pausada só funciona quando o modo de foco do NVDA está ativado. Caso contrário, navegar com as setas faz com que os controles sejam lidos usando os métodos nativos do NVDA.
- Em alguns casos, o anúncio do estado pode falhar ou estar incorreto.
    - Quando uma caixa de seleção está marcada, desmarcá-la faz com que o estado "marcado" seja anunciado incorretamente.
    - Quando um botão de alternância é pressionado ou um item da lista é selecionado, desativar o botão ou desmarcar o item não os anuncia.
    - Essa falha ocorre apenas na primeira vez que uma caixa de seleção é desmarcada, um botão de alternância  é desativado ou um item da lista  é desmarcado com a Barra de espaço ou Control+Barra de espaço.
    - Para ter certeza, você pode usar o atalho NVDA+Tab para que a informação seja repetida pelo NVDA. Neste caso, o estado será anunciado corretamente.
- Alguns tipos de menus, como os do Thunderbird, são lidos de maneira um pouco estranha. As informações "submenu" e "indisponível" são anunciadas várias vezes, mesmo quando não é necessário. Nestes casos, ao navegar pelos menus do Thunderbird e outros menus similares, é recomendado que o Modo Virtual Vision seja temporariamente desativado (através da tecla de atalho) até que uma solução para esse problema seja encontrada.
- Em alguns tipos de caixas de diálogo que não têm um título associado, seu conteúdo não é lido automaticamente. Nesses casos, você pode usar o modo de navegação de objetos do NVDA para explorar a caixa de diálogo ou fazer com que o NVDA tente lê-la usando a tecla de atalho NVDA+Tab.
- O anúncio de janelas ativas faz com que essa informação seja anunciada incorretamente em certos casos, por exemplo, ao abrir uma caixa de combinação com o atalho Alt+Seta para baixo ou ao abrir um menu de contexto como o do Google Chrome.
- Em certos momentos, erros ocasionais podem aparecer no log do NVDA, mas eles não interferem na operação. Esses erros serão corrigidos nas próximas atualizações.

### Histórico de alterações (Informação Pausada)

#### Versão 1.5

- O estado "internal_link" (que identifica links para a mesma página) foi adicionado à lista de estados a serem anunciados.
- Mais alguns controles também foram adicionados à lista de tipos de controle a serem anunciados.
- Uma lógica foi criada para verificar a presença da versão antiga do complemento e removê-la antes de instalar esta nova versão.
- Corrigido um problema em que as Configurações para o nível de extensão de mensagem personalizada eram perdidas quando o NVDA era reiniciado ou quando seu idioma era alterado.
- O código do complemento foi simplificado e partes desnecessárias e repetidas foram removidas para facilitar a manutenção.
- O complemento agora está disponível na loja de complementos do NVDA. Basta procurar por "Informação Pausada".
- A funcionalidade do complemento foi integrada ao DeltaTalk como o "Modo Virtual Vision", portanto, esta será a última versão autônoma.

#### Versão 1.4

- Corrigido um erro com o anúncio de janelas ativas em que ao focar na barra de tarefas ou alternar entre tarefas com o atalho Alt+Tab, o primeiro item não era anunciado. Esse problema também afetava alguns itens das janelas normais, que eram ignorados.

#### Versão 1.3

- Primeira versão oficial de lançamento.
- Foi implementado um nível de extensão de mensagem personalizado, que permite controlar individualmente todas as informações anunciadas pelo complemento.
- Uma nova opção de configuração foi criada para desabilitar completamente o complemento.
- Uma tecla de atalho para ativar/desativar também foi implementada, o que é especialmente útil para desativar temporariamente o complemento em certos casos.

#### Versão 1.2

- Versão de teste privada, lançada inicialmente como 1.1 e posteriormente atualizada para 1.2.
- Foi criada uma nova opção de configuração que permite escolher se o complemento deve ou não traduzir os nomes dos tipos e estados de controle.
- Foi implementada uma lógica de níveis de extensão de mensagens - longas, médias e curtas. No nível longo (padrão), todas as informações possíveis serão faladas. No nível médio, algumas informações serão suprimidas e no nível curto, apenas as informações essenciais serão faladas.

#### Versão 1.1

- Novos métodos de leitura de estados de controle foram criados para corrigir um problema em que determinados estados não eram lidos.
- Foi criada uma nova interface para o complemento, com o primeiro conceito de opções de configuração.
- Corrigido um problema em que a descrição de determinados objetos e o conteúdo de algumas caixas de diálogo não eram lidos.
- Corrigido um problema em que o valor da barra de progresso não era lido automaticamente.
- Foi corrigido um erro onde não era possível focar corretamente nos links contidos em mensagens de e-mail e páginas da web.
- Corrigido um problema com a leitura de células do Excel.
- Foi criada uma lógica para verificar se o estado somente leitura é relevante para evitar anúncios desnecessários.

#### Versão 1.0

- Versão completamente reescrita do protótipo inicial, com diversas correções de bugs.
- Foi criado um dicionário completo com os nomes dos tipos e estados de controle, com suas respectivas traduções, que será atualizado conforme necessário.
- A documentação foi reescrita e atualizada.

#### Versão 0.1

- Protótipo inicial, criado com poucos recursos e ainda pouco funcional.
- Criação de documentação inicial.