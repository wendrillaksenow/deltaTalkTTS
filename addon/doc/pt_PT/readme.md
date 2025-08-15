# MicroPower DeltaTalk TTS - extra para NVDA

Autores: Patrick Barboza [patrickbarboza774@gmail.com](mailto:patrickbarboza774@gmail.com) e Wendrill Aksenow Brandão [wendrillaksenow@gmail.com](mailto:wendrillaksenow@gmail.com)

Este extra implementa a compatibilidade do NVDA com o sintetizador MicroPower DeltaTalk. Inclui dois módulos integrados, que serão descritos em pormenor mais adiante.

## Sintetizador DeltaTalk

### Descrição

O DeltaTalk é o primeiro sintetizador de fala de alta qualidade, disponível para a língua portuguesa. Foi criado pela empresa brasileira MicroPower Software, especificamente para o leitor de ecrã Virtual Vision, em 1997.

### Características

- Suporta as configurações de voz, velocidade, entoação e volume.
- Suporta a alteração da percentagem da entoação para letras maiúsculas
- É muito leve e responsivo
- Tem um melhor controlo das características de voz, tais como velocidade e entoação, em comparação com a versão Sapi 4.
- A leitura é mais precisa, sem falhas, lentidão ou interrupções.

### Instalação e utilização

O extra pode ser transferido e instalado a partir da loja de extras do NVDA. Basta pesquisar por "MicroPower DeltaTalk TTS.

Após a instalação, aceda às configurações de voz do NVDA (NVDA+Ctrl+V) prima o botão "Alterar", e selecione o sintetizador MicroPower DeltaTalk TTS.

Também pode aceder rapidamente ao diálogo "Selecionar sintetizador" com o atalho NVDA+CTRL+S.

A partir da versão 0.4, já não é necessário copiar os ficheiros de dados do DeltaTalk para a pasta do programa NVDA. Estes serão carregados a partir da pasta do próprio extra.

Embora não o possamos garantir, alguns dos problemas relatados por certos utilizadores são supostamente resolvidos com esta solução. No entanto, alguns problemas mais específicos podem persistir.

Por se tratar de um componente antigo (quase 30 anos de idade), o sintetizador pode ser instável ou apresentar problemas que dificultam ou mesmo impedem o seu funcionamento em computadores mais modernos. Descobrimos recentemente este facto e tudo o que podemos fazer é pedir aos utilizadores que sejam pacientes e evitem utilizá-lo com a velocidade máxima, o que poderá aliviar um pouco estes problemas.

### Dicionários de Pronúncia e de Símbolos

O DeltaTalk integra um dicionário de símbolos próprio, que é ativado de forma automática durante o carregamento do extra.

Devido à arquitetura do leitor de ecrã NVDA, este dicionário de símbolos é partilhado com outros sintetizadores compatíveis, como o Eloquence e o eSpeak.

Caso pretenda utilizar exclusivamente o dicionário de símbolos predefinido fornecido pelo NVDA, poderá desativar o "Dicionário de Símbolos do DeltaTalk". Para tal, aceda às configurações do NVDA e, na categoria "Voz", desmarque o item correspondente da lista de dicionários extra para o processamento de caracteres e símbolos.

Tenha em atenção que esta definição será automaticamente revertida se, ao reiniciar o NVDA, o DeltaTalk estiver definido como o sintetizador padrão (o que fará com que o dicionário seja reativado).

Além disso, o DeltaTalk inclui um dicionário de pronúncia interno, que contém mais de 100.000 regras de pronúncia para palavras da língua portuguesa. Este dicionário está incluído no pacote do extra e é essencial para o funcionamento do sintetizador. Será atualizado regularmente com novas regras de pronúncia à medida que o extra for sendo atualizado.

### Dispositivos áudio secundários e modo de diminuição do volume

A partir da versão 0.3, o extra inclui suporte inicial para o modo de diminuição do volume (Shift+NVDA+D) e dispositivos de áudio secundários.

Tenha em atenção que esta funcionalidade ainda está em fase experimental e pode apresentar problemas, pelo que está desativada por defeito.

Consulte a secção "Histórico de alterações" abaixo para saber como pode ativar esta funcionalidade e obter mais informações.

### Modo Virtual Vision

A funcionalidade do extra "Informação Pausada" está agora integrada ao DeltaTalk como o "Modo Virtual Vision".

Veja mais sobre esta funcionalidade na secção "Modo Virtual Vision" abaixo.

### Opções de configuração

