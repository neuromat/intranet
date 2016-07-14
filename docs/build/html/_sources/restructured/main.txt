Exemplos de reStructuredText
=============================

Você pode checar o código para fazer os exemplos abaixo em *exibir fonte*.

Inserir código e detalhar:
----------------------------------------

.. Coloque as linhas do código e quais deseja dar um foco
.. literalinclude:: ./hello.py
    :language: python
    :lines: 1-4
    :emphasize-lines: 2 


Outro exemplo de código:
-------------------------

Esse é um parágrafo. O próximo parágrafo será mostrado como código, use para bash scripts e etc::

   Ele vai aparecer como se fosse um código,
   mas não é processado.

   Pode ser usado por várias linhas....

Aqui o texto fica normal de novo.

    
Exemplo de include
------------------

.. Incluir desse ou outro diretório é simples
.. include:: table.rst

A tabela verdade acima foi inserida com um include.


Listas
------

* Uma lista

  * com uma lista encaixada
  * outros temas e tal

* Continuação da lista 


Links
-----

Pode ser feito assim: `Google <http://google.com/>`_ 

Ou separado, assim: `Quase um Google`_.

.. _Quase um Google: http://bing.com/


Imagens
-------

Inserindo uma imagem

.. image:: homepage_nira.png
   :name: Home do NIRA


Outra forma, usando refs:

.. _homepage nira:

.. image:: homepage_nira.png



Referências
-----------

http://www.sphinx-doc.org/en/stable/rest.html

http://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html

http://docutils.sourceforge.net/docs/ref/rst/directives.html

http://gisellezeno.com/tutorials/sphinx-for-python-documentation.html

http://www.sphinx-doc.org/en/stable/markup/code.html

