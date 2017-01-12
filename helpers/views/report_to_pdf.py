# Funcao que recebe o conteudo que seria o output importante de um report
# e mostra isso como pdf


# Fazer apenas uma capsula pra gerar um html e jogar isso e depois exportar em pdf
# cada report vai precisar ter um novo template pra gerar pdfs, algo como: nome_do_arquivo_report_pdf.html

from helpers.views.pdf import render as render_to_pdf


def report(template_src, context_dict):
    render_to_pdf(template_src=template_src, context_dict=context_dict)
