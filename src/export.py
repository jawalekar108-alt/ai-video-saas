from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):

    def header(self):

        self.set_font("Helvetica","B",14)

        self.cell(0,10,"AI Video Intelligence Report",new_x="LMARGIN",new_y="NEXT",align="C")

        self.ln(5)

    def footer(self):

        self.set_y(-15)

        self.set_font("Helvetica",size=8)

        self.cell(

        0,

        10,

        f"Generated {datetime.now().strftime('%Y-%m-%d')} | Page {self.page_no()}",

        align="C"

        )


def export_pdf(title,content):

    try:

        pdf=PDF()

        pdf.add_page()

        pdf.set_font("Helvetica","B",15)

        pdf.multi_cell(0,10,title)

        pdf.ln(4)

        pdf.set_font("Helvetica",size=11)

        content=str(content)

        # safer encoding
        content=content.encode("latin-1","replace").decode("latin-1")

        pdf.multi_cell(0,7,content)

        return bytes(pdf.output(dest="S"))

    except Exception as e:

        print("PDF ERROR:",e)

        return None