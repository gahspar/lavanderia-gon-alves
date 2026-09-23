from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image

ROOT = Path(r"C:\Users\paulo\OneDrive\Documentos\ChatGPT\Lavanderia Gonçalves & Duwe")
SHOT = ROOT / "output" / "screenshots"
OUT = ROOT / "output" / "pdf" / "Proposta_Site_Lavanderia_Goncalves_Duwe.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

NAVY = "#101B42"
NAVY2 = "#182857"
GOLD = "#D9AA3D"
GOLD2 = "#F1D48A"
INK = "#172039"
MUTED = "#687086"
IVORY = "#F7F5EF"
WHITE = "#FFFFFF"
LINE = "#DDE2EA"

pdfmetrics.registerFont(TTFont("Body", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Body-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Display", r"C:\Windows\Fonts\georgia.ttf"))
pdfmetrics.registerFont(TTFont("Display-Bold", r"C:\Windows\Fonts\georgiab.ttf"))

W, H = landscape(A4)
c = canvas.Canvas(str(OUT), pagesize=(W, H))
c.setTitle("Proposta de Site - Lavanderia Gonçalves & Duwe")
c.setAuthor("Apresentação comercial")
c.setSubject("Mockup completo de site, decisões estratégicas e plano de implementação")


def hexcolor(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i+2], 16) / 255 for i in (0, 2, 4))


def color(value):
    c.setFillColorRGB(*hexcolor(value))


def stroke(value):
    c.setStrokeColorRGB(*hexcolor(value))


