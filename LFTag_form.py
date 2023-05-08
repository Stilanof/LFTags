import tkinter as tk
from tkinter import messagebox
import json 
from ttkbootstrap import Style,ttk
import git


# Configuración del proveedor
#terraform = terrascript.Terrascript()
#terraform += terrascript.provider.aws(region="us-east-1")

# Crear la ventana principal
ventana = tk.Tk()
#vapor
style = Style(theme='solar')
ventana.title("IMPLEMENTACIÓN AUTOMATIZADA DE LFTAGS AWS")
# obtener el ancho y alto de la pantalla
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()
# Calcular las coordenadas para posicionar la ventana en el centro
x = int((screen_width - ventana.winfo_reqwidth()) / 2.5)
y = int((screen_height - ventana.winfo_reqheight()) / 3)
# Establecer la geometría de la ventana en el centro
ventana.geometry(f"+{x}+{y}")
ventana.minsize(width=500,height=300)
ventana.maxsize(width=500, height=500)

respuestas=[]
def enviar_formulario():
    # mostrar mensaje final
    messagebox.showinfo("Formulario enviado", "Tu solicitud ha sido enviada a revisión del Gobierno de Datos!")
    # cerrar ventana del formulario
    ventana.destroy()
    exportar_respuestas(respuestas)
    push(respuestas)
    print(respuestas)

def push(respuestas):
    repo = git.Repo('C:\\Users\\susana.tilano.flores\\Desktop\\proyecto_practica\\LFTags-1') 
    repo.git.add('.')
    repo.git.commit('-m', 'Commit automático'+respuestas[0]) 
    origin = repo.remote(name='origin')
    origin.push()

