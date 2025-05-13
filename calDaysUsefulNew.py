import pickle
import locale
import pandas as pd
import streamlit as st
import datetime
from datetime import date
from datetime import timedelta
from io import BytesIO
from os import path
import os
import streamlit.components.v1 as components
import datetime
from datetime import date
from datetime import timedelta
import time

def dateFullLang(date, mode):
    dayStr = date.day
    monthNum = date.month
    monthStr = months[monthNum]
    yearStr = date.year
    weekNum = date.weekday()
    weekStr = weeks[weekNum]
    dateFull = f'{dayStr} de {monthStr} de {yearStr}'
    if mode == 0:
        return dateFull
    else:
        return (dateFull, weekStr)   
    
def countCurUseFul(dateTuple):
    title = dateTuple[-1]
    dateIni = dateTuple[0]
    num = dateTuple[1]
    mode = dateTuple[2]
    expr = dateTuple[3]
    dateIniStr = dateIni.strftime("%d/%m/%Y")
    dateIniName = dateFullLang(dateIni, 0)
    data_atual = datetime.datetime.today()
    count = 0 
    n = 0 
    while count < num:
        dateNew = dateIni + datetime.timedelta(days=n)
        weekNum = dateNew.weekday()
        #weekName = dateNew.strftime("%A")
        dateFormat = dateNew.strftime("%d/%m/%Y")
        #dateName = dateNew.strftime("%#d de %B de %Y")
        dateResp = dateFullLang(dateNew, 1)
        dateName = dateResp[0]
        weekName = dateResp[1]
        if n == 0:
            status = 'não conta'
        else: 
            if mode == 0:
                if count == num - 1: 
                    if any ([weekNum == 5 or weekNum == 6]):
                        status = 'não conta'
                    else:
                        status = 'conta'
                        count += 1
                else:
                    status = 'conta'
                    count += 1
            else:
                if any ([weekNum == 5 or weekNum == 6]):
                    status = 'não conta'
                else:
                    status = 'conta'
                    count += 1
        if status == 'conta': 
            countStr = f'{str(count)}.°'
        else: 
            countStr = ''        
        infoCombo = [f'{dateFormat} ({dateName})', weekName, status, countStr, n + 1]
        for i, info in enumerate(infoCombo):
            key = keyCurrent[i]
            dateCurrUse[key].append(info)    
        n += 1
    dayFinal = dateCurrUse[keyCurrent[0]]
    if len(dayFinal) == 0:
        dateFinal = f'{dateIniStr} ({dateIniName})'
    else:
        dateFinal = dayFinal[-1]
    nLanc = len(dateCurrUse[keyCurrent[0]])
    st.markdown(f":page_with_curl: **<font color={color}>{title}</font>**", True)
    colStart, colFinal, colCrit = st.columns(spec=3, gap='small', vertical_alignment='top', border=True)
    colStart.markdown(f'**Data inicial**  : {dateIniStr} ({dateIniName})')
    colFinal.markdown(f'**Data Final**  : {dateFinal}')
    colCrit.markdown(f"**Critério**: {expr}")
    colDays, colLanc = st.columns(spec=2, gap='small', vertical_alignment='top', border=True)
    colDays.markdown(f'**Número de dias informados**: {num}')
    colLanc.markdown(f'**Número de dias lançados**: {nLanc}')

def treatmentDf(title, field):
    df = pd.DataFrame(dateCurrUse)
    dfTerm = df[field].value_counts()
    dfTerm = dfTerm.reset_index()
    dfTerm = dfTerm.rename(columns={'index': field})
    dfTerm = dfTerm.rename(columns={'count': 'frequência'})
    colEmpty, = st.columns(spec=1, gap='small', vertical_alignment='top')
    colEmpty.text('')
    colEstat, = st.columns(spec=1, gap='small', vertical_alignment='top')
    colEstat.markdown(f":page_facing_up: **<font color={color}>{title}</font>**", True)
    return dfTerm
    