O DeltaTalk inclui agora uma categoria no diálogo de configurações do NVDA, que permite-lhe ajustar algumas opções do funcionamento do extra.

Inicialmente, apenas está disponível uma opção para ativar ou desativar a utilização experimental do modo NVWave para a reprodução de áudio e um botão para ajustar as opções do novo "Modo Virtual Vision". No futuro, serão adicionadas mais opções que lhe permitirão ajustar o modo de leitura e o funcionamento do próprio sintetizador.

### Problemas conhecidos

- O sintetizador está limitado a 3 instâncias de cada vez. Esta limitação é imposta pela DLL do DeltaTalk e não pode ser contornada, ao menos por agora.

    - Se utilizar o NVDA com um perfil de configuração com vozes diferentes, após a terceira alteração, o sintetizador bloqueará e não será carregado até que o NVDA seja reiniciado.

    - Da mesma forma, se mudar manualmente para outro sintetizador e depois voltar para o DeltaTalk, este bloqueará após a terceira mudança até que o NVDA seja reiniciado.

- Durante a leitura contínua, o cursor do sistema não segue o sintetizador. Em vez disso, vai diretamente para o fim do texto.

- Em alguns casos, o sintetizador pode bloquear completamente e permanecer sem voz até que o NVDA seja reiniciado.

### Desenvolvimento futuro

Este extra é um protótipo inicial, mas já está perfeitamente funcional. As versões futuras poderão incluir:

- Instâncias de sintetizador ilimitadas, permitindo-lhe utilizar diferentes perfis de voz e alterar livremente o sintetizador
- Opções de configuração que lhe permitirão controlar o funcionamento interno do sintetizador

### Agradecimentos

Este projeto foi possível graças ao apoio das ferramentas de inteligência artificial Claude, Grok e ChatGPT, que contribuíram em diferentes fases do desenvolvimento técnico e conceptual do extra.

Os autores gostariam também de agradecer aos amigos que contribuíram durante a fase de testes fechados com sugestões e relatórios de erros.

Da mesma forma, os autores agradecem a todos os que experimentarem este extra a partir de agora e pedem que quaisquer erros sejam comunicados através dos dados de contacto indicados no início deste documento.

Por último, mas não menos importante, aqui ficam os nossos mais profundos agradecimentos ao Denis Renato da Costa e à MicroPower Software, que gentilmente nos forneceram o DeltaTalk SDK e as suas APIs de desenvolvimento, sem os quais nada disto seria possível.

### Histórico de alterações

#### Versão 0.4.1

- Esta versão apenas corrige um problema em que o sintetizador não podia ser carregado porque faltava um dos ficheiros principais.

#### Versão 0.4

- A funcionalidade do antigo extra "Informação Pausada" foi integrada ao DeltaTalk como um plugin global denominado "Modo Virtual Vision".

    - A versão atual é idêntica à última versão do extra original, mas será atualizada regularmente.
    - O ficheiro installTasks.py inclui agora uma rotina que verifica a presença do antigo extra e remove-o se estiver instalado.

- Foi criado um novo painel de configurações para o DeltaTalk e adicionado ao diálogo de configurações do NVDA. Este painel será alargado com novas opções de configuração ao longo do tempo.
- O extra funciona agora de forma completamente independente, eliminando a necessidade de copiar os ficheiros de dados do DeltaTalk para a pasta do programa NVDA.

    - As rotinas correspondentes para copiar e remover estes ficheiros foram removidas do código principal do extra e do ficheiro installTasks.py.
    - Isto deve resolver a maior parte dos problemas relatados por alguns utilizadores, mas não podemos garantir que sejam efetivamente resolvidos.

#### Versão 0.3

- Foi implementada uma lógica que verifica o dicionário de pronúncia interno do sintetizador (Brport.lng) e o copia automaticamente para a pasta do programa NVDA se forem detetadas alterações ao ficheiro original incluído no pacote do extra.
- Foi incluído um dicionário de símbolos integrado para o DeltaTalk, permitindo-lhe interpretar os sinais de pontuação à sua maneira.
- O extra agora utiliza "log" (importado do "logHandler") em vez de "logging", para uma melhor integração com o NVDA.
- Foi incluído suporte experimental para reprodução de áudio utilizando o sistema "nvwave", com geração de áudio em blocos múltiplos e reprodução assíncrona.

    - Isto ativa o suporte inicial para dispositivos de áudio secundários e o modo de diminuição do volume (Shift+NVDA+D).
    - Esta funcionalidade ainda está desativada por predefinição e pode ser ativada para testes através da nova opção "Utilizar o NVWave para reprodução de áudio" no diálogo de configurações do NVDA, categoria "DeltaTalk".