def exportar_respuestas(respuestas):
    with open("respuestas.py", "w", encoding="utf-8") as f:
       json.dump(respuestas, f, ensure_ascii=False)

    #RECURSOS-TERRAFORM
    if respuestas[1] == "Creación":
        # Define las variables
        prefix = respuestas[2]
        nombre_tag = respuestas[3]
        tag=prefix+nombre_tag
        valores_tag = respuestas[4] 
        print(valores_tag)
        #valores_tag = valores_tag.split(",")
        #print(valores_tag)
        
        resource_type= "aws_lakeformation_lf_tag"
        # definir plantilla del recurso
        resource_template = """
resource "{3}" "{0}" {{
key = "{1}"
values = [{2}]
}}
        """.format(tag, tag, valores_tag, resource_type)
        # verificar si el recurso ya existe
        existing_resource = False
        with open("mainLFTag.tf", "r") as f:
            contents = f.read()
            if tag in contents and resource_type in contents:
                existing_resource = True
        # si el recurso no existe, añadirlo al archivo
        if not existing_resource:
            with open("mainLFTag.tf", "a") as f:
                f.write(resource_template)

    else:
        if (respuestas[2] == "Recurso") and (respuestas[3] == "Tabla"):
            # Define las variables
            db_name = respuestas[4]
            tabla = respuestas[5]
            valor_tag = respuestas[6]
            clave_tag = respuestas[7]
            resource_type= "aws_lakeformation_resource_lf_tags"
            resource_name= db_name+tabla+clave_tag+valor_tag
            # definir plantilla del recurso
            resource_template = """
resource "{0}" "{1}" {{
    table {{
        database_name = "{2}"
        name="{3}"
}}
    lf_tag {{
        key   = "{4}"
        value = "{5}"
    }}
    }}
            """.format(resource_type, resource_name, db_name, tabla, valor_tag, clave_tag)
            # verificar si el recurso ya existe
            existing_resource = False
            with open("mainLFTag.tf", "r") as f:
                contents = f.read()
                if resource_name in contents and resource_type in contents:
                    existing_resource = True
            # si el recurso no existe, añadirlo al archivo
            if not existing_resource:
                with open("mainLFTag.tf", "a") as f:
                    f.write(resource_template)

        elif (respuestas[2] == "Recurso") and (respuestas[3] == "Base de Datos"):
                db = respuestas[4]
                clave_tag = respuestas[5]
                valor_tag = respuestas[6]
                resource_type= "aws_lakeformation_resource_lf_tags"
                resource_name= db+clave_tag+valor_tag
                # definir plantilla del recurso
                resource_template = """
resource "{0}" "{1}" {{
    database {{
        name="{2}"
    }}
    lf_tag {{
        key   = "{3}"
        value = "{4}"
    }}
    }}
                """.format(resource_type, resource_name, db, clave_tag, valor_tag)
                # verificar si el recurso ya existe
                existing_resource = False
                with open("mainLFTag.tf", "r") as f:
                    contents = f.read()
                    if resource_name in contents and resource_type in contents:
                        existing_resource = True
                # si el recurso no existe, añadirlo al archivo
                if not existing_resource:
                    with open("mainLFTag.tf", "a") as f:
                        f.write(resource_template)

        elif (respuestas[2] == "Rol/cuenta") and (respuestas[3] == "Rol"):
                rol_nombre = respuestas[4]
                arn_rol = respuestas[5]
                valor_tag = respuestas[7]
                clave_tag = respuestas[6]
                resource_type= "aws_lakeformation_permissions"
                resource_name1= rol_nombre+clave_tag+valor_tag+"db"
                resource_name2= rol_nombre+clave_tag+valor_tag+"t"
                # definir plantilla del recurso
                resource_template = """
resource "{0}" "{1}" {{
    principal   = {2}
    permissions = ["DESCRIBE"]
    lf_tag_policy {{
        resource_type = "DATABASE"
        expression {{
        key    = {3}
        values = {4}
    }}
    }}
    }}
resource "{0}" "{5}" {{
    principal   = {2}
    permissions = ["SELECT", "DESCRIBE"]
        lf_tag_policy {{
            resource_type = "TABLE"
            expression {{
            key    = {3}
            values = {4}
    }}
    }}
    }}
                """.format(resource_type, resource_name1, arn_rol, clave_tag,valor_tag,resource_name2)
                # verificar si el recurso ya existe
                existing_resource = False
                with open("mainLFTag.tf", "r") as f:
                    contents = f.read()
                    if resource_name2 in contents and resource_type in contents:
                        existing_resource = True
                # si el recurso no existe, añadirlo al archivo
                if not existing_resource:
                    with open("mainLFTag.tf", "a") as f:
                        f.write(resource_template)

        elif (respuestas[2] == "Rol/cuenta") and (respuestas[3] == "Cuenta"):
                cuenta = respuestas[4]
                valor_tag = respuestas[6]
                clave_tag = respuestas[5]
                resource_type= "aws_lakeformation_permissions"
                resource_name1= cuenta+clave_tag+valor_tag+"db"
                resource_name2= cuenta+clave_tag+valor_tag+"t"
                # definir plantilla del recurso
                resource_template = """
resource "{0}" "{1}" {{
    principal   = {2}
    permissions = ["DESCRIBE","SELECT","ALTER", "DELETE", "DROP", "INSERT"] 
    permissions_with_grant_option = ["DESCRIBE","SELECT","ALTER", "DELETE", "DROP", "INSERT"] 
        lf_tag_policy {{
            resource_type = "DATABASE"
            expression {{
            key    = {3}
            values = {4}
    }}
    }}
    }}
resource "{0}" "{5}" {{
    principal   = {2}
    permissions = ["DESCRIBE","SELECT","ALTER", "DELETE", "DROP", "INSERT"] 
    permissions_with_grant_option = ["DESCRIBE","SELECT","ALTER", "DELETE", "DROP", "INSERT"] 
        lf_tag_policy {{
            resource_type = "TABLE"
            expression {{
            key    = {3}
            values = {4}
}}
}}
}}
                """.format(resource_type, resource_name1, cuenta, clave_tag, valor_tag, resource_name2)
                # verificar si el recurso ya existe
                existing_resource = False
                with open("mainLFTag.tf", "r") as f:
                    contents = f.read()
                    if resource_name2 in contents and resource_type in contents:
                        existing_resource = True
                # si el recurso no existe, añadirlo al archivo
                if not existing_resource:
                    with open("mainLFTag.tf", "a") as f:
                        f.write(resource_template)

#FORMULARIO
def enviar_seccion1():
    print("¿Cuál es tu usuario de red?:", usuario_var.get())
    print("¿Qué proceso deseas realizar?:", proceso.get())
    if proceso.get() == 'Creación':
        seccion2.pack()
    else:
        seccion3.pack(fill=tk.BOTH, expand=True)
    seccion1.pack_forget()
    respuestas.extend([usuario_var.get(),proceso.get()])

def enviar_creacion():
    print("Tipo de etiqueta a crear:", etiqueta.get())
    print("Clave de etiqueta:", clave_etiqueta_var.get())
    print("Valores posibles de etiqueta:", valores_etiqueta_var.get())
    print("Justificación:", justificacion_var.get())
    seccion2.pack_forget()
    respuestas.extend([etiqueta.get(),clave_etiqueta_var.get(),valores_etiqueta_var.get(),justificacion_var.get()])
    enviar_formulario()

def enviar_seccion3():
    print("¿Solicita asignación a?:", tipo_asignacion.get())
    if tipo_asignacion.get() == "Recurso":
        seccion4.pack(fill=tk.BOTH, expand=True)
    else:
        seccion5.pack(fill=tk.BOTH, expand=True)
    seccion3.pack_forget()
    respuestas.extend([tipo_asignacion.get()])
   
def enviar_seccion4():
    print("Nivel de estructura de datos a asignar:", nivel_asignacion.get())
    if nivel_asignacion.get() == "Base de Datos":
        seccion6.pack(fill=tk.BOTH, expand=True)
    else:
        seccion7.pack(fill=tk.BOTH, expand=True)
    seccion4.pack_forget()
    respuestas.extend([nivel_asignacion.get()])

def enviar_seccion5():
    print("Asignación a:", user_asignacion.get())
    if user_asignacion.get() == "Rol":
        seccion8.pack(fill=tk.BOTH, expand=True)
    else:
        seccion9.pack(fill=tk.BOTH, expand=True)
    seccion5.pack_forget()
    respuestas.extend([user_asignacion.get()])

def enviar_seccion6():
    print("Nombre de base de datos a asignar:", db_var.get())
    print("Valor etiqueta a asignar:", valor_etiqueta_var6.get())
    print("Clave etiqueta a asignar:", clave_var6.get())
    seccion6.pack_forget()
    respuestas.extend([db_var.get(),valor_etiqueta_var6.get(),clave_var6.get()])
    enviar_formulario()

def enviar_seccion7():
    print("Nombre de base de datos madre de la tabla a asignar:", db_nombre_var.get())
    print("Nombre de tabla a asignar:", tabla_var.get())
    print("Clave etiqueta a asignar:", clave_var7.get())
    print("Valor etiqueta a asignar:", valor_etiqueta_var7.get())
    seccion7.pack_forget()
    respuestas.extend([db_nombre_var.get(),tabla_var.get(),clave_var7.get(),valor_etiqueta_var7.get()])
    enviar_formulario()

def enviar_seccion8():
    print("Nombre rol a asignar:", rol_nombre_var.get())
    print("ARN del rol a asignar:", arn_rol_var.get())
    print("Valor etiqueta a asignar:", valor_etiqueta_var8.get())
    print("Clave etiqueta a asignar:", clave_var8.get())
    seccion8.pack_forget()
    respuestas.extend([rol_nombre_var.get(),arn_rol_var.get(),clave_var8.get(),valor_etiqueta_var8.get()])
    enviar_formulario()

def enviar_seccion9():
    print("Número cuenta a asignar:", cuenta_var.get())
    print("Valor etiqueta a asignar:", valor_etiqueta_var9.get())
    print("Clave etiqueta a asignar:", clave_var9.get())
    seccion9.pack_forget()
    respuestas.extend([cuenta_var.get(),clave_var9.get(),valor_etiqueta_var9.get()])
    enviar_formulario()

# Crear los widgets del formulario
#SECCION1
seccion1 = tk.Frame(ventana)
#Pregunta1
usuario_var= tk.StringVar()
usuario= tk.Label(seccion1, text="¿Cuál es tu usuario de red?",font=("Arial", 14)).pack(side="top")
usuario = tk.Entry(seccion1,textvariable=usuario_var,font=("Arial")).pack(side="top") #entrada texto
#Pregunta2
proceso= tk.Label(seccion1, text="¿Qué proceso deseas realizar?",font=("Arial", 14)).pack()
opciones_proceso = ['Creación', 'Asignación']
proceso = tk.StringVar()
elegir_proceso = tk.OptionMenu(seccion1, proceso, *opciones_proceso).pack()
# Crear botón para avanzar a la siguiente sección
boton_avanzar = tk.Button(seccion1, text="Siguiente",font=("Arial"), command=enviar_seccion1).pack()