def wrap(text, font, size, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = word if not line else line + " " + word
        if pdfmetrics.stringWidth(trial, font, size) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def paragraph(text, x, y, width, font="Body", size=9.2, leading=13, fill=MUTED, max_lines=None):
    color(fill)
    c.setFont(font, size)
    lines = wrap(text, font, size, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def label(text, x, y, fill=GOLD):
    color(fill)
    c.setFont("Body-Bold", 7.2)
    c.drawString(x, y, text.upper())
    return y - 14


def heading(text, x, y, width, size=22, fill=INK):
    color(fill)
    c.setFont("Display-Bold", size)
    lines = wrap(text, "Display-Bold", size, width)
    for line in lines:
        c.drawString(x, y, line)
        y -= size * 1.15
    return y


def bullet(text, x, y, width, fill=WHITE):
    color(GOLD)
    c.circle(x + 3, y + 3, 2.2, fill=1, stroke=0)
    return paragraph(text, x + 13, y + 7, width - 13, font="Body", size=8.5, leading=11.5, fill=fill)


def draw_image_fit(path, x, y, w, h, bg=WHITE, pad=0):
    color(bg)
    c.rect(x, y, w, h, fill=1, stroke=0)
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min((w - 2 * pad) / iw, (h - 2 * pad) / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(str(path)), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, preserveAspectRatio=True, mask="auto")


def page_header(page_num, title):
    color(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    color(NAVY)
    c.rect(0, H - 42, W, 42, fill=1, stroke=0)
    color(GOLD2)
    c.setFont("Display-Bold", 11)
    c.drawString(28, H - 27, "Gonçalves & Duwe")
    color(WHITE)
    c.setFont("Body", 7)
    c.drawString(144, H - 26, title.upper())
    c.setFont("Body-Bold", 7)
    c.drawRightString(W - 28, H - 26, f"{page_num:02d} / 07")


def insight_page(page_num, page_title, image_name, panel_title, intro, bullets, footer):
    page_header(page_num, page_title)
    image_x, image_y, image_w, image_h = 28, 28, 545, H - 86
    panel_x, panel_y, panel_w, panel_h = 592, 28, W - 620, H - 86
    draw_image_fit(SHOT / image_name, image_x, image_y, image_w, image_h, bg=IVORY, pad=6)
    color(NAVY)
    c.roundRect(panel_x, panel_y, panel_w, panel_h, 4, fill=1, stroke=0)
    y = H - 76
    y = label("Insight comercial", panel_x + 22, y, GOLD2)
    y = heading(panel_title, panel_x + 22, y, panel_w - 44, 19, WHITE) - 8
    y = paragraph(intro, panel_x + 22, y, panel_w - 44, size=8.7, leading=12.2, fill="#CBD1E0") - 12
    stroke("#35436B")
    c.line(panel_x + 22, y, panel_x + panel_w - 22, y)
    y -= 20
    for item in bullets:
        y = bullet(item, panel_x + 22, y, panel_w - 44, WHITE) - 10
    paragraph(footer.upper(), panel_x + 22, panel_y + 31, panel_w - 44, font="Body-Bold", size=6.6, leading=8.2, fill=GOLD2, max_lines=2)
    c.showPage()


# 1 - Cover
color(NAVY)
c.rect(0, 0, W, H, fill=1, stroke=0)
draw_image_fit(SHOT / "01-hero.png", 0, 0, 555, H, bg=NAVY)
color(NAVY)
c.rect(540, 0, W - 540, H, fill=1, stroke=0)
color(GOLD)
c.rect(540, 0, 7, H, fill=1, stroke=0)
x, y = 578, H - 72
y = label("Proposta visual e estratégica", x, y, GOLD2) - 8
y = heading("Um site que transforma confiança local em novos orçamentos.", x, y, W - x - 38, 25, WHITE) - 10
y = paragraph("Mockup profissional para apresentar uma presença digital alinhada aos 30+ anos da Lavanderia Gonçalves & Duwe.", x, y, W - x - 38, size=9.2, leading=13.5, fill="#D4D8E3") - 24
stroke("#39466C")
c.line(x, y, W - 38, y)
y -= 24
for item in [
    "Jornada clara para hotelaria e atendimento residencial.",
    "Orçamento por WhatsApp como ação principal.",
    "Prova social, cobertura e experiência logo nas áreas decisivas.",
    "Layout responsivo, pronto para demonstração em celular e desktop.",
]:
    y = bullet(item, x, y, W - x - 38, WHITE) - 12
color(GOLD2)
c.setFont("Body-Bold", 7.4)
c.drawString(x, 48, "LAVANDERIA GONÇALVES & DUWE  ·  BLUMENAU / SC")
c.showPage()


# 2 - Hero
insight_page(
    2,
    "Primeira dobra e posicionamento",
    "01-hero.png",
    "A proposta de valor aparece antes de qualquer distração.",
    "A primeira tela combina credibilidade, clareza e ação. Em poucos segundos, o visitante entende o serviço, reconhece o padrão profissional e encontra o caminho para pedir orçamento.",
    [
        "Mensagem que conversa com hotéis e famílias sem diluir o posicionamento.",
        "30+ anos, nota 4,9 e 60 avaliações reduzem a insegurança de um novo cliente.",
        "Botão amarelo cria contraste e leva direto ao WhatsApp com mensagem pronta.",
        "Fotografia premium posiciona o serviço acima da disputa apenas por preço.",
    ],
    "Objetivo: gerar contato já na primeira tela",
)


# 3 - Solutions
insight_page(
    3,
    "Soluções e segmentação",
    "02-solucoes.png",
    "Dois públicos, duas conversas comerciais específicas.",
    "A separação entre hotelaria e residencial torna a proposta relevante para cada perfil e evita que o cliente precise interpretar se o serviço atende sua necessidade.",
    [
        "Hotelaria recebe destaque visual por ter maior recorrência e valor de contrato.",
        "Abrangência de Blumenau, Pomerode e Timbó aparece dentro da própria oferta.",
        "Residencial comunica praticidade, itens atendidos e limite geográfico correto.",
        "Cada botão abre uma conversa de WhatsApp com contexto diferente para facilitar a triagem.",
    ],
    "Objetivo: aumentar a qualidade dos pedidos de orçamento",
)


# 4 - Process and coverage
insight_page(
    4,
    "Processo e cobertura",
    "03-processo-cobertura.png",
    "O site antecipa as duas maiores dúvidas antes do contato.",
    "Explicar como funciona e onde a empresa atende reduz fricção. O cliente chega ao WhatsApp com mais confiança e com uma expectativa melhor alinhada sobre logística e prazo.",
    [
        "Etapas simples tornam um serviço operacional fácil de compreender.",
        "Coleta, tratamento e entrega são apresentados como um fluxo organizado.",
        "Mapa estilizado reforça presença regional sem depender de texto longo.",
        "A divisão de cobertura protege a operação: hotelaria regional e residencial local.",
    ],
    "Objetivo: reduzir objeções e contatos fora da área atendida",
)


# 5 - Story and reviews
insight_page(
    5,
    "História e prova social",
    "04-historia-avaliacoes.png",
    "Tempo de mercado e avaliações viram argumentos de venda.",
    "Uma empresa com trajetória desde 1995 não precisa parecer nova para parecer atual. O design organiza essa história e transforma reputação já conquistada em confiança digital.",
    [
        "O marco de 1995 comunica permanência, experiência e segurança.",
        "A nota 4,9/5 é mostrada perto de depoimentos reais e específicos.",
        "Comentários sobre atendimento, organização e prazo respondem às objeções centrais do nicho.",
        "A seção funciona como validação para quem chegou por indicação ou pesquisa no Google.",
    ],
    "Objetivo: dar prova concreta antes da decisão",
)


# 6 - FAQ and close
insight_page(
    6,
    "Dúvidas, chamada final e contato",
    "06-faq-cta-footer.png",
    "O fechamento da página conduz para uma ação sem pressão.",
    "Depois de conhecer a empresa, o visitante encontra respostas rápidas, uma chamada direta e todos os canais de contato. O objetivo é não perder quem chegou ao fim da página ainda com uma dúvida.",
    [
        "FAQ responde peças atendidas, hotelaria, coleta e orçamento.",
        "Chamada final retoma o benefício e abre o WhatsApp.",
        "Rodapé reúne telefone, endereço, Instagram e horário de atendimento.",
        "A estrutura também fortalece a presença local em buscas por lavanderia em Blumenau.",
    ],
    "Objetivo: converter a última dúvida em conversa",
)


# 7 - Mobile + rollout plan
page_header(7, "Experiência mobile e plano de implementação")
draw_image_fit(SHOT / "05-mobile.png", 34, 28, 250, H - 86, bg=NAVY, pad=4)
x = 315
y = H - 77
y = label("Pronto para o uso real", x, y) - 8
y = heading("O caminho para colocar este modelo no ar.", x, y, W - x - 36, 22, INK) - 5
y = paragraph("A maior parte dos contatos locais tende a acontecer pelo celular. Por isso, o mockup mantém leitura, prova social e orçamento acessíveis em telas menores.", x, y, W - x - 36, size=9, leading=13, fill=MUTED) - 18

phases = [
    ("01", "Validação comercial", "Confirmar serviços, horários, áreas de coleta, fotos reais e diferenciais operacionais."),
    ("02", "Conteúdo final", "Revisar textos, selecionar depoimentos autorizados e atualizar as imagens da operação."),
    ("03", "Publicação", "Conectar domínio, WhatsApp, métricas de acesso e informações locais para busca."),
    ("04", "Evolução", "Acompanhar cliques e pedidos para melhorar campanhas, páginas e chamadas comerciais."),
]
for num, title, desc in phases:
    color(NAVY)
    c.roundRect(x, y - 54, 38, 38, 3, fill=1, stroke=0)
    color(GOLD2)
    c.setFont("Display-Bold", 12)
    c.drawCentredString(x + 19, y - 41, num)
    color(INK)
    c.setFont("Body-Bold", 10)
    c.drawString(x + 52, y - 28, title)
    paragraph(desc, x + 52, y - 42, W - x - 90, size=8, leading=10.7, fill=MUTED, max_lines=2)
    y -= 72

color(IVORY)
c.roundRect(x, 39, W - x - 36, 72, 4, fill=1, stroke=0)
color(NAVY)
c.setFont("Display-Bold", 14)
c.drawString(x + 18, 84, "Resultado esperado")
paragraph("Uma presença digital clara, confiável e mensurável, preparada para transformar pesquisa e indicação em conversas comerciais qualificadas.", x + 18, 68, W - x - 72, size=8.5, leading=11.5, fill=MUTED)
c.showPage()

c.save()
print(OUT)
