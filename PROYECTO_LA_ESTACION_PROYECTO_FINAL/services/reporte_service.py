from fpdf import FPDF
from flask import Response

class ReporteService:
    @staticmethod
    def generar_pdf_productos(productos):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Inventario - La Estación de los Detalles", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(80, 10, "Producto", 1)
        pdf.cell(40, 10, "Precio", 1)
        pdf.cell(40, 10, "Stock", 1)
        pdf.ln()

        pdf.set_font("Arial", size=12)
        for p in productos:
            pdf.cell(80, 10, p.nombre, 1)
            pdf.cell(40, 10, f"${p.precio}", 1)
            pdf.cell(40, 10, str(p.stock), 1)
            pdf.ln()
            
        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf')