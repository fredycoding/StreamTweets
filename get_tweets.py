### En este ejemplo se muestra como se puede utilizar el API de Twitter para recibir tweets en tiempo real.
### Leemos los 100 primeros tweets en streaming
### Realizado por Fredy Diaz

import tweepy
import pandas as pd


df = pd.DataFrame(columns=['Usuario', 'Nombre', 'Seguidores', 'Verificado', 'Texto', 'Fecha', 'Ubicación'])

# Aca se obtienen los datos de la api de Twitter
clave_usuario = '*****************'
secreto_usuario = '*******************'
token_acceso = '******************************'
token_acceso_secreto = '************************************'

usuario = []
nombre = []
seguidores = []
verificado = []
texto = []
fecha = []
ubicacion = []

# Subclass Stream to print IDs of Tweets received
class IDPrinter(tweepy.Stream):  
  
    contador = 0
    def on_status(self, status):
        
        if not status.truncated:
            
            text = status.text
        else:
            # If the tweet is truncated, only print the first 140 characters
            text = status.extended_tweet['full_text']



        if self.contador <= 100: 
          
            #print(status)
            usuario.append(status.user.screen_name)
            nombre.append(status.user.name)
            seguidores.append(status.user.followers_count)

            if status.user.verified:
               verificado.append(status.user.verified)
            else:
               verificado.append("")   

            texto.append(text)
            fecha.append(status.created_at)

            if status.user.location != None:            
                ubicacion.append(status.user.location)
            else:
                ubicacion.append('No especificado')    

            print(text)
            # Descomentar para visualizar en consola resultados
            """print(status.id)
            print(text)
            print(status.created_at)   
            print(status.user.screen_name)
        
            if status.user.location != None:
                print(status.user.location)"""  

            print("Contador: ", self.contador)    
            self.contador += 1 

        if self.contador == 100:
            print("Contador: ", self.contador)
            self.disconnect()
            df['Usuario'] = usuario
            df['Nombre'] = nombre
            df['Seguidores'] = seguidores
            df['Verificado'] = verificado
            df['Texto'] = texto
            df['Fecha'] = fecha
            df['Ubicación'] = ubicacion
            df.to_csv('tweets.csv', index=False)
            print(df)


# Initialize instance of the subclass
printer = IDPrinter( clave_usuario, secreto_usuario, token_acceso, token_acceso_secreto)

# Filter realtime Tweets by keyword
printer.filter(track=["Colombia"])
