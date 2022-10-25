# -*- coding: cp1252 -*-
"""M�dulo para automa��o de aplica��es desktop. Vers�o 3.1"""
# importa recursos do m�dulo pywinauto em n�vel global
from pywinauto import Application


def _aplicacao(estilo_aplicacao='win32'):
    """Inicia e retorna um objeto do tipo Application da biblioteca pywinauto."""
    # define app como global
    global APP

    # instancia o objeto application
    APP = Application(backend=estilo_aplicacao)

    # retorna o objeto application instanciado
    return APP


def iniciar_app(
    executavel,
    estilo_aplicacao='win32',
    esperar=(),
    inverter: bool = False,
    ocioso: bool = False,
):
    """Inicia e retorna um processo do sistema de um
    objeto do tipo Application com o caminho recebido."""
    # define app como global
    global APP

    # instancia o objeto application
    APP = _aplicacao(estilo_aplicacao=estilo_aplicacao)

    # inicia o processo de execu��o do aplicativo passado como par�metro
    APP.start(cmd_line=executavel, wait_for_idle=ocioso,)

    # verifica se foi passado algum par�metro para esperar, caso n�o:
    if esperar == ():
        # aguarda a inicializa��o da aplica��o ficar pronta em at� 10 segundos
        APP.window().wait('ready', 10)
    else:
        if inverter == False:
            # aguarda a inicializa��o da aplica��o ficar na condi��o informada
            APP.window().wait(*esperar)
        else:
            # aguarda a inicializa��o da aplica��o n�o ficar na condi��o informada
            APP.window().wait_not(*esperar)

    # coleta o PID da aplica��o instanciada
    processo_app: int = APP.process

    # retorna o PID coletado
    return processo_app


def conectar_app(PID, tempo_espera=60):
    """Inicia e retorna um processo do sistema de um
    objeto do tipo Application com o caminho recebido."""
    # define app como global
    global APP

    # instancia o objeto application
    APP = _aplicacao()

    # inicia o processo de execu��o do aplicativo passado como par�metro
    app_conectado: Application = APP.connect(process=PID, timeout=tempo_espera)

    # coleta o PID da aplica��o instanciada
    processo_app: int = app_conectado.process

    # retorna o PID coletado
    return processo_app


def encerrar_app(pid: int, forcar: bool = False):
    """Encerra e retorna um processo do sistema de um
    objeto do tipo Application com o caminho recebido."""
    # importa app para o escopo da fun��o
    global APP

    # define PID interno como o informado no par�metro ou nulo
    pid = pid or None

    # caso o PID seja nulo
    if pid == None:
        # retorna False
        return False
    # caso o PID tenha algum valor
    else:
        # conecta a aplica��o correspondente ao PID informado
        app_interno: Application = APP.connect(process=pid, timeout=60)

    # encerra o aplicativo em execu��o
    app_interno.kill(soft=not forcar)

    # retorna o objeto application com o processo encerrado
    return True


def retornar_janelas_disponiveis(pid: int):
    """Retorna as janelas dispon�veis em um
    objeto do tipo Application j� em execu��o."""
    # importa app para o escopo da fun��o
    global APP

    # define PID interno como o informado no par�metro ou nulo
    pid = pid or None

    # caso o PID seja nulo
    if pid == None:
        # retorna False
        return False
    # caso o PID tenha algum valor
    else:
        # conecta a aplica��o correspondente ao PID informado
        app_interno: Application = APP.connect(process=pid, timeout=60)

    # coleta as janelas dispon�veis
    lista_janelas = app_interno.windows()

    # instancia uma lista vazia
    lista_janelas_str = []
    # para cada janela na lista de janelas
    for janela in lista_janelas:
        # coleta e salva o nome da janela
        lista_janelas_str.append(janela.texts()[0])

    # retorna uma lista das janelas coletadas
    return lista_janelas_str


def localizar_elemento(caminho_campo, estatico: bool = True):
    tipo_retorno = type(bool())

    elemento = _localizar_elemento(
        caminho_campo=caminho_campo,
        estatico=estatico,
        tipo_retorno=tipo_retorno
    )

    return elemento


