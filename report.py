
import sys
import json
import argparse
import os
import locale
from reportlab.platypus import *
from reportlab.lib import utils
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from time import *
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

styles = getSampleStyleSheet()

if __name__=='__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--datos', nargs=1,
                      help="JSON String para procesar")
  parser.add_argument('--filesPath', nargs=1,
                     help="carpeta de destino")
  parser.add_argument('--fileName', nargs=1,
                     help="nombre aleatorio")
  arguments = parser.parse_args()
  print('arguments',arguments)
  data = json.loads(arguments.datos[0])
  filesPath = arguments.filesPath[0]
  fileName = arguments.fileName[0]
# Datos para PDF
reportData = data['reportData']
companyData = data['companyData']
# Locaciones desde JSON
LocationsList = reportData['locations']
headerData = reportData['headerReport']
Company = companyData['name']
Address = companyData['address']
Audit = headerData['gembaWalkName']
Status = str(headerData['score'])
User = headerData['user']
TitleFooter = headerData['revision'] if headerData['revision'] else 'Gemba Walks Statistics Report'

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = letter[0]

# Iconos para status de tarea
badIcon = Image(filesPath+'bad.png')
badIcon.drawHeight = 0.25*inch*badIcon.drawHeight / badIcon.drawWidth
badIcon.drawWidth = 0.25*inch
successIcon = Image(filesPath+'success.png')
successIcon.drawHeight = 0.25*inch*successIcon.drawHeight / successIcon.drawWidth
successIcon.drawWidth = 0.25*inch

colwidths = ( PAGE_WIDTH-( 3*inch ), 1*inch )

GRID_HEADER = TableStyle(
  [
    # Encabezado
    ('GRID', (0,0), (-1,-1), 1, colors.transparent),
    ('BACKGROUND', (0, 0), (-1, 0), colors.lemonchiffon),
    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('ALIGN', (1, 0), (-1,-0), 'RIGHT'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 15),
    ('TOPPADDING', (0, 0), (-1, 0), 15),
  ]
)
GRID_TASKS = TableStyle(
  [
    ('GRID', (0, 0), (-1,-1), 1, colors.transparent),
    ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.black),
    ('LINEABOVE',(0,0), (-1,0), 1.5, colors.black),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('ALIGN', (1, 0), (-1,-0), 'RIGHT'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('TOPPADDING', (0, 0), (-1, 0), 12),
  ]
)
GRID_CONTENT = TableStyle(
  [
    ('GRID', (0, 0), (-1,-1), 1, colors.transparent),
    ('LINEBELOW', (0, 0), (-1, -1), 0.75, colors.gray),
    ('ALIGN', (1, 0), (-1, -0), 'CENTER'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 13),
    ('TOPPADDING', (0, 0), (-1, 0), 13),
    ('LEFTPADDING', (0, 0), (-1, 0), 25)
  ]
)

# Formato de fecha
dbDtFormat = '%A, %d/%B/%Y %H:%M'
# locale.setlocale(locale.LC_ALL, '')
reportDate = strftime(dbDtFormat, localtime() )

# Medidas logos
companyData = data['companyData']
companyLogo = utils.ImageReader('http://'+companyData['image'])
iGoSeeLogo = utils.ImageReader(filesPath+'logo.png')
companyLogo_width, companyLogo_height = companyLogo.getSize()
iGoSeeLogo_width, iGoSeeLogo_height = iGoSeeLogo.getSize()
aspectCompany = companyLogo_height / float(companyLogo_width)
aspectiGoSee = iGoSeeLogo_height / float(iGoSeeLogo_width)

def firstPage(canvas, doc):
  canvas.saveState()
  # Header
  canvas.setFont( 'Helvetica', 16 )
  canvas.drawImage( companyLogo, 65, PAGE_HEIGHT-108,
                      width=65, height=(65 * aspectCompany ) )
  canvas.drawString(150, PAGE_HEIGHT-85, Company)
  canvas.setFont( 'Helvetica', 12 )
  canvas.drawString(150, PAGE_HEIGHT-105, Address)
  canvas.line(50, 720, 550, 720)
  canvas.setFont( 'Helvetica', 16 )
  canvas.drawString(65, PAGE_HEIGHT-150, Audit)
  canvas.drawString(PAGE_WIDTH - (1.5 * inch), PAGE_HEIGHT-150, Status)
  # Footer
  canvas.setFont( 'Helvetica', 10 )
  canvas.drawString( 65, inch * 1.05, TitleFooter )
  canvas.drawString( PAGE_WIDTH - (3 * inch), inch * 1.05, reportDate )
  canvas.line(50, 70, 550, 70)
  canvas.drawString( 65, inch * 0.70, 'Pag. %d' % doc.page )
  canvas.drawString( 250, inch * 0.70, 'iGo&See Report Generator' )
  canvas.drawImage( iGoSeeLogo, PAGE_WIDTH - (1.55 * inch), 0.55 * inch,
                      width=35, height=(35 * aspectiGoSee ) )
  canvas.restoreState()

def laterPages(canvas, doc):
  canvas.saveState()
  # Footer
  canvas.setFont( 'Helvetica', 10 )
  canvas.drawString( 65, inch * 1.05, TitleFooter )
  canvas.drawString( PAGE_WIDTH - (3 * inch), inch * 1.05, reportDate )
  canvas.line(50, 70, 550, 70)
  canvas.drawString( 65, 0.70 * inch, 'Pag. %d' % doc.page )
  canvas.drawString( 250, inch * 0.70, 'iGo&See Report Generator' )
  canvas.drawImage( iGoSeeLogo, PAGE_WIDTH - (1.55 * inch), 0.55 * inch,
                      width=35, height=(35 * aspectiGoSee ) )
  canvas.restoreState()

def go():
  Elements.insert(0, Spacer(0,inch))
  save_name = os.path.join(os.path.expanduser("~"), filesPath, fileName)
  doc = SimpleDocTemplate(save_name, rightMargin=60, leftMargin=60, topMargin=30, bottomMargin=75)
  doc.build(Elements, onFirstPage=firstPage, onLaterPages=laterPages)

Elements = []
# Estilos titulos
HeaderStyle = styles["Heading1"]
ParaStyle = styles["Normal"]

def header(txt, style=HeaderStyle, klass=Paragraph, sep=0.3):
  s = Spacer(0.2*inch, sep*inch)
  Elements.append(s)
  para = klass(txt, style)
  Elements.append(para)

def tableList(item, styleTable, colTable, sep=0.3):
  s = Spacer(0.2*inch, sep*inch)
  Elements.append(s)
  t = Table( item, colTable )
  t.setStyle( styleTable )
  Elements.append(t)

def locationInfo(data):
  name = data["name"]
  score = data["score"]
  tableList([[name, (str(score) + '%')]], GRID_HEADER, colwidths)

def tasksInfo(data):
  taskName = data["name"]
  status = data["compliance"]
  if status:
    icon = successIcon
  else:
    icon = badIcon
  tableList([[taskName, icon]], GRID_TASKS, colwidths, sep=0 )

def evidenceInfo(data):
  evidenceList = []
  if data.endswith('jpg'):
    evidenceItem = Image(data)
    evidenceItem.drawHeight = 2*inch*evidenceItem.drawHeight / evidenceItem.drawWidth
    evidenceItem.drawWidth = 2*inch
    evidenceList.append([evidenceItem])
  else:
    p = Paragraph(data, styles["BodyText"])
    evidenceList.append([p])
  
  tableList(evidenceList, GRID_CONTENT, ( PAGE_WIDTH-( 2*inch )), sep=0 )

# Contenido PDF
header(User, sep=0.9, style=ParaStyle)
header(reportDate, sep=0.2, style=ParaStyle)

for location in LocationsList:
  # Titulo locacion
  tasks = location["tasksReports"]
  locationInfo(location)

  for task in tasks:
    # Titulo tareas
    evidences = task["documents"]
    tasksInfo(task)

    for evidence in evidences:
      # Evidencias
      evidenceInfo(evidence)

go()
