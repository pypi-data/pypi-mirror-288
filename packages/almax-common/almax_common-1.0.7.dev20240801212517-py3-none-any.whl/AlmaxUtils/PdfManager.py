import AlmaxUtils.Time as TimeLib
import os
import pypdf

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def GeneratePdf(client_info, orders, totalObj, finalText: list, documentType: str) -> str:
    now = TimeLib.now
    now_month = now.month if now.month > 9 else f"0{now.month}"
    now_day = now.day if now.day > 9 else f"0{now.day}"
    now_hour = now.hour if now.hour > 9 else f"0{now.hour}"
    now_minute = now.minute if now.minute > 9 else f"0{now.minute}"
    now_second = now.second if now.second > 9 else f"0{now.second}"

    file_path = f"{documentType}/{now.year}/{now_month}"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path = f"{file_path}/{now_day}_{now_hour}{now_minute}{now_second}.pdf"

    size_societyName = 25
    margin = 10
    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin,
    )

    content = []
    styles = getSampleStyleSheet()

    header_table_data = [
        [
            Paragraph(
                f"<font color='red' size={size_societyName}>M</font><font color='black' size={size_societyName}>A</font> SRLS",
                ParagraphStyle(
                    name=any,
                    parent=styles["Normal"],
                    fontName="Times-Roman",  # Cambia con il tuo font preferito
                    fontSize=12,
                ),
            ),
            documentType,
        ],
        ["", ""],
        [
            Paragraph(
                f"Via Cefalonia 24, Brescia (BS)",
                ParagraphStyle(
                    name=any,
                    parent=styles["Normal"],
                    fontName="Times-Roman",
                ),
            ),
            Paragraph(
                f"Spettabile {client_info}",
                ParagraphStyle(
                    name="Centered1",
                    parent=getSampleStyleSheet()["Normal"],
                    fontName="Times-Bold",
                    alignment=1,  # 0=left, 1=center, 2=right
                ),
            ),
        ],
        [
            Paragraph(
                f"P.IVA 04033430986",
                ParagraphStyle(
                    name=any,
                    parent=styles["Normal"],
                    fontName="Times-Roman",
                ),
            ),
            "",
        ],
    ]

    header_table_style = TableStyle(
        [
            # startcol, startrow - endcol, endrow
            ("FONT", (0, 0), (1, 0), "Times-Bold"),
            ("SIZE", (0, 0), (1, 0), 15),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TEXTCOLOR", (0, 0), (1, 0), colors.red),
        ]
    )

    header_table = Table(
        header_table_data, colWidths=[doc.width / 2 - 10, doc.width / 2 - 10]
    )
    header_table.setStyle(header_table_style)
    content.append(header_table)

    content.append(Spacer(1, 10))  # Aggiungi spaziatura

    body_table_data = [["Descrizione", "Quantità", "Prezzo €", "Totale € (no IVA)"]]
    for order in orders:
        attributes = [
            order["Description"],
            order["Quantity"],
            order["Price"],
            order["Total"],
        ]
        body_table_data.append(ToParagraph_ForTable(attributes))
    body_table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.red),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
    )
    body_table = Table(body_table_data, colWidths=[368, 48, 60, 82])
    body_table.setStyle(body_table_style)
    content.append(body_table)

    table_data = [["", ""]]
    styleIva = ParagraphStyle(
        name="Centered1",
        parent=getSampleStyleSheet()["Normal"],
        fontName="Times-Roman",
        alignment=0,  # 0=left, 1=center, 2=right
    )
    styleIvaPrice = ParagraphStyle(
        name="Centered2",
        parent=getSampleStyleSheet()["Normal"],
        fontName="Helvetica",
        alignment=0,  # 0=left, 1=center, 2=right
    )
    noIva = [
        Paragraph(totalObj[0]["text"], styleIva),
        Paragraph(totalObj[0]["value"], styleIvaPrice),
    ]
    iva = [
        Paragraph(totalObj[1]["text"], styleIva),
        Paragraph(totalObj[1]["value"], styleIvaPrice),
    ]
    totale = [
        Paragraph(
            totalObj[2]["text"],
            ParagraphStyle(
                name="Centered1",
                parent=getSampleStyleSheet()["Normal"],
                fontName="Times-Bold",
                alignment=0,  # 0=left, 1=center, 2=right
            ),
        ),
        Paragraph(
            totalObj[2]["value"],
            ParagraphStyle(
                name="Centered2",
                parent=getSampleStyleSheet()["Normal"],
                fontName="Helvetica-Bold",
                alignment=0,  # 0=left, 1=center, 2=right
            ),
        ),
    ]
    table_data.append(noIva)
    table_data.append(iva)
    table_data.append(totale)
    table = Table(table_data, [115, 75])
    table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),  # Align all cells to the left
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),  # Center header text
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Center text vertically
                # ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    content.append(table)

    content.append(Spacer(1, 12))  # Aggiungi spaziatura

    for text in finalText:
        content.append(
            Paragraph(
                text,
                ParagraphStyle(
                    name="Centered",
                    parent=getSampleStyleSheet()["Normal"],
                    fontName="Times-Bold",
                    alignment=1,  # 0=left, 1=center, 2=right
                    textColor=colors.red,
                ),
            )
        )

    # Build the PDF
    doc.build(content)

    return file_path
    # try:
    # except Exception as e:
    #    print(f'Error generating PDF: {e}');


