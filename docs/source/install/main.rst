Instalando a última versão estável do NIRA
=========================

Instalação do NIRA para um ambiente Linux Debian (Jessie), utilizando Python 2.7, Virtualenv, Apache2, Git e PostgreSQL.


1. Pacotes necessários
----------------------

Precisamos instalar o git, postgres, apache2 e outras dependências::

	apt-get install python-pip apache2 git postgresql-9.4 libpq-dev python-dev libapache2-mod-wsgi


Baixe o virtualenv::

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
	git clone https://github.com/neuromat/nira.git


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


5. Configure um banco de dados
------------------------------

Configurar um banco de dados PostgreSQL é simples, são três passos:

1. Usando o usuário postgres::

    su postgres

2. Crie um usuário de banco e defina uma senha::

    createuser seu_usuario --pwprompt --encrypted
	
3. Crie um banco::

    createdb seu_banco --owner=seu_usuario


6. Configure seu settings_local
-------------------------------

O arquivo *settings_local.py* deve ficar no diretório sistema do projeto do NIRA, no nosso caso::
	
    cd /var/lib/sistema-nira/nira/sistema/
    vi /var/lib/sistema-nira/sistema/settings_local.py


Em *settings_local.py* você deve configurar o sistema para usar o seu banco de dados PostgreSQL.
Você também deve alterar a variável com o nome do seu CEPID.

.. literalinclude:: ./settings_local.py
    :language: python
    :emphasize-lines: 21, 23, 29-32

Veja mais na página sobre a interface_.

.. _interface:
    ../interface/main.html


7. Configuração do Apache
-------------------------

Crie um diretório para armazenar os logs de erro do sistema::

    mkdir /var/log/apache2/nira


Vá para o diretório de sites do Apache e abra um arquivo para o nira, *nira.conf*::

    cd /etc/apache2/sites-available
    vi nira.conf


Coloque algo similar ao código abaixo, alterando *ServerAdmin, ServerName, ServerAlias* de acordo seu ambiente e altere o diretório caso seja necessário:

.. literalinclude:: ./nira.conf


Desabilite o virtualhost padrão do Apache e habilite o NIRA::

    a2dissite 000-default.conf
    a2ensite nira


8. Configurações finais
-----------------------

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

Você pode logar no sistema com o Administrador criado no passo 8.