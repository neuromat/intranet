=========
Interface
=========

*****************************
Utilizando o tema Django Suit
*****************************

O NIRA tem suporte ao tema Django Suit, um tema moderno para a interface do Django.

O `Django Suit <http://djangosuit.com/>`_ deve ser utilizado para fins não comerciais.


1. Instale o Django Suit
-------------------------

Instale a última versão estável do Django Suit::
    
    pip install django-suit


2. Alterar alguns arquivos
--------------------------

Inclua *suit* em INSTALLED_APPS, dentro de sistema/settings.py:

.. literalinclude:: ./settings_suit.py
    :language: python

Inclua o código abaixo em sistema/settings_local.py:

.. literalinclude:: ./interface.py
    :language: python

:Recomendação:
    Para os próximos passos, faça um backup do arquivo caso deseje voltar para a interface original no futuro.

Delete o arquivo index.html em templates/admin/index.html

Substitua o código encontrado em templates/documents/documents.html pelo seguinte:

.. literalinclude:: ./documents_suit.html
    :language: html

Substitua o código encontrado em templates/report/reports.html pelo seguinte:

.. literalinclude:: ./reports_suit.html
    :language: html

Substitua o código encontrado em templates/add_content/add_content.html pelo seguinte:

.. literalinclude:: ./add_content_suit.html
    :language: html

3. Atualizar os arquivos static
-------------------------------

No diretório raiz do NIRA, atualize os arquivos static::

    cd /var/lib/sistema-nira/nira/
    python manage.py collectstatic

Responda 'yes' para atualizar para o novo tema.

Atualize o Apache::

    service apache2 restart

Agora você deve ver o NIRA com o tema atualizado.


Referências
+++++++++++
`Django Suit Docs <http://django-suit.readthedocs.io/en/develop/>`_