def _localizar_elemento(
        caminho_campo,
        estatico: bool = True,
        tipo_retorno: type = type(Application())
    ):
    """Localiza e retorna um objeto do tipo Application
    percorrendo o caminho at� o �ltimo o elemento."""
    # importa app para o escopo da fun��o
    global APP

    # inicializa APP para uma vari�vel interna
    app_interno = APP

    # trata o caminho da �rvore de parantesco do app
    campo = caminho_campo.split('->')
    index = 0

    # localiza o elemento at� o final da �rvore de parantesco do app:
    while index < len(campo):

        # Se index for igual ao primeiro elemento
        if index == 0:
            # coleta um objeto application
            #   colocando o t�tulo como nome informado
            app_interno = app_interno.window(title=campo[0])

        # Se index for igual ao �ltimo elemento
        elif (index == (len(campo) - 1)) and (estatico is False):

            # coleta o elemento informado e concatena 'Edit' no final
            app_interno = app_interno[campo[index] + 'Edit']

        # Se o index n�o for igual ao primeiro elemento
        #   nem o index for igual ao �ltimo elemento
        else:
            # coleta o elemento informado e concatena 'Edit' no final
            app_interno = app_interno[campo[index]]

        # l�gica para a condicional
        index = index + 1

    # retorna o elemento encontrado
    if type(tipo_retorno) == type(bool()):
        return True
    else:
        return app_interno


def digitar(
    caminho_campo,
    valor,
    com_espaco=True,
    digitacao_visivel=True,
    com_nova_linha=False,
):
    """Digita em um elemento dentro de um objeto do tipo Application."""
    # Define libera��o para digitar
    estatico = False

    # localiza o elemento at� o final da �rvore de parantesco do app
    app_interno = _localizar_elemento(caminho_campo, estatico)

    # digita o valor no campo localizado
    app_interno.type_keys(
        valor, with_spaces=com_espaco,
        set_foreground=digitacao_visivel,
        with_newlines=com_nova_linha,
    )

    # trata o valor capturado conforme o tipo do valor de entrada
    valor_retornado = type(valor)(capturar_texto(caminho_campo, estatico))

    # retorna o valor capturado e tratado
    return valor_retornado


def coletar_arvore_elementos(nome_janela,) -> list:
    """Lista um elemento dentro de um objeto do
    tipo Application e retorna o valor coletado."""
    # importa recursos do m�dulo io
    import io

    # importa recursos do m�dulo Path
    from contextlib import redirect_stdout

    # Define libera��o para digitar
    estatico = False

    # localiza o elemento at� o final da �rvore de parantesco do app
    app_interno = _localizar_elemento(nome_janela, estatico)

    conteudoStdOut = io.StringIO()
    with redirect_stdout(conteudoStdOut):
        app_interno.print_control_identifiers()

    valor = conteudoStdOut.getvalue()
    valor_dividido = valor.split('\n')
    
    # retorna o valor capturado e tratado
    return valor_dividido


def localizar_diretorio_em_treeview(
    caminho_janela,
    caminho_diretorio,
    estatico: bool = True,
):
    """Localiza um diret�rio, seguindo a �rvore de diret�rios informada,\
    dentro de um objeto TreeView do tipo Application."""
    try:
        # localiza e armazena o elemento conforme informado
        app_interno = _localizar_elemento(caminho_janela, estatico=estatico)

        # seleciona o caminho informado na janela do tipo TreeView
        app_interno.TreeView.get_item(caminho_diretorio).click()

        # clica em Ok para confirmar
        app_interno.OK.click()

        # retorna verdadeiro caso processo seja feito com sucesso
        return True
    except:
        return False


def capturar_texto(caminho_campo, estatico: bool = True) -> str:
    """Captura o texto de um elemento
    dentro de um objeto do tipo Application."""
    # localiza o elemento at� o final da �rvore de parantesco do app
    app_interno = _localizar_elemento(caminho_campo, estatico)

    # captura o texto do campo localizado
    valor_capturado = app_interno.texts()[0]

    # retorna o valor capturado
    return valor_capturado


def clicar(caminho_campo):
    """Clica em um elemento dentro de um objeto do tipo Application."""
    # localiza o elemento at� o final da �rvore de parantesco do app
    app_interno = _localizar_elemento(caminho_campo)

    # digita o valor no campo localizado
    app_interno.click()

    # retorna o valor capturado e tratado
    return True


