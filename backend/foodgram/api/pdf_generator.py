from django.http.response import HttpResponse
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Frame


def generate_pdf(obj):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="shopping-list.pdf"')
    canvas = Canvas(response)
    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'data/DejaVuSerif.ttf'))

    style = ParagraphStyle('russian_text')
    style.fontName = 'DejaVuSerif'
    style.leading = 0.5 * cm

    story = ['Список ингредиентов:\n\n']
    story.extend(f'{index + 1}. {item["ingredient__name"]} '
                 f'({item["ingredient__measurement_unit"]}) - '
                 f'{item["amount__sum"]}\n'
                 for index, item in enumerate(obj))
    for i, part in enumerate(story):
        story[i] = Paragraph(part.replace('\n', '<br></br>'), style)

    frame = Frame(0, 0, 21 * cm, 29.7 * cm, leftPadding=cm, bottomPadding=cm,
                  rightPadding=cm, topPadding=cm, )
    frame.addFromList(story, canvas)
    canvas.showPage()
    canvas.save()
    return response
