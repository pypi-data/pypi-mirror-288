# -*- coding: utf-8 -*-
"""
    pybde: A module to access Database Statistics from Mauro Borges Institute (IMB) 
    (c) 2024 Bernard Silva de Oliveira [bernard.oliveira@goias.gov.br]

"""

import requests
import json


ulrMain = 'http://painelmunicipal.imb.go.gov.br/visao/'
parameters = {
            "variableDescribe": 'variavel.php?formatado=0&json=1&codigovariavel=',
            "unidadeMedida": "unidade.php?formatado=0&json=1&codigounidade=",
            "localidades": 'localidade.php?formatado=0&json=1&codigolocalidade=&codigoibge=',
            "dados": '''dados.php?parametros=0|1|{locbde}|{codibge}|{codvarbde}|{anoinicial}|
                                {anofinal}|{ultimoano}|{periodo}|{seriehistorica}|{auxvar}|{auxund}|{auxvarfnt}|
                                {auxfnt}|{auxvarnota}|{auxnota}|'''
        }

class BDEquery:

    # Get variables datasets from databases statistics
    def getVariables(self, codvar:int=None) -> dict:
        """
            Access variables (codes)  in Statistics Database in IMB
            |
            |   Parameters
            |   ----------
            |   codvar: int, optional
            |       Code of the variable in the BDE.
            |
            |   Returns
            |   -------
            |   data: dict
            |
            |   Examples
            |   --------
            |
            |   import pybdedata.query as bde
            |
            |   bdeObj = bde.BDEquery()
            |
            |   bdeObj.getVariables() -> Get all variables code in the BDE.
            |   bdeObj.getVariables(codvar=1) -> Get information variable the of code 1 in the BDE
        """
        if codvar is None:
            url = ulrMain + parameters['variableDescribe']
        else:
            url = ulrMain + parameters['variableDescribe'] + str(codvar)

        # Information requests
        data = requests.get(url)
        data = data.text
        data = json.loads(data)

        return data

    # Get units datasets from databases statistics
    def getUnits(self, codund:int=None) -> dict:
        """
            Access units from data  in Statistics Database in IMB
            |
            |   Parameters
            |   ----------
            |   codund: int, optional
            |       Internal code of the units of measurement in the BDE.
            |
            |   Returns
            |   -------
            |   data: dict
            |
            |   Examples
            |   --------
            |
            |   import pybdedata.query as bde 
            |
            |   bdeObj = bde.BDEquery()
            |
            |   bdeObj.getUnits() -> Access all units of measurement variables in the BDE.
            |   bdeObj.getUnits(codund=1) -> Get information measurement variable the of code 1 in the BDE.
        """
        if codund is None:
            url = ulrMain + parameters['unidadeMedida']
        else:
            url = ulrMain + parameters['unidadeMedida'] + str(codund)

        # Requisicao da informacao
        data = requests.get(url)
        data = data.text
        data = json.loads(data)

        return data

    # Get locations datasets from databases statistics
    @property
    def getLocations(self) -> dict:
        """
            Access locations (municipalities) in Statistics Database - IMB
            |
            |   Returns
            |   -------
            |   data: dict
            |   import pybdedata.query as bde 
            |
            |   bdeObj = bde.BDEquery()
            |
            |   bdeObj.getLocations

        """
        # Request information
        url = ulrMain + parameters['localidades']
        data = requests.get(url)
        data = data.text
        data = json.loads(data)

        return data

    # Get datas from databases statistics
    def getdata(self, codvarbde:str, **kwargs) -> dict:

        """

            |   Access data in Statistics Database - IMB
            |
            |   Parameters
            |   ----------
            |   codvarbde: str
            |       Variable code of the BDE. To acquire the code of the variables in the BDE, use the function getVariables of the pybde.
            |       To query multiples variables, use semicolon in between codes.
            |
            |   codibge: str, optional
            |       IBGE locality code, but use 'T' to show all municipalities. The value 'T' is default.
            |
            |   initialyear:str, optional
            |       Initial year you want to view the information.
            |
            |   finalyear:str, optional
            |       Final year for which information is to be viewed.
            |
            |   timeseries:int, optional
            |       Number of year of the values of the variable, the starting point being the last year
            |
            |   Returns
            |   -------
            |   data: dict
            |
            |   Examples
            |   --------
            |   import pybdedata.query as bde
            |
            |   bdeObj = bde.BDEquery()
            |
            |   bdeObj.getdata(codvarbde='1;2',codibge='5208707') -> Access data from Goiãnia City.
            |   bdeObj.getdata(codvarbde='15',codibge='5208707',timeseries=10) -> Access data from Goiãnia City in 10 years.
            |   bdeObj.getdata(codvarbde='15',codibge='5208707',initialyear=2013,finalyear=2019) -> Access data from Goiania City in between 2013 and 2019.
            |   bdeObj.getdata(codvarbde='15',codibge='5208707',initialyear=2013,finalyear=2019,timeseries=5) -> Access data from Goiania City of the last 5 years in between 2013 and 2019.



        """

        #Parâmetros da API
        param = {
            "codibge": 'T',
            "initialyear": None,
            "finalyear": None,
            "timeseries": None,
        }

        for kp in kwargs.keys():
            try:param[kp] = kwargs[kp]
            except:continue

        if (param['initialyear'] is not None) and (param['initialyear'] is not None):
            ultimoano = 0
            periodo = None
        else:
            ultimoano = 1
            periodo = 1


        # URL dos dados
        url = ulrMain + parameters['dados']
        url = url.format(locbde=None, codibge=param['codibge'], codvarbde=codvarbde,
                         anoinicial=param['initialyear'],anofinal=param['finalyear'],
                         ultimoano=ultimoano, periodo=periodo,seriehistorica=param["timeseries"],
                         auxvar=1, auxund=1,auxvarfnt=1, auxfnt=1,auxvarnota=1, auxnota=1)

        # Requisicao da informacao
        # Initial Time request
        data = requests.get(url)
        data = data.text
        data = json.loads(data)
        listData = []
        # End Time request
        # Initial Time Format
        for row in data:
            dicData = {}
            for j in row.keys():

                if j == 'anos':
                    fulldic = dict()
                    dataYear = row[j]
                    count = 1

                    for k in dataYear.items():
                        new = dicData.copy()
                        new['ano'] = k[0]
                        new['valor'] = k[1]
                        fulldic[str(count)] = new
                        count += 1

                    for i in fulldic.values():
                        listData.append(i)

                else:
                    dicData[j] = row[j]

        # End Time format
        data = listData
        return data