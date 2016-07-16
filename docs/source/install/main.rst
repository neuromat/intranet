Instalando o NIRA Dev
=========================

Instalação do NIRA para um ambiente Linux Debian, utilizando Python 2.7, Virtualenv, Apache2, Git e PostgreSQL.


1. Pacotes necessários
----------------------

Precisamos instalar o git, postgres, virtualenv, apache2::

	apt-get install python-pip apache2 git postgresql-9.4 libpq-dev python-dev libapache2-mod-wsgi
	pip install virtualenv


2. Virtualenv
-------------

Criar um virtualenv 
+++++++++++++++++++	

Para criar um virtualenv em um diretório, por exemplo */var/lib*, faça::

	cd /var/lib
	virtualenv sistema-nira


Baixar o NIRA no virtualenv
+++++++++++++++++++++++++++

Baixe o NIRA Dev do git para dentro do virtualenv com o seguinte comando::
	
	cd /var/lib/sistema-nira
	git clone https://github.com/neuromat/nira.git -b "Dev"


Ativar o virtualenv
+++++++++++++++++++

Ative o virtualenv e siga para realizar os próximos passos::

	cd /var/lib/sistema-nira
	source bin/activate


3. Instalar os pacotes necessários para o funcionamento do NIRA na versão desejada
----------------------------------------------------------------------------------

Instale os pacotes necessários da versão obtida do GitHub::
	
	cd /var/lib/sistema-nira/nira/
	pip install -r requirements.txt


4. Alterar o arquivo wsgi.py
----------------------------

Abra o arquivo de wsgi::
	
	cd /var/lib/sistema-nira/nira/sistema
	vi /var/lib/sistema-nira/nira/sistema/wsgi.py


Deixe similar ao seguinte código, modificando caso seu diretório seja diferente:

.. literalinclude:: ./wsgi.py
    :language: python
    :emphasize-lines: 12-13


5. Configure seu settings_local
-------------------------------

Configure um postgres banco de dados
++++++++++++++++++++++++++++++++++++

Configurar um banco de dados PostgreSQL é simples, são três passos:

1. Usando o usuário postgres::

    su postgres

2. Crie um usuário de banco e defina uma senha::

    createuser seu_usuario --pwprompt --encrypted
	
3. Crie um banco e defina uma senha::

    createdb seu_banco


Settings local 
++++++++++++++

O arquivo *settings_local.py* deve ficar no diretório sistema do projeto do NIRA, no nosso caso::
	
    cd /var/lib/sistema-nira/nira/sistema/
    vi /var/lib/sistema-nira/sistema/settings_local.py


Em *settings_local.py* você deve configurar o sistema para usar o seu banco de dados PostgreSQL.
Você também deve alterar a variável com o nome do seu CEPID.

.. literalinclude:: ./settings_local.py
    :language: python
    :emphasize-lines: 21, 24, 47, 53-55

A linha de *INSTALLED_APPS* que está comentada deve ser descomentada somente se a interface visual desejada seja o Django Suit. Veja mais na página sobre a interface_.

.. _interface:
    ../interface/main.html


6. Configuração do Apache
-------------------------

Crie um diretório para armazenar os logs de erro do sistema::

    mkdir /var/log/apache2/nira


Vá para o diretório de sites do Apache e abra um arquivo para o nira, *nira.conf*::

    cd /etc/apache2/sites-available
    vi nira.conf


Coloque algo similar ao código abaixo, alterando *ServerAdmin, ServerName, ServerAlias* de acordo seu ambiente e altere o diretório caso seja necessário:

.. literalinclude:: ./nira.conf


Desligue o sites do Apache e habilite o NIRA::

    a2dissite 000-default.conf
    a2ensite nira


7. Configurações finais
-----------------------

Arrumando os arquivos de static::

    cd /var/lib/sistema-nira/nira/
    nano sistema/settings.py

Comente a seguinte parte do código::

    # STATICFILES_DIRS = (
    #     os.path.join(BASE_DIR, 'static'),
    # )


Para obter os arquivos de static, faça::

    cd /var/lib/sistema-nira/nira/
    python manage.py collectstatic


Configure o banco de dados com os apps do NIRA::

    python manage.py migrate


Crie um usuário administrador::

    python manage.py createsuperuser


Reinicie o Apache::
		
    service apache2 restart


Se tudo tiver corrido corretamente, o NIRA estará na porta configurada no arquivo do Apache.

Você pode logar no sistema com o Administrador criado no passo 7.