def simular_clique(
    botao: str,
    eixo_x: int,
    eixo_y: int,
    tipo_clique: str = 'unico'
    ):
    """Simula clique do mouse, performando o mouse real."""
    try:
        # importa recursos do m�dulo mouse
        from pywinauto.mouse import click, double_click

        if ( not botao.upper() in ['ESQUERDO', 'DIREITO']):
            raise ValueError('Informe um bot�o v�lido: esquerdo, direito.')
        
        if ( not tipo_clique.upper() in ['UNICO', 'DUPLO']):
            raise ValueError(
                'Tipo de clique inv�lido, escolha entre �nico e duplo.'
            )

        if not type(eixo_x) == type(int()) \
        or not type(eixo_y) == type(int()):
            raise ValueError('Coordenadas precisam ser do tipo inteiro.')

        if botao.upper() == 'ESQUERDO':
            botao = 'left'
        else:
            botao = 'right'

        if tipo_clique.upper() == 'UNICO':
            click(button=botao, coords=(eixo_x, eixo_y))
        elif tipo_clique.upper() == 'DUPLO':
            double_click(button=botao, coords=(eixo_x, eixo_y))

        return True
    except Exception as erro:
        return erro


def simular_digitacao(
    texto: str,
    com_espaco: bool = True,
    com_tab: bool = False,
    com_linha_nova: bool = False,
    ):
    """Simula digita��o do teclado, performando o teclado real."""
    try:
        # importa recursos do m�dulo keyboard
        from pywinauto.keyboard import send_keys

        if not type(com_espaco) == type(bool()) \
        or not type(com_tab) == type(bool()) \
        or not type(com_linha_nova) == type(bool()):
            raise ValueError(
                '''Informe os par�metros com_espaco,
                 com_tab e com_linha_nova com valor boleano'''
            )

        if not type(texto) == type(str()):
            raise ValueError('Informe um texto do tipo string.')

        send_keys(
            keys=texto,
            with_spaces=com_espaco,
            with_tabs=com_tab,
            with_newlines=com_linha_nova
        )
        
        return True
    except Exception as erro:
        return erro


def mover_mouse(eixo_x: int, eixo_y: int):
    try:
        # importa recursos do m�dulo mouse
        from pywinauto.mouse import move

        if not type(eixo_x) == type(int()) \
        or not type(eixo_y) == type(int()):
            raise ValueError('Coordenadas precisam ser do tipo inteiro.')

        move(coords=(eixo_x, eixo_y))

        return True
    except Exception as erro:
        return erro


def coletar_situacao_janela(nome_janela) -> str:
    """Coleta a situa��o do estado atual de uma
    janela de um objeto do tipo Application."""
    # importa app para o escopo da fun��o
    global APP

    # inicializa APP para uma vari�vel interna
    app_interno = APP

    # coleta a situacao atual da janela
    situacao = app_interno.window(title=nome_janela).get_show_state()

    # 1 - Normal
    if situacao == 1:
        situacao = 'normal'
    # 2 - Minimizado
    elif situacao == 2:
        situacao = 'minimizado'
    # 3 - Maximizado
    elif situacao == 3:
        situacao = 'maximizado'
    # Caso n�o encontre as situa��es normal, ninimizado e maximizado
    else:
        # define um valor padr�o
        situacao = 'n�o identificado'

    # retorna a situa��o da janela
    return situacao


def esta_visivel(nome_janela) -> str:
    """Verifica se a janela de um objeto do tipo Application est� vis�vel."""
    # coleta a situa��o atual da janela
    situacao = coletar_situacao_janela(nome_janela)

    # define vis�vel para situa��o 'maximizado' ou 'normal'
    if situacao == 'maximizado' or situacao == 'normal':
        situacao = 'visivel'
    # define n�o vis�vel para situa��o 'minimizado'
    elif situacao == 'minimizado':
        situacao = 'n�o vis�vel'
    # Caso n�o encontre as situa��es normal, ninimizado e maximizado
    else:
        # define um valor padr�o
        situacao = 'n�o identificado'

    # retorna a situa��o da janela
    return situacao


def janela_existente(pid, nome_janela) -> bool:
    """Verifica se a janela de um objeto do tipo Application est� vis�vel."""
    # coleta a situa��o atual da janela
    lista_janelas = retornar_janelas_disponiveis(pid)

    # verifica se o nome da janela informada corresponde � alguma janela na lista
    for janela in lista_janelas:
        # caso o nome da janela seja o mesmo da janela atual da lista
        if janela == nome_janela:
            # retorna True
            return True

    # retorna False caso nenhuma janela tenha correspondido
    return False


def esta_com_foco(nome_janela) -> bool:
    """Verifica se a janela de um objeto do tipo Application est� com foco."""
    # importa app para o escopo da fun��o
    global APP

    # inicializa APP para uma vari�vel interna
    app_interno = APP

    # coleta a situacao atual de foco da janela
    foco : bool = app_interno.window(title=nome_janela).has_focus()

    # retorna a situa��o coletada
    return foco


