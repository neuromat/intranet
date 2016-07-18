Utilizando o tema Django Suit
=============================

O NIRA tem suporte ao tema Django Suit, um tema moderno para a interface do Django.

O `Django Suit <http://djangosuit.com/>`_ deve ser utilizado para fins não comerciais.


1. Instale o Django Suit
-------------------------

Instale a última versão estável do Django Suit::
    
    pip install django-suit


2. Colocar nos apps instalados
------------------------------

Incluia *suit* em INSTALLED_APPS, dentro de settings.py:

.. literalinclude:: ./settings_suit.py
    :language: python

Inclua o código abaixo em settings_local.py:

.. literalinclude:: ./interface.py
    :language: python


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