#SECCION2
seccion2 = tk.Frame(ventana)
#Pregunta3.1
etiqueta= tk.Label(seccion2, text="Tipo de etiqueta a crear",font=("Arial", 14)).pack()
tipo_etiqueta=['bus', 'seg','tec']
etiqueta = tk.StringVar()
elegir_etiqueta = tk.OptionMenu(seccion2, etiqueta, *tipo_etiqueta).pack()
#Pregunta3.2
clave_etiqueta_var=tk.StringVar()
clave_etiqueta = tk.Label(seccion2, text="Clave de etiqueta",font=("Arial", 14)).pack()
clave_etiqueta = tk.Entry(seccion2,textvariable=clave_etiqueta_var,font=("Arial")).pack()
#Pregunta3.3
valores_etiqueta_var=tk.StringVar()
valores_etiqueta = tk.Label(seccion2, text="Valores posibles de etiqueta (separados por comas)",font=("Arial", 14)).pack()
valores_etiqueta = tk.Entry(seccion2,textvariable=valores_etiqueta_var,font=("Arial")).pack()
#Pregunta3.4
justificacion_var=tk.StringVar()
justificacion = tk.Label(seccion2, text="Justificación: ¿Por qué es ncesaria esta etiqueta?",font=("Arial", 14)).pack()
justificacion = tk.Entry(seccion2,textvariable=justificacion_var,font=("Arial")).pack()
# Crear botón para avanzar a la siguiente sección
boton_enviar_creacion = tk.Button(seccion2, text="Enviar a crear etiqueta", command=enviar_creacion,font=("Arial")).pack()
seccion2.pack_forget()

#SECCION3
seccion3 = tk.Frame(ventana)
# Pregunta4
tipo_asignacion= tk.Label(seccion3, text="¿Solicita asignación a?",font=("Arial", 14)).pack()
tipo=['Recurso', 'Rol/cuenta']
tipo_asignacion = tk.StringVar()
elegir_tipo = tk.OptionMenu(seccion3, tipo_asignacion, *tipo).pack()
# Crear botón para avanzar a la siguiente sección
boton_avanzar = tk.Button(seccion3, text="Siguiente", command=enviar_seccion3,font=("Arial")).pack()
seccion3.pack_forget()

#SECCION4
seccion4 = tk.Frame(ventana)
# Pregunta5
nivel_asignacion= tk.Label(seccion4, text="¿A qué nivel de estructura de datos se realizará la asignación?",font=("Arial", 14)).pack()
nivel=['Base de Datos', 'Tabla']
nivel_asignacion = tk.StringVar()
elegir_nivel = tk.OptionMenu(seccion4, nivel_asignacion, *nivel).pack()
# Crear botón para avanzar a la siguiente sección
boton_avanzar = tk.Button(seccion4, text="Siguiente", command=enviar_seccion4,font=("Arial")).pack()
seccion4.pack_forget()

#SECCION5
seccion5 = tk.Frame(ventana)
# Pregunta6
user_asignacion= tk.Label(seccion5, text="¿Solicita asignación a?",font=("Arial", 14)).pack()
user=['Rol', 'Cuenta']
user_asignacion = tk.StringVar()
elegir_user = tk.OptionMenu(seccion5, user_asignacion, *user).pack()
# Crear botón para avanzar a la siguiente sección
boton_avanzar = tk.Button(seccion5, text="Siguiente", command=enviar_seccion5,font=("Arial")).pack()
seccion5.pack_forget()

#SECCION6
seccion6 = tk.Frame(ventana)
#Pregunta7
db_var=tk.StringVar()
db= tk.Label(seccion6, text="¿Nombre de base de datos a asignar?",font=("Arial", 14)).pack()
db= tk.Entry(seccion6, textvariable= db_var,font=("Arial")).pack() #entrada texto
#Pregunta8
clave_var6=tk.StringVar()
clave= tk.Label(seccion6, text="Clave etiqueta a asignar",font=("Arial", 14)).pack()
clave = tk.Entry(seccion6, textvariable=clave_var6,font=("Arial")).pack() #entrada texto
#Pregunta9
valor_etiqueta_var6=tk.StringVar()
valor_etiqueta= tk.Label(seccion6, text="Valor etiqueta a asignar",font=("Arial", 14)).pack()
valor_etiqueta= tk.Entry(seccion6, textvariable=valor_etiqueta_var6,font=("Arial")).pack() #entrada texto
# Crear botón para avanzar a la siguiente sección
boton_avanzar = tk.Button(seccion6, text="Enviar solicitud", command=enviar_seccion6,font=("Arial")).pack()
seccion6.pack_forget()

#SECCION7
seccion7 = tk.Frame(ventana)
#Pregunta10
db_nombre_var=tk.StringVar()
db_nombre= tk.Label(seccion7, text="¿Nombre de base de datos madre de la tabla a asignar?",font=("Arial", 14)).pack()
db_nombre = tk.Entry(seccion7, textvariable=db_nombre_var,font=("Arial")).pack() #entrada texto
#Pregunta10
tabla_var=tk.StringVar()
tabla= tk.Label(seccion7, text="¿Nombre tabla a asignar?",font=("Arial", 14)).pack()
tabla = tk.Entry(seccion7, textvariable=tabla_var,font=("Arial")).pack() #entrada texto
#Pregunta12
valor_etiqueta_var7=tk.StringVar()
valor_etiqueta= tk.Label(seccion7, text="Valor etiqueta a asignar",font=("Arial", 14)).pack()
valor_etiqueta = tk.Entry(seccion7, textvariable=valor_etiqueta_var7,font=("Arial")).pack() #entrada texto
#Pregunta13
clave_var7=tk.StringVar()
clave= tk.Label(seccion7, text="Clave etiqueta a asignar",font=("Arial", 14)).pack()
clave = tk.Entry(seccion7, textvariable=clave_var7,font=("Arial")).pack() #entrada texto
# Crear botón para avanzar a la siguiente sección
boton_avanzar = tk.Button(seccion7, text="Enviar solicitud", command=enviar_seccion7,font=("Arial")).pack()
seccion7.pack_forget()

#SECCION8
seccion8 = tk.Frame(ventana)
#Pregunta14
rol_nombre_var=tk.StringVar()
rol_nombre= tk.Label(seccion8, text="¿Nombre rol a asignar?",font=("Arial", 14)).pack()
rol_nombre = tk.Entry(seccion8, textvariable=rol_nombre_var,font=("Arial")).pack() #entrada texto
#Pregunta15
arn_rol_var=tk.StringVar()
arn_rol= tk.Label(seccion8, text="¿ARN del rol?",font=("Arial", 14)).pack()
arn_rol = tk.Entry(seccion8, textvariable=arn_rol_var,font=("Arial")).pack() #entrada texto
#Pregunta14
valor_etiqueta_var8=tk.StringVar()
valor_etiqueta= tk.Label(seccion8, text="Valor etiqueta a asignar",font=("Arial", 14)).pack()
valor_etiqueta = tk.Entry(seccion8, textvariable=valor_etiqueta_var8,font=("Arial")).pack() #entrada texto
#Pregunta17
clave_var8=tk.StringVar()
clave= tk.Label(seccion8, text="Clave etiqueta a asignar",font=("Arial", 14)).pack()
clave = tk.Entry(seccion8, textvariable=clave_var8,font=("Arial")).pack() #entrada texto
# Crear botón para avanzar a la siguiente sección
boton_avanzar = tk.Button(seccion8, text="Enviar solicitud", command=enviar_seccion8,font=("Arial")).pack()
seccion8.pack_forget()

#SECCION9
seccion9 = tk.Frame(ventana)
#Pregunta18
cuenta_var=tk.StringVar()
cuenta= tk.Label(seccion9, text="Número cuenta a asignar",font=("Arial", 14)).pack()
cuenta = tk.Entry(seccion9, textvariable=cuenta_var,font=("Arial")).pack() #entrada texto
#Pregunta19
valor_etiqueta_var9=tk.StringVar()
valor_etiqueta= tk.Label(seccion9, text="Valor etiqueta a asignar",font=("Arial", 14)).pack()
valor_etiqueta = tk.Entry(seccion9, textvariable=valor_etiqueta_var9,font=("Arial")).pack() #entrada texto
#Pregunta20
clave_var9=tk.StringVar()
clave= tk.Label(seccion9, text="Clave etiqueta a asignar",font=("Arial", 14)).pack()
clave = tk.Entry(seccion9, textvariable=clave_var9,font=("Arial")).pack() #entrada texto
# Crear botón para avanzar a la siguiente sección
boton_avanzar = tk.Button(seccion9, text="Enviar solicitud", command=enviar_seccion9,font=("Arial")).pack()
seccion9.pack_forget()

# Mostrar la ventana
seccion1.pack(fill=tk.BOTH, expand=True)
ventana.mainloop()