def minimizar_janela(nome_janela) -> bool:
    """Miniminiza a janela de um objeto do tipo Application."""
    # importa app para o escopo da fun��o
    global APP

    try:
        # inicializa APP para uma vari�vel interna
        app_interno = APP

        # miniminiza a janela informada
        app_interno.window(title=nome_janela).minimize()

        # retorna verdadeiro confirmando a execu��o da a��o
        return True
    except:
        return False


def maximizar_janela(nome_janela) -> bool:
    """Maximiza a janela de um objeto do tipo Application."""
    # importa app para o escopo da fun��o
    global APP

    try:
        # inicializa APP para uma vari�vel interna
        app_interno = APP

        # maximiza a janela informada
        app_interno.window(title=nome_janela).maximize()

        # retorna verdadeiro confirmando a execu��o da a��o
        return True
    except:
        return False


def restaurar_janela(nome_janela) -> bool:
    """Miniminiza a janela de um objeto do tipo Application."""
    # importa app para o escopo da fun��o
    global APP

    try:
        # inicializa APP para uma vari�vel interna
        app_interno = APP

        # restaura a janela informada
        app_interno.window(title=nome_janela).restore()

        # retorna verdadeiro confirmando a execu��o da a��o
        return True
    except:
        return True


def coletar_dados_selecao(caminho_campo) -> str:
    """Coleta dados dispon�veis para sele��o em um
    elemento de sele��o em um objeto do tipo Application."""
    # define est�tico como falso para trabalhar com elemento din�mico
    estatico = False

    # localiza o elemento at� o final da �rvore de parantesco do app
    app_interno = _localizar_elemento(caminho_campo, estatico)

    # captura o texto do campo localizado
    valor_capturado = app_interno.item_texts()

    # retorna o valor capturado
    return valor_capturado


def coletar_dado_selecionado(caminho_campo) -> str:
    """Coleta dado j� selecionado em um elemento
    de sele��o em um objeto do tipo Application."""
    # define est�tico como falso para trabalhar com elemento din�mico
    estatico = False

    # localiza o elemento at� o final da �rvore de parantesco do app
    app_interno = _localizar_elemento(caminho_campo, estatico)

    # captura o texto do campo localizado
    valor_capturado = app_interno.selected_text()

    # retorna o valor capturado
    return valor_capturado


def selecionar_em_campo_selecao(caminho_campo, item) -> str:
    """Seleciona um dado em um elemento de
    sele��o em um objeto do tipo Application."""
    # define est�tico como falso para trabalhar com elemento din�mico
    estatico = False

    # localiza o elemento at� o final da �rvore de parantesco do app
    app_interno = _localizar_elemento(caminho_campo, estatico)

    # seleciona o item informado
    app_interno.select(item)

    # captura o texto do campo localizado
    valor_capturado = coletar_dado_selecionado(caminho_campo)

    # retorna o valor capturado
    return valor_capturado


def selecionar_em_campo_lista(caminho_campo, item) -> str:
    """Seleciona um dado em um elemento de
    lista em um objeto do tipo Application."""
    # define est�tico como falso para trabalhar com elemento din�mico
    estatico = False

    # localiza o elemento at� o final da �rvore de parantesco do app
    app_interno = _localizar_elemento(caminho_campo, estatico)

    # seleciona o item informado
    app_interno.select(item)

    # captura o �ndice do �tem selecionado
    indice_selecionado = app_interno.selected_indices()

    # retorna o valor capturado
    return indice_selecionado


def selecionar_menu(nome_janela, caminho_menu):
    """Seleciona um item de menu conforme o caminho
    informado em um objeto do tipo Application."""
    # importa app para o escopo da fun��o
    global APP

    try:
        # inicializa APP para uma vari�vel interna
        app_interno = APP

        # percorre e clica no menu informado
        app_interno.window(title=nome_janela).menu_select(caminho_menu)

        # retorna verdadeiro confirmando a execu��o da a��o
        return True
    except:
        return False


def fechar_janela(nome_janela):
    """Encerra uma janela de um objeto do tipo
    Application com o caminho recebido."""
    # importa app para o escopo da fun��o
    global APP

    # inicializa APP para uma vari�vel interna
    app_interno = APP

    # fecha a janela informada
    app_interno.window(title=nome_janela).close()

    # retorna verdadeiro confirmando a execu��o da a��o
    return True