def ToParagraph_ForTable(elements: list, setStyle=False):
    style = ParagraphStyle(
        name="Centered1",
        parent=getSampleStyleSheet()["Normal"],
        fontName="Times-Roman",
        alignment=0,  # 0=left, 1=center, 2=right
    )
    if setStyle:
        return [Paragraph(f"{element}", style) for element in elements]
    return [Paragraph(f"{element}") for element in elements]


def DivideAndMergePages(pdf_vecchio, indici_pagine, directorySalvataggio, nomeFile):
    """- DA RISCRIVERE - La funzione usa la libreria PyPDF2 e si occupa di strarre le singole pagine da un dato PDF.
    pdf_vecchio è il reader, generalmente dichiarato come pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    indici_pagine è la posizione delle pagine specifiche da estrarre; può essere un singolo indice o più di uno; in case fossero tanti, è strettamente necessario sia un array
    directorySalvataggio è il nome della cartella in cui salvare il/i file_estratto
    nomeFile è il nome che verrà assegnato al PDF contenente le pagine divise."""

    file_da_scrivere = pypdf.PdfFileWriter()

    if isinstance(indici_pagine, list):
        for i in indici_pagine:
            file_da_scrivere.addPage(pdf_vecchio.getPage(i))
    else:
        file_da_scrivere.addPage(pdf_vecchio.getPage(indici_pagine))

    # Metto ogni file diviso nell'apposita cartella
    with open(directorySalvataggio + "/" + nomeFile, "wb") as file_estratto:
        file_da_scrivere.write(file_estratto)


def MergePDFs(nome_pdf1, nome_pdf2, directorySalvataggio):
    # Lettura PDF
    # nomePDF = simpledialog.askstring(title=nomeProgramma, prompt="Inserire il nome del file PDF senza l'estensione.\nEsempio: se il file si chiama 'test.pdf', basterà inserire 'test'")
    pdfFileObj_1 = open(directorySalvataggio + "/" + nome_pdf1 + ".pdf", "rb")
    pdfReader_1 = pypdf.PdfFileReader(pdfFileObj_1)
    # print("unisci Ok1" + directorySalvataggio + "/" + nome_pdf2+".pdf")
    pdfFileObj_2 = open(directorySalvataggio + "/" + nome_pdf2 + ".pdf", "rb")
    pdfReader_2 = pypdf.PdfFileReader(pdfFileObj_2)
    # print("unisci Ok2")
    numPagine1 = pdfReader_1.numPages
    numPagine2 = pdfReader_2.numPages

    pdf_unito = pypdf.PdfFileWriter()
    for i in range(numPagine1):
        pdf_unito.addPage(pdfReader_1.getPage(i))
    for i in range(numPagine2):
        pdf_unito.addPage(pdfReader_2.getPage(i))

    with open(directorySalvataggio + "/pdfUnito.pdf", "wb") as file_da_scrivere:
        pdf_unito.write(file_da_scrivere)

    pdfFileObj_1.close()
    pdfFileObj_2.close()
    os.remove(directorySalvataggio + "/" + nome_pdf1 + ".pdf")
    os.remove(directorySalvataggio + "/" + nome_pdf2 + ".pdf")
    os.rename(
        directorySalvataggio + "/pdfUnito.pdf",
        directorySalvataggio + "/" + nome_pdf1 + ".pdf",
    )
