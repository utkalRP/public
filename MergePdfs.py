from PyPDF2 import PdfFileMerger, PdfFileReader

mergerObject = PdfFileMerger()
for i in range(99,119):
    mergerObject.append(PdfFileReader(f'hhvs{i}.pdf', 'rb'))

mergerObject.write('MergedFile.pdf')
