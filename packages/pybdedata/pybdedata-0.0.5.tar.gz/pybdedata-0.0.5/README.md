## pybdedata - a module to access IMB data



This is a module to access data from IMB (Mauro Borges Statistic and Socioeconomic Institute). Such information
can be found at https://painelmunicipal.imb.go.gov.br/ by entering variable code, IBGE code or location IMB code.

Install: pip install pybdedata 

 Usage:

      #Import modules pybde and pandas
      import pybdedata.query as bde 
      import pandas as pd
      
      #Object instance
      bdeObj = bde.BDEquery()
      
      #Variables information from Statistics Database of IMB 
      variables = pd.DataFrame(data=bdeObj.getVariables())
      
      #Variables units information from Statistics Database of IMB
      units = pd.DataFrame(data=bdeObj.getUnits())
      
      #Municipalites information from Statistics Database of IMB
      location = pd.DataFrame(data=bdeObj.getLocations)
      
      #Access data from Statistics Database of IMB in variables code of 1 and 2.
      data = pd.DataFrame(data=bdeObj.getdata(codvarbde='1;2'))