def graphicDf(title):
    chartData = pd.DataFrame(dfCount)
    colEmpty, = st.columns(spec=1, gap='small', vertical_alignment='top')
    colEmpty.text('')
    colEstat, = st.columns(spec=1, gap='small', vertical_alignment='top')
    colEstat.markdown(f":bar_chart: **<font color={color}>{title}</font>**", True)
    
    #colEstat.markdown(f":bar_chart: **:blue[{title}]**")
    return chartData
    
# Function to convert DataFrame to Excel file in memory
def toCsv():
    csv = df.to_csv(index=False).encode('ISO-8859-1')
    return csv

def toPickle():
    pkl = pickle.dumps(df)
    return pkl

def toHtml():
    htmlText = df.to_html(index=False)
    htmlText += dfCount.to_html(index=False)
    hmtlPlus = """
    <style>
        .button {
          background-color: #04AA6D; /* Green */
          border: None;
          color: white;
          text-align: center;
          text-decoration: none;
          display: inline-block;
          font-size: 13px;
          margin: 6px 2px;
          cursor: pointer;
        }
        .button1 {padding: 8px 14px;}
    </style>
    <button class="button button1" onclick=window.print()>Imprime</button>
    """    
    htmlText += f"<body>{hmtlPlus}</body>"
    return htmlText
    
def toTxt():
    txt = df.to_string(index=False).encode('ISO-8859-1') 
    txt += dfCount.to_string(index=False).encode('ISO-8859-1')
    return txt
 
def toJson():
    json = df.to_json()
    json += dfCount.to_json()
    return json
    
def toTex():
    tex = df.to_latex()
    tex += dfCount.to_latex()
    return tex

def toInClip(mode):
    if mode == 0:
        txt = df.to_string(index=False).encode('ISO-8859-1') 
        txt += dfCount.to_string(index=False).encode('ISO-8859-1')
    else:
        txt = ''
    codeJs = f"""navigator.clipboard.writeText({txt});"""
    jsHtml = f"""
    <script>
    {codeJs};
    </script>
    """
    components.html(jsHtml)
    
def iniVars():
    prefix = f'dfTable_{plur}'
    labels = {'csv':[f'{prefix}.csv', "Download das tabelas para o formato 'csv'.", ":material/download:"], 
              'pickle': [f'{prefix}.pkl', "Download das tabelas para o formato 'pickle'.", ":material/download:"], 
              'html': [f'{prefix}.html', "Download das tabelas para o formato 'html'.", ":material/download:"], 
              'txt': [f'{prefix}.txt', "Download das tabelas para o formato 'txt'.", ":material/download:"], 
              'json': [f'{prefix}.json', "Download das tabelas para o formato 'json'.", ":material/download:"], 
              'latex': [f'{prefix}.tex', "Download das tabelas para o formato 'tex'.", ":material/download:"], 
              'clipboard': ['', "Envia os dados das tabelas para a área de transferência.", ":material/assignment:"], 
              'clear': ['', "Limpa a área de transferência.", ":material/mop:"]
             }
    keys = list(labels.keys())
    colorOpt = st.session_state.colorOpt
    with st.container(border=False):
        colOpt, = st.columns(spec=1, gap='small', vertical_alignment='center', border=False)
        st.markdown(f":point_right: **<font color={colorOpt}>Opções</font>**", True)
        #st.markdown(f":point_right: {color}[opções]**")
        #Csv
        colCsv, colPkl, colHtml, colString = st.columns(spec=4, gap='small', vertical_alignment='center', border=False)
        colJson, colLatex, colClip, colClear = st.columns(spec=4, gap='small', vertical_alignment='top', border=False)
        if colCsv.download_button(
            label=keys[0],
            use_container_width=True, 
            data=toCsv(),
            file_name=labels[keys[0]][0],
            mime='text/csv', 
            help=labels[keys[0]][1], 
            icon=labels[keys[0]][2]
            ):
            st.session_state.files.append(labels[keys[0]][0])
        #Pkl
        if colPkl.download_button(
            label=keys[1],
            use_container_width=True, 
            data=toPickle(),
            file_name=labels[keys[1]][0],
            mime="application/octet-stream", 
            help=labels[keys[1]][1], 
            icon=labels[keys[1]][2]
            ): 
            st.session_state.files.append(labels[keys[1]][0])
        #Html
        if colHtml.download_button(
            label=keys[2],
            use_container_width=True, 
            data=toHtml(),
            file_name=labels[keys[2]][0], 
            help=labels[keys[2]][1], 
            icon=labels[keys[2]][2]
            ):
            st.session_state.files.append(labels[keys[2]][0])
        #String 
        if colString.download_button(
            label=keys[3],
            use_container_width=True, 
            data=toTxt(),
            file_name=labels[keys[3]][0], 
            help=labels[keys[3]][1], 
            icon=labels[keys[3]][2] 
            ):
            st.session_state.files.append(labels[keys[3]][0])
        #Json
        if colJson.download_button(
            label=keys[4],
            use_container_width=True,
            data=toJson(),
            file_name=labels[keys[4]][0], 
            help=labels[keys[4]][1], 
            icon=labels[keys[4]][2]
            ):
            st.session_state.files.append(labels[keys[4]][0])
        #Tex
        if colLatex.download_button(
            label=keys[5],
            use_container_width=True,
            data=toTex(),
            file_name=labels[keys[5]][0], 
            help=labels[keys[5]][1], 
            icon=labels[keys[5]][2]
            ):
            st.session_state.files.append(labels[keys[5]][0])
        #Clipboard
        if colClip.button(
            label=keys[6],
            use_container_width=True, 
            help=labels[keys[6]][1], 
            icon=labels[keys[6]][2]
        ):
            toInClip(0)        
        #Clear
        if colClear.button(
            label=keys[7],
            use_container_width=True, 
            help=labels[keys[7]][1], 
            icon=labels[keys[7]][2]
        ):
            toInClip(1)
            
