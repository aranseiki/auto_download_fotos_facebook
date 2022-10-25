# auto_download_fotos_facebook

#### Este projeto tem como finalidade o download de todas as fotos do Facebook via automação.
#### Para isso, foi usado como dependência o Selenium e Python.

#### As bibliotecas dentro da pasta 'lib/' são autoria própria.

#### Para executar o projeto é necessário ter instalado as dependências acima, além das descritas no arquivo requirements.txt para as bibliotecas funcionarem corretamente.

#### Um script PowerShell foi criado para automatizar esse processo quanto às dependências de bibliotecas do Python. Basta executar o arquivo PrepararAmbiente.ps1 para preparar o ambiente antes de executar o projeto, ou então o arquivo Executar.ps1 para preparar o ambiente e em seguida executar a automação em uma mesma execução.
#### Caso seja necessário alguma configuração do Python ou Pip tem algums parâmetros de configuração no arquivo ConfigPowerShell.ini, onde é possível determinar a versão do Python, proxy para o pip, o arquivo requirements.txt e muito mais.

#### Também é necessário configurar variáveis de ambiente com alguns dados para a automação seguir funcionando bem e protegendo seus dados são elas:
  * usuario_facebook
  * senha_facebook
  * nome_perfil_facebook
  * nome_usuario_facebook

#### onde usuario_facebook é o nome de login, senha_facebook é sua senha de login, nome_perfil_facebook é o nome simples ou apelido e nome_usuario_facebook é o nome completo como consta configurado no Facebook.

A estimativa de volumetria é a realização do download de aproximadamente 650 fotos em 15 minutos.
