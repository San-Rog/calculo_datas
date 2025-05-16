import streamlit as st 
import streamlit.components.v1 as components
import datetime
import time
import os
import datetime
from datetime import date
import pandas as pd
from datetime import timedelta

def checkHoliday(listDate, listHoli, date):
    dateStr =  date.strftime("%d/%m/%Y")
    try:
        return listDate.index(dateStr)
    except:
        return ""

def dateFullLang(date):
    dateStr = date.strftime("%d/%m/%Y")
    weekNum = date.weekday()
    weekStr = weeks[weekNum]
    dateFull = f'{dateStr} ({weekStr})'
    return dateFull

def findCurFul():
    listData = st.session_state.dateonly.tolist()
    listHoli = st.session_state.holonly.tolist()
    colorIni = st.session_state.color
    @st.dialog(' ')
    def config():
        colOne, colTwo = st.columns(spec=([3.5, 1]), gap="small", vertical_alignment="top", border=True)
        colOne.markdown('📁 Modifique a cor do título de tabelas e gráficos!')
        colorSel = colTwo.color_picker("Cor inicial", colorIni)
        st.session_state.color = colorSel            
    config()
    time.sleep(timeDay*1.1)
    dateIni = st.session_state[listKeys[0]]
    num = int(st.session_state[listKeys[1]])
    val = checkDate(dateIni, num)
    if not val:
        return
    for mode in [0, 1]:
        daySeq = []
        count = 0 
        n = 0 
        while count < num:
            dateNew = dateIni + datetime.timedelta(days=n)
            weekNum = dateNew.weekday()
            if n == 0:
                pass
            else: 
                if mode == 0:
                    if count == num - 1:
                        index = checkHoliday(listData, listHoli, dateNew)
                        if any ([weekNum == 5, weekNum == 6, index != '']):
                            pass
                        else:
                            count += 1
                    else:
                        count += 1
                else:
                    index = checkHoliday(listData, listHoli, dateNew)
                    if any ([weekNum == 5, weekNum == 6, index != '']):
                        pass
                    else:
                        count += 1
            daySeq.append(dateNew)    
            n += 1
        dateFinal = max(daySeq)
        dateStr = dateFullLang(dateFinal)
    st.session_state[listKeys[1]] = num        
        
def zeraWidget():
    iniFinally(1)
    
def iniFinally(mode):
    if mode == 0:
        for key in listKeys:
            if key not in st.session_state:
                try:
                    st.session_state[key] = keyNames[key]
                except:
                    pass        
    else:
        try:
            for key in listKeys:
                del st.session_state[key]
        except:
            pass
        iniFinally(0)
    try:
        st.rerun()
    except:
        pass
    st.session_state['acesso'] = [st.session_state.calendar, 
                                  st.session_state.days]
    
def changeDays():
    time.sleep(timeDay)
    nDays = st.session_state[listKeys[2]]
    nPlus = st.session_state[listKeys[1]]
    del st.session_state[listKeys[2]]
    st.session_state[listKeys[1]] = nPlus + nDays
    
def changeDate():
    valCal = st.session_state[listKeys[0]]
    del st.session_state[listKeys[0]]
    if valCal is None: 
        st.session_state[listKeys[0]] = date.today()
    else:
        try:
            st.session_state[listKeys[0]] = valCal
        except:
            st.session_state[listKeys[0]] = date.today()
            
def checkDate(dateSel, nDays):
    time.sleep(timeDay*1.1)    
    if nDays <= 0:
        block = f"Não se fará cálculo de datas, pois o número de dias é igual a {nDays}!"
        endor = False
    else:
        novaData = dateSel + datetime.timedelta(days=nDays)
        block = f"O cálculo leva em conta data de {dateSel.strftime('%d/%m/%Y')} e {nDays} dia(s)!"
        endor = True
    st.toast(f"⚠️ {block}")
    time.sleep(0.2)
    return endor

