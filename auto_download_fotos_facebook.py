import lib.automacao_web_utils as webutils
import lib.python_utils as pyutils
import os


try:
    os.environ['WDM_SSL_VERIFY'] = '0'
    cls = pyutils.cls

    conta_email = os.getenv('usuario_facebook')
    conta_senha = os.getenv('senha_facebook')
    nome_perfil_facebook = os.getenv('nome_perfil_facebook')
    nome_usuario_facebook = os.getenv('nome_usuario_facebook')
    validacao_navegador = False

    if None in [conta_email, conta_senha, nome_usuario_facebook]:
        raise SystemError('Verifique as variáveis de ambiente e tente novamente.')

    if pyutils.pasta_existente('./albuns_salvos') is False:
        pyutils.criar_pasta('./albuns_salvos')

    validacao_navegador = webutils.iniciar_navegador(
        nome_navegador='edge',
        url='https://www.facebook.com/',
        options=(
            'debug-level=3',
            'disable-gpu',
            'log-level=3',
            '--start-maximized',
        ),
    )

    webutils.aguardar_elemento(
        identificador="//input[@name='email']",
        tipo_elemento='xpath',
    )
    webutils.escrever_em_elemento(
        seletor="//input[@name='email']",
        texto=conta_email,
        tipo_elemento='xpath',
    )

    webutils.aguardar_elemento(
        identificador="//input[@name='pass']",
        tipo_elemento='xpath',
    )
    webutils.escrever_em_elemento(
        seletor="//input[@name='pass']",
        texto=conta_senha,
        tipo_elemento='xpath',
    )

    webutils.aguardar_elemento(
        identificador="//button[@name='login']",
        tipo_elemento='xpath',
    )
    webutils.clicar_elemento(
        seletor="//button[@name='login']",
        tipo_elemento='xpath',
    )

    elemento_notificacao = "//div[@aria-label='Solicitação de notificações push']/parent::span/parent::div"
    webutils.aguardar_elemento(
        identificador=elemento_notificacao,
        tipo_elemento='xpath',
    )
    webutils.clicar_elemento(
        seletor=elemento_notificacao,
        tipo_elemento='xpath',
    )

    modal_usuario = (
        "//div[@aria-label='Configurações e controles da conta']/span"
    )
    webutils.aguardar_elemento(
        identificador=modal_usuario,
        tipo_elemento='xpath',
    )
    webutils.clicar_elemento(
        seletor=modal_usuario,
        tipo_elemento='xpath',
    )

    webutils.aguardar_elemento(
        identificador=modal_usuario,
        tipo_elemento='xpath',
    )
    webutils.clicar_elemento(
        seletor=modal_usuario,
        tipo_elemento='xpath',
    )
    webutils.clicar_elemento(
        seletor=modal_usuario,
        tipo_elemento='xpath',
    )

    perfil_usuario = f"//div[@aria-label='Seu perfil']/following::span[text()='{nome_usuario_facebook.title()}']"
    webutils.aguardar_elemento(
        identificador=perfil_usuario,
        tipo_elemento='xpath',
    )
    webutils.clicar_elemento(
        seletor=perfil_usuario,
        tipo_elemento='xpath',
    )

    link_fotos = "//span[text()='Fotos']"
    webutils.aguardar_elemento(
        identificador=link_fotos,
        tipo_elemento='xpath',
    )
    webutils.clicar_elemento(
        seletor=link_fotos,
        tipo_elemento='xpath',
    )

    link_album_fotos = (
        f"//a[@href='https://www.facebook.com/{nome_perfil_facebook}/photos_albums']"
    )
    webutils.aguardar_elemento(
        identificador=link_album_fotos,
        tipo_elemento='xpath',
    )
    webutils.clicar_elemento(
        seletor=link_album_fotos,
        tipo_elemento='xpath',
    )

    imagem_capa_perfil = "//img[@data-imgperflogname='profileCoverPhoto']"
    webutils.centralizar_elemento(
        seletor=imagem_capa_perfil,
        tipo_elemento='xpath',
    )

    capa_perfil = f"//a[@href='https://www.facebook.com/{nome_perfil_facebook}/photos_albums']/parent::*/parent::*/parent::*/parent::*/parent::*/parent::*/div[3]"
    webutils.aguardar_elemento(
        identificador=capa_perfil,
        tipo_elemento='xpath',
    )
    webutils.centralizar_elemento(
        seletor=imagem_capa_perfil,
        tipo_elemento='xpath',
    )

    elemento_criar_album = "//span[text()='Criar álbum']"
    webutils.aguardar_elemento(
        identificador=elemento_criar_album,
        tipo_elemento='xpath',
    )
    webutils.centralizar_elemento(
        seletor=imagem_capa_perfil,
        tipo_elemento='xpath',
    )

    lista_albuns = webutils.extrair_texto(
        seletor=capa_perfil,
        tipo_elemento='xpath',
    )

    lista_albuns = lista_albuns.splitlines()
    lista_albuns_tratada = []
    for album in lista_albuns:
        if not album.upper().__contains__(
            'ITENS'
        ) and not album.upper().__contains__('ITEM'):
            lista_albuns_tratada.append(album)

    for indice in range(1, len(lista_albuns_tratada)):
        if (
            (
                not lista_albuns_tratada[indice]
                .upper()
                .__contains__('CRIAR ÁLBUM')
            )
            and (
                not lista_albuns_tratada[indice]
                .upper()
                .__contains__('TWIBBON APP PHOTOS')
            )
            and (
                not lista_albuns_tratada[indice]
                .upper()
                .__contains__('FOTOS EM DESTAQUE')
            )
        ):
            nome_album = lista_albuns_tratada[indice]
            print(
                f'\n\n\n------------ ÁLBUM DE NÚMERO: {indice} E NOME: {nome_album} ------------\n\n\n'
            )

            elemento_album_atual = f"//span[text()='{nome_album}']/parent::*/parent::*/parent::*/parent::*/parent::*/parent::*/parent::*/parent::*"
            webutils.aguardar_elemento(
                identificador=elemento_album_atual,
                tipo_elemento='xpath',
            )

            webutils.clicar_elemento(
                seletor=elemento_album_atual,
                tipo_elemento='xpath',
            )

            final_pagina = False
            quantidade_fotos = 1
            quantidade_anterior = 0
            contagem = 0
            numero_publicacoes = f"//span[text()='{nome_album}']/parent::*/parent::*/div[3]/span"
            webutils.aguardar_elemento(
                identificador=numero_publicacoes,
                tipo_elemento='xpath',
            )
            quantidade_fotos = webutils.extrair_texto(
                seletor=numero_publicacoes,
                tipo_elemento='xpath',
            )
            if quantidade_fotos.upper().__contains__('PUBLICAÇÃO'):
                quantidade_fotos = quantidade_fotos.partition(' · ')
                quantidade_fotos = int(quantidade_fotos[2].partition(' ')[0])
            else:
                quantidade_fotos = int(quantidade_fotos.partition(' ')[0])

            lista_fotos_album_atual = []
            lista_fotos_baixadas = []
            for numero_foto in range(1, quantidade_fotos + 1):
                foto_atual = f"//span[text()='Compartilhar']/parent::*/parent::*/parent::*/parent::*/parent::*/parent::*/parent::*/parent::*/parent::*/parent::*/parent::*/parent::*/parent::*/parent::*/parent::*/div[2]/div/div/div[{numero_foto}]/a"
                validacao_foto = webutils.aguardar_elemento(
                    identificador=foto_atual,
                    tipo_elemento='xpath',
                    tempo=5,
                )

                if validacao_foto is True:
                    texto_extraido = ''
                    texto_extraido = webutils.extrair_texto(seletor=foto_atual, tipo_elemento='xpath')
                    if not texto_extraido == '':
                        continue

                    webutils.clicar_elemento(
                        seletor=foto_atual,
                        tipo_elemento='xpath',
                    )

                    acoes_foto = "//div[@aria-label='Ações para esta publicação']"
                    webutils.aguardar_elemento(
                        identificador=acoes_foto,
                        tipo_elemento='xpath'
                    )
                    webutils.clicar_elemento(
                        seletor=acoes_foto,
                        tipo_elemento='xpath'
                    )

                    opcao_baixar_foto = "//span[text()='Baixar']/parent::*/parent::*/parent::*/parent::*"
                    webutils.aguardar_elemento(
                        identificador=opcao_baixar_foto,
                        tipo_elemento='xpath'
                    )
                    webutils.clicar_elemento(
                        seletor=opcao_baixar_foto,
                        tipo_elemento='xpath'
                    )

                    botao_x_fechar = "(//div[@aria-label='Fechar'])[1]"
                    webutils.aguardar_elemento(
                        identificador=botao_x_fechar,
                        tipo_elemento='xpath'
                    )
                    webutils.clicar_elemento(
                        seletor=botao_x_fechar,
                        tipo_elemento='xpath'
                    )

            nome_album = nome_album.replace('...', '')
            pasta_album_foto = f'./albuns_salvos/{nome_album}'
            if pyutils.pasta_existente(pasta_album_foto) is False:
                pyutils.criar_pasta(pasta_album_foto)
                while pyutils.pasta_existente(pasta_album_foto) is False:
                    ...

            lista_fotos_baixadas = pyutils.retornar_arquivos_em_pasta(
                caminho=r'C:\Users\techa\Downloads', filtro='*.jpg'
            )
            for indice_foto in range(len(lista_fotos_baixadas)):
                foto_atual = lista_fotos_baixadas[indice_foto]
                foto_transferida = f'./albuns_salvos/{nome_album}/foto_{indice_foto+1}.jpg'
                if pyutils.arquivo_existente(
                    caminho=foto_transferida,
                ):
                    pyutils.excluir_arquivo(
                        caminho=foto_transferida,
                    )

                    while pyutils.arquivo_existente(
                        caminho=foto_transferida,
                    ) is True:
                        ...

                pyutils.recortar(
                    caminho_atual=foto_atual,
                    caminho_novo=foto_transferida,
                )
                while pyutils.arquivo_existente(
                    caminho=foto_atual,
                ) is True:
                    ...

            webutils.voltar_pagina()
except Exception as erro:
    print(erro)
    breakpoint()
finally:
    if validacao_navegador is True:
        webutils.encerrar_navegador()
        ...
