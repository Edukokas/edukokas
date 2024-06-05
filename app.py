from flask import Flask, request, render_template, send_file, url_for
import PyPDF2
import os

app = Flask(__name__)


def unir_pdfs(lista_pdfs, salida):
    pdf_writer = PyPDF2.PdfWriter()
    for pdf in lista_pdfs:
        pdf_reader = PyPDF2.PdfReader(pdf)
        for pagina in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[pagina])
    with open(salida, 'wb') as salida_pdf:
        pdf_writer.write(salida_pdf)


def separar_pdfs(pdf_entrada, paginas_seleccionadas, salida):
    pdf_reader = PyPDF2.PdfReader(pdf_entrada)
    pdf_writer = PyPDF2.PdfWriter()
    for pagina in paginas_seleccionadas:
        pdf_writer.add_page(pdf_reader.pages[pagina])
    with open(salida, 'wb') as salida_pdf:
        pdf_writer.write(salida_pdf)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/subir', methods=['POST'])
def subir():
    archivo = request.files['archivo']
    archivo.save(os.path.join('static', archivo.filename))
    return render_template('ver_pdf.html', nombre_archivo=archivo.filename)


@app.route('/separar', methods=['POST'])
def separar():
    nombre_archivo = request.form['nombre_archivo']
    paginas = request.form['paginas']
    paginas_seleccionadas = [int(p.strip()) for p in paginas.split(',')]

    archivo_salida_separado = 'separado.pdf'
    separar_pdfs(os.path.join('static', nombre_archivo), paginas_seleccionadas, archivo_salida_separado)

    return send_file(archivo_salida_separado, as_attachment=True)


@app.route('/unir', methods=['POST'])
def unir():
    archivos = request.files.getlist('archivos')
    lista_pdfs = []
    for archivo in archivos:
        archivo.save(os.path.join('static', archivo.filename))
        lista_pdfs.append(os.path.join('static', archivo.filename))

    archivo_salida_unido = 'unido.pdf'
    unir_pdfs(lista_pdfs, archivo_salida_unido)

    return send_file(archivo_salida_unido, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