def changeSlCalend():
    time.sleep(timeDay)
    nDays = st.session_state[listKeys[5]]
    dateCalend = st.session_state[listKeys[0]] 
    newDate = dateCalend + timedelta(days=nDays)
    if newDate < dateMin: 
        newDate = dateMin
    if newDate > dateMax:
        newDate = dateMax
    st.session_state[listKeys[0]] = newDate
    del st.session_state[listKeys[5]]
    
def listFiles():
    try:
        @st.dialog(' ')
        def lista(files):
            st.markdown('📁 Arquivos nesta sessão de trabalho (pasta Downloads)')
            nFiles = len(files)
            if nFiles > 0:
                filesStr = f'{nFiles} arquivo(s): '
                for f, file in enumerate(files): 
                    #filesStr = f'#{f+1} 💾{file} '
                    st.markdown(f'#{f+1} - 💾 {file}')
            else:
                filesStr =  '✖️ Não houve download na atual sessão de uso do app!'   
                st.markdown(filesStr)
        lista(st.session_state.files)
    except:
        pass

def exibInfo():
    @st.dialog(' ')
    def config():
        info = st.session_state.info
        infoKeys = list(info.keys())
        tempus = time.time() - info[infoKeys[3]]
        st.markdown(f'**🔴 Número de acessos a módulos/submódulos do app**: {info[infoKeys[0]]}')
        st.markdown(f'**📅 Data de início da sessão**: {dateFullLang(info[infoKeys[1]])}')
        st.markdown(f'**⏲️ Hora de início**: {info[infoKeys[2]]}')
        st.markdown(f'⏳ **Tempo de uso deste app**: {tempus} segundo(s).')
    config()

def exibHoliday():
    dateOnly = st.session_state.dateonly
    nData = len(dateOnly) 
    dateAlpha = st.session_state.dateminstr
    dateOmega = st.session_state.datemaxstr
    @st.dialog(' ')
    def holid():
        st.write(f'{nData} feriado(s) - período de {dateAlpha} a {dateOmega}')
        st.dataframe(data=dfHoliday, use_container_width=True, hide_index=True) 
    holid()
def readHoliday():
    dtf = pd.read_csv('feriadosNacionais.csv')
    return dtf

def main():
    colorOpt = st.session_state.colorOpt
    with st.container(border=6):  
        colLacunose, = st.columns(1, gap='medium', vertical_alignment="center")
        with colLacunose:
            st.markdown(f":memo: **<font color={colorOpt}>Dados</font>**", True)
        colCalendar, sldDate, colDays, sldDays = st.columns([2.8, 2.5, 2.8, 2.5], gap='medium', 
                                                            vertical_alignment="center")
        dateSel = colCalendar.date_input(label='Data inicial', value='today', key=listKeys[0], 
                                         format="DD/MM/YYYY", on_change=changeDate, min_value=dateMin, max_value=dateMax,
                                         help="Digite ou selecione a data de início da contagem de prazo. Para incrementá-la, deslize o comando ao lado.")
        nSlDate = sldDate.slider(label='Incremento de data', min_value=0, max_value=6000, key=listKeys[5], 
                                 step=1, on_change=changeSlCalend, label_visibility="hidden")                         
        nDays = colDays.number_input(label='Número de dias', step=1, key=listKeys[1], 
                                     help="Digite ou incremente/decremente o número de dias da contagem. Para incrementá-lo, deslize o comando ao lado.")  
        nPlus = sldDays.slider(label='Incremento de dias', min_value=0, max_value=6000, 
                               key=listKeys[2], step=1, on_change=changeDays, label_visibility="hidden") 
        colHollow, = st.columns(1, gap='medium', vertical_alignment="center")
        with colHollow:
            st.write("")
            st.markdown(f":control_knobs: **<font color={colorOpt}>Comandos</font>**", True)
            #st.markdown(f":control_knobs: **:blue[Comandos]**")
        colCal, colFiles, colInfo, colHoliday, colClear = st.columns(spec=5, gap='small', vertical_alignment='center')
        colCal.button(label='Cálculo', use_container_width=True, icon="material:calculate:", 
                      on_click=findCurFul, help="Realize a operação necessária à contagem de dias corridos e úteis.")
        colFiles.button(label='Arquivos', use_container_width=True, icon="💾", 
                        on_click=listFiles, help="Verifique os arquivos gravados durante esta sessão de uso do aplicativo.")
        colInfo.button(label='Acesso', use_container_width=True, icon="👓", 
                        on_click=exibInfo, help="Verifique as informações registradas durante esta sessão de uso do aplicativo.")
        colHoliday.button(label='Feriados', use_container_width=True, icon="📅", 
                          on_click=exibHoliday, help="Verifique os feriados dos últimos anos.")
        colClear.button(label='Limpeza', use_container_width=True, icon="🧹", 
                        on_click=zeraWidget, help="Limpe os dados constantes da tela, exceto a data inicial.")
    with st.expander(label='Sobre esta aplicação', expanded=False, icon='📌'):
        textHelp = """
        Esta aplicação permite calcular prazos em dias corridos ou dias úteis. Parte de data data e números de dias
        de interesse do usuário. No caso do período em dias corridos, entram sábados, domingos e feriados, desde que 
        nenhum deles esteja no início ou término da contagem. Já na contagem em dias úteis, sábados, domingos e feriados
        não entram, estejam no meio ou nas datas extremas (começo ou final) da contagem.
        Esta ferramenta não é um aplicativo rigoroso ou oficial, especialmente porque não leva em consideração datas em que, 
        por diferentes motivos, não houver expediente público ou privado. 
        Mesmo em relação aos feriados nacionais, chama-se a atenção para o fato de que se baseiam em planilha disponível 
        na internet e copiada em 13 de maio de 2025 pelo desenvolvedor.                      
        """
        st.text(textHelp)