- As mensagens de erro do DeltaTalk utilizam agora traduções mais amigáveis, para além dos códigos de erro internos da DLL.
- Foram implementadas rotinas para remover os ficheiros de dados do DeltaTalk da pasta do programa NVDA se o extra for desinstalado. Note que podem ser necessários privilégios de administrador.

#### Versão 0.2

- Esta é a primeira versão pública, com algumas correções de erros importantes.
- As rotinas que copiam os ficheiros de dados do DeltaTalk para a pasta do programa NVDA foram corrigidas de modo a que o acesso administrativo só seja solicitado quando necessário. Isto elimina a necessidade de executar o NVDA como administrador ao instalar o extra.
- O ficheiro "installTasks.py" suporta agora a internacionalização para manter a consistência com o código principal do sintetizador.
- Foram adicionadas mais mensagens de log ao código principal do sintetizador para facilitar a depuração e a identificação de possíveis problemas.
- A documentação para o extra (que anteriormente era apenas um rascunho inicial) foi reescrita e atualizada.
- Os códigos antigos foram retirados do extra porque não funcionavam e eram obsoletos.
- As traduções para português do Brasil e português de Portugal foram adicionadas para as mensagens do extra.

#### Versão 0.1

- Primeira versão de teste privada, com várias correções de erros que impediam o funcionamento do sintetizador.
- Foi criada uma rotina que copia os ficheiros de dados do DeltaTalk para a pasta do programa NVDA durante a instalação do extra, o que elimina a necessidade de manter instalada a versão Sapi 4.

    - Foi também adicionada uma lógica que verifica a presença destes ficheiros na pasta do programa NVDA antes de carregar o sintetizador, e copia-os novamente se estiverem em falta.
    - Note que, para que isto funcione, o NVDA deve ser executado como administrador.

- O suporte inicial para internacionalização foi adicionado ao código principal do sintetizador.

## Modo Virtual Vision

### Descrição

O modo Virtual Vision (originalmente 'Informação Pausada') é uma extensão que insere pausas durante a leitura das informações de controlo, proporcionando uma leitura mais detalhada e pausada das informações dos controlos e estados quando o foco muda entre elementos da interface.

Esta funcionalidade foi inspirada no leitor de ecrã brasileiro "Virtual Vision", conhecido pela sua forma pausada de anunciar a informação, melhorando a compreensão do utilizador.

Este módulo está integrado ao DeltaTalk para garantir uma experiência de leitura completa semelhante à do Virtual Vision.

Se quiser utilizá-lo com outros sintetizadores, pode instalar o antigo extra "Informação Pausada", que é perfeitamente compatível com qualquer sintetizador que esteja a ser utilizado pelo NVDA. Note-se que, por razões de compatibilidade, não é recomendável manter ambos os extras instalados.

Também não deve esquecer que o antigo extra "Informação Pausada" foi descontinuado e não receberá atualizações futuras, pelo que poderá perder a compatibilidade com novas versões do NVDA.

### Nota importante

A leitura pausada baseia-se exclusivamente no nível de pontuação. São adicionados hífenes para pausar a leitura da informação. Se o nível de pontuação estiver definido para algo acima de "alguns", os hífenes serão lidos em voz alta.

Da mesma forma, se os símbolos (especificamente o hífen) não estiverem corretamente ajustados no diálogo de pronúncia da pontuação/símbolo, as pausas podem não ocorrer.

Para garantir que as pausas funcionam como esperado, vá ao diálogo de pronúncia da pontuação/símbolo e certifique-se de que o hífen está definido para ser enviado para o sintetizador quando está abaixo do nível de símbolos.

### Funcionalidades

- Anúncio dos tipos e estados de controlo: A extensão anuncia o tipo de controlo (por exemplo "caixa de verificação", "botão de opção", "menu", "caixa de edição") e o seu estado (por exemplo "marcado", "pressionado", "indisponível", "ocupado").
- O anúncio é feito de forma pausada, à semelhança do que era feito pelo leitor de ecrã Virtual Vision.

### Utilização

Após a instalação do extra MicroPower DeltaTalk para NVDA, o Modo Virtual Vision funciona automaticamente, permitindo uma leitura mais detalhada e pausada das informações sobre os tipos e os estados dos controlos, desde que o sintetizador DeltaTalk esteja ativo.. Não é necessária qualquer configuração adicional.

### Opções de configuração

Como mencionado, não é necessária qualquer configuração adicional quando se utiliza esta extensão. As predefinições e a integração com o sintetizador DeltaTalk proporcionam uma experiência de leitura de ecrã e navegação no Windows muito semelhante à do Virtual Vision.

No entanto, estão disponíveis várias opções de configuração, permitindo-lhe ajustar o funcionamento da extensão ao seu gosto ou às suas necessidades.

Para aceder às configurações do Modo Virtual Vision, abra o diálogo de configurações do NVDA, vá para a categoria "DeltaTalk" e prima o botão "Modo Virtual Vision...". Estão disponíveis as seguintes opções:

- Ativar o modo Virtual Vision: Se desmarcar esta opção, a extensão será completamente desativada e todas as outras opções de configuração ficarão indisponíveis. Também pode ativar/desativar o Modo Virtual Vision utilizando o atalho NVDA+Shift+V. Este atalho pode ser modificado a partir do diálogo "Definir comandos" do NVDA, na categoria "DeltaTalk". Note que o extra irá desativar automaticamente o Modo Virtual vision quando mudar para outro sintetizador e irá ativá-lo novamente quando voltar a utilizar o DeltaTalk.
- Permitir traduções personalizadas para os nomes dos tipos e estados de controlo: Se esta opção estiver marcada, a extensão utilizará um dicionário interno para traduzir os nomes dos tipos e estados dos controlos. Caso contrário, serão utilizadas as traduções internas do NVDA.
- Extensão da mensagem: Este grupo de botões de opção controla a quantidade de informação a ser falada.
    - Curta: Apenas as informações de navegação essenciais do NVDA serão faladas.
    - Média: Para além das informações de navegação essenciais do NVDA, a extensão adicionará mais algumas informações. Por exemplo, quando um objeto tem uma tecla de atalho associada, ouvirá a informação "atalho" antes de a tecla de atalho ser anunciada. Também ouvirá a informação "valor" antes de anunciar o valor dos controlos de deslize e das barras de deslocamento.
    - Longa: A extensão acrescentará outro conjunto de informações para além das anteriores. Ao navegar pelos itens de uma lista, vista em árvore ou menus, ouvirá as informações correspondentes de acordo com o tipo de item. A extensão também o avisará sempre que uma janela for ativada. Esta é a configuração por defeito.
    - Personalizada: Com esta opção, é possível controlar individualmente todas as informações anunciadas pela extensão.

#### Configurações para o nível personalizado

Ao definir o nível de extensão da mensagem como "Personalizado", pode ajustar individualmente todas as informações anunciadas, por exemplo, pode desativar as informações que não quer ou não precisa que sejam anunciadas. Pode fazê-lo através do botão "Configurar". Este botão só está disponível quando o nível de extensão da mensagem personalizada está selecionado. Clicar neste botão abre um diálogo de configuração para o nível personalizado, com as seguintes opções:

- Selecionar os controlos a anunciar: Nesta lista, é possível ativar ou desativar todos os tipos de controlo suportados pelo Modo Virtual Vision. Para os controlos desativados, apenas serão anunciados o nome e o estado (se aplicável).

- Outras mensagens adicionais: Este grupo de controlos contém as seguintes opções:
    - Anunciar janelas ativas: Anuncia sempre que uma janela é ativada.
    - Anunciar "atalho" antes das teclas de atalho dos objetos: Quando um objeto tem uma tecla de atalho associada, anuncia a informação "atalho" antes de a tecla de atalho correspondente ser anunciada.
    - Anunciar "valor" antes dos valores do controlo de deslize e da barra de deslocamento: Quando focar numa barra deslizante ou de deslocamento, anuncia a informação "valor" antes de o valor ser anunciado.

### Problemas conhecidos

- Nas páginas Web, a leitura pausada só funciona quando o modo de foco do NVDA está ativado. Caso contrário, a navegação com as setas faz com que os controlos sejam lidos utilizando os métodos nativos do NVDA.
- Em alguns casos, o anúncio dos estados pode falhar ou ser incorreto.
    - Quando uma caixa de verificação está marcada, desmarcá-la faz com que o estado "marcado" seja anunciado incorretamente.
    - Quando um botão de alternância é premido ou um item de lista é selecionado, a desativação do botão ou a anulação da seleção do item não os anuncia.
    - Esta falha só ocorre na primeira vez que se desmarca uma caixa de verificação, se desativa um botão de alternância ou se anula a seleção de um item de lista com a Barra de Espaço ou Control+Barra de Espaço.
    - Para ter a certeza, pode utilizar o atalho NVDA+Tab para que a informação seja repetida pelo NVDA. Neste caso, o estado será anunciado corretamente.
