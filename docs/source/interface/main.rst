=========
Interface
=========

*****************************
Utilizando o tema Django Suit
*****************************

O NIRA tem suporte ao tema Django Suit, um tema moderno para a interface do Django.

O `Django Suit <http://djangosuit.com/>`_ está licenciado sob os termos da
`Creative Commons Attribution-NonCommercial 3.0 <https://creativecommons.org/licenses/by-nc/3.0/br/>`_, o que significa
que seu uso é gratuito apenas para fins não comerciais.


1. Instale o Django Suit
-------------------------

Instale a última versão estável do Django Suit::
    
    pip install django-suit


2. Alterar alguns arquivos
--------------------------

Inclua *suit* em INSTALLED_APPS, dentro de sistema/settings.py:

.. literalinclude:: ./settings_suit.py
    :language: python
    :emphasize-lines: 11

Inclua o código abaixo em sistema/settings_local.py:

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