def configDbHol():
    newCol = ' # '
    dfHoliday[newCol] = [row + 1 for row in range(len(dfHoliday))]  
        
def defineLim():
    listDate = []
    nOnly = len(dateOnly)
    dateMinStr = dateOnly[0]
    dateMaxStr = dateOnly[nOnly-1]
    listDate.append(dateMinStr)
    listDate.append(dateMaxStr)
    for dateStr in [dateMinStr, dateMaxStr]:
        dateSplit = [int(dat) for dat in list(reversed(dateStr.split('/')))]
        dateObj = date(dateSplit[0], dateSplit[1], dateSplit[2])
        listDate.append(dateObj)
    return listDate
    
if __name__ == '__main__':
    st.subheader("Tela de entrada de dados 📆")
    global dictKeys, listKeys, timeDay
    global months, weeks
    global dateMin, dateMax
    global dfHoliday
    global dateOnly, holOnly
    keyNames = {'calendar': date.today(), 
                'days': 0, 
                'plus': 0, 
                'current': "", 
                'useful': "", 
                'sldata': 0}
    listKeys = list(keyNames.keys())
    timeDay = float(0.50)    
    months = {1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril', 5:'maio', 6: 'junho', 
              7: 'julho', 8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'}
    weeks = {6: 'domingo', 0: 'segunda-feira', 1: 'terça-feira', 
             2: 'quarta-feira', 3: 'quinta-feira', 4: 'sexta-feira', 
             5: 'sábado'}
    dfHoliday = readHoliday()
    dfHoliday = dfHoliday.dropna()
    dateOnly = dfHoliday['Data']
    holOnly = dfHoliday['Feriado']
    configDbHol()
    if 'dateonly' not in st.session_state:
        st.session_state.dateonly = dateOnly
    if 'holonly' not in st.session_state:
        st.session_state.holonly = holOnly
    dateMinStr, dateMaxStr, dateMin, dateMax = defineLim()
    if 'dateminstr' not in st.session_state:
        st.session_state.dateminstr = dateMinStr
    if 'datemaxstr' not in st.session_state:
        st.session_state.datemaxstr = dateMaxStr
    if 'acesso' not in st.session_state:
        st.session_state['acesso'] = []
    if 'files' not in st.session_state:
        st.session_state['files'] = [] 
    iniFinally(0)
    main()