- Alguns tipos de menus, como os do Thunderbird, têm uma leitura um pouco estranha. As informações "submenu" e "indisponível" são anunciadas várias vezes, mesmo quando não é necessário. Nestes casos, ao navegar pelos menus do Thunderbird e outros menus semelhantes, recomenda-se que o Modo Virtual Vision seja temporariamente desativado (através da tecla de atalho) até que seja encontrada uma solução para este problema.
- Em alguns tipos de caixas de diálogo que não têm um título associado, o seu conteúdo não é lido automaticamente. Nestes casos, pode utilizar o modo de navegação de objetos do NVDA para explorar a caixa de diálogo ou fazer com que o NVDA tente lê-la utilizando o atalho NVDA+Tab.
- O anúncio de janelas ativas, em certos casos, faz com que esta informação seja anunciada incorretamente, por exemplo, ao abrir uma caixa combinada com o atalho Alt+Seta para baixo ou ao abrir um menu de contexto como o do Google Chrome.
- Em determinados momentos, podem aparecer erros ocasionais no log do NVDA, mas estes não interferem com o funcionamento. Estes erros serão corrigidos nas próximas atualizações.

### Histórico de alterações (Informação Pausada)

#### Versão 1.5

- O estado "internal_link" (que identifica os links para a mesma página) foi acrescentado à lista dos estados a anunciar.
- Foram também acrescentados mais alguns controlos à lista de tipos de controlo a anunciar.
- Foi criada uma lógica que verifica a presença da versão antiga do extra e remove-a antes de instalar esta nova versão.
- Foi corrigido um problema em que as configurações para o nível de extensão da mensagem personalizada se perdiam quando o NVDA era reiniciado ou quando o seu idioma era alterado.
- O código do extra foi simplificado e as partes desnecessárias e repetidas foram eliminadas para facilitar a manutenção.
- O extra está agora disponível na loja de extras do NVDA. Basta procurar por "Informação Pausada".
- A funcionalidade do extra foi integrada no DeltaTalk como o "Modo Virtual Vision", pelo que esta será a última versão autónoma.

#### Versão 1.4

- Foi corrigido um erro com o anúncio de janelas ativas que fazia com que, ao focar a barra de tarefas ou alternar entre tarefas com o atalho Alt+Tab, o primeiro item não fosse anunciado. Este problema também afetava alguns itens em janelas normais, que eram ignorados.

#### Versão 1.3

- Primeira versão de lançamento oficial.
- Foi implementado um nível de extensão de mensagem personalizado, que permite controlar individualmente todas as informações anunciadas pelo extra.
- Foi criada uma nova opção de configuração para desativar completamente o extra.
- Foi também adicionada uma tecla de atalho para ativar/desativar, que é especialmente útil para desativar temporariamente o extra em determinados casos.

#### Versão 1.2

- Versão de teste privada, inicialmente lançada como 1.1 e posteriormente atualizada para 1.2.
- Foi criada uma nova opção de configuração que lhe permite escolher se o extra deve ou não traduzir os nomes dos tipos e estados dos controlos.
- Foi implementada uma lógica de níveis de extensão da mensagem - longa, média e curta. No nível longo (predefinição), todas as informações possíveis serão faladas. No nível médio, algumas informações serão suprimidas e no nível curto, apenas as informações essenciais serão faladas.

#### Versão 1.1

- Foram criados novos métodos de leitura dos estados de controlo para corrigir um problema em que certos estados não eram lidos.
- Foi criada uma nova interface para o extra, com o primeiro conceito de opções de configuração.
- Foi corrigido um erro em que a descrição de determinados objetos e o conteúdo de algumas caixas de diálogo não eram lidos.
- Foi corrigido um erro em que o valor das barras de progresso não era lido automaticamente.
- Foi corrigido um erro em que não era possível focar corretamente os links contidos em mensagens de e-mail e páginas Web.
- Foi corrigido um problema com a leitura de células do Excel.
- Foi criada uma lógica para verificar se o estado só de leitura é relevante, a fim de evitar anúncios desnecessários.

#### Versão 1.0

- Versão completamente reescrita a partir do protótipo inicial, com várias correções de erros.
- Foi criado um dicionário completo com os nomes dos tipos e estados de controlo, com as respetivas traduções, que será atualizado sempre que necessário.
- A documentação foi reescrita e atualizada.

#### Versão 0.1

- Protótipo inicial, criado com muito poucos recursos e ainda não muito funcional.
- Criação da documentação inicial.