def checkDate(dateSel, nDays):
    if nDays <= 0:
        st.toast("⚠️ e os gráficos não exibirão dados representativos da contagem!")
        time.sleep(0.2)
        st.toast(f"⚠️ A rotina baseou-se em {nDays} dia {sing}, de modo que as tabelas (junto com os arquivos de download) ")
        time.sleep(0.2)
        
def main():
    global output, dirRoot
    global keyCurrent, keyUseFul
    global dateCurrUse, df, dfCount 
    global months, weeks
    keyCurrent = ['dia do mês', 'dias da semana', 
                  'condição', 'sequencial', 'contador geral']
    dateCurrUse = {key:[] for key in keyCurrent}
    months = {1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril', 5:'maio', 6: 'junho', 
              7: 'julho', 8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'}
    weeks = {6: 'domingo', 0: 'segunda-feira', 1: 'terça-feira', 
             2: 'quarta-feira', 3: 'quinta-feira', 4: 'sexta-feira', 
             5: 'sábado'}
    dateNow = datetime.date.today()
    dayFirst = st.session_state['acesso'][0]
    nDays = st.session_state['acesso'][1]
    args =  [(dayFirst, nDays, 0, f'contagem em dias {plur}', 'Demonstrativo cronológico')]
    for a, arg in enumerate(args):
        #st.divider()
        if a == (len(args) - 1): 
            st.write('')
            st.write('')
        countCurUseFul(arg)
        df = pd.DataFrame(dateCurrUse)
        #['dia do mês', 'dias da semana', 
        #'condição', 'sequencial', 'contador geral']
        for f in [1, 2]: 
            field = keyCurrent[f]
            title = f"Binômio '{field} x frequência' no período da contagem"
            st.dataframe(data=df, hide_index=True, use_container_width=True)
            dfCount = treatmentDf(title, field)
            st.dataframe(data=dfCount, hide_index=True, use_container_width=True)
            chartData = graphicDf(title)
            st.bar_chart(chartData, y="frequência", x=field)        
        output = BytesIO() 
    iniVars()

if __name__ == '__main__':
    global timeDay
    global cliks
    global sing, plur, symb, color   
    timeDay = 0.5
    sing = 'útil'
    plur = 'úteis'
    symb = '📙'
    dateSel = st.session_state.acesso[0]
    nDays = st.session_state.acesso[1]
    val = checkDate(dateSel, nDays)
    st.spinner('Confecção do demonstrativo de dias corridos em andamento. Aguarde...', show_time=True)
    color = st.session_state.color
    st.markdown(f"# Prazo em dias {plur} {symb}")
    main()
        