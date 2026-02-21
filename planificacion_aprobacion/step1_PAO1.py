
import pandas as pd
import glob
from complete_data_to_model import complete_data_to_model, limpieza_df_con_gpa_socioeconomico_interes
from inference import get_model_available, get_data_academic_risk, predict_academic_risk
import numpy as np
from dotenv import load_dotenv
load_dotenv()
import os

os.add_dll_directory('C:\\Program Files\\IBM\\SQLLIB\\BIN')
# conectar a la base de datos IBM Db2
import ibm_db


conn_str = 'DATABASE=' + os.getenv('DATABASE') + ';HOSTNAME=192.168.254.53;PORT=' + os.getenv('PORT') + ';PROTOCOL=TCPIP;UID=' + os.getenv('USERNAME_DB') + ';PWD=' + os.getenv('PASSWORD_DB') + ';'
print(conn_str)
conn = ibm_db.connect(conn_str, '', '')
# conn = ibm_db.connect(os.getenv('DATABASE'), os.getenv('USERNAME_DB'), os.getenv('PASSWORD_DB')) # os.getenv('HOSTNAME'), os.getenv('PORT')

if conn:
    print("Conexión exitosa")
else:
    print("Error al conectar")


def get_data_from_query(sql_str):
    stmt_select  = ibm_db.exec_immediate(conn, sql_str)
    
    # Fetch all rows
    data_list = []
    result = ibm_db.fetch_assoc(stmt_select)
    while result:
        # print(result)
        data_list.append(result)
        result = ibm_db.fetch_assoc(stmt_select)
    return data_list


modelo, label_encoders, feature_info = get_model_available()

def make_analysis(list_matricula, cod_materia):
    mi_df, list_student_off = get_data_academic_risk(list_matricula, cod_materia, label_encoders)
    if mi_df.empty:
        print("⚠️ No se encontraron datos para los estudiantes proporcionados. Asegúrate de que las matrículas sean correctas y que los estudiantes hayan tomado la materia objetivo.")
        return {}, mi_df, {}, list_student_off

    print("Debe coinicidir la cantidad:",mi_df.shape[0] == len(list_matricula))
    if mi_df.shape[0] != len(list_matricula):
        print("⚠️ Advertencia: Algunos estudiantes no tienen datos completos para el análisis.")

    results = predict_academic_risk(modelo, feature_info, mi_df)

    stats = results['statistics']
    # print(f"📊 {stats['pred_aprobar']} estudiantes aprobarán ({stats['pct_aprobar']:.2f}%)")
    
    return results, mi_df, stats, list_student_off

# ### Datos de historico completo desde 2020 a 2025 2S
list_names_files = glob.glob("../data/riesgo_academico/all_*")
df_materias = pd.read_csv("../data/riesgo_academico/dificultad_materia.csv")


df_complete = pd.DataFrame()

for file in list_names_files:
    if not "2026" in file:
        print("file", file)
        split_file = file.split("_")
        termino = split_file[-1].split(".")[0]
        if termino == "3S":
            continue
        
        df = pd.read_csv(file)

        df["anio"] = split_file[-2]
        df["termino"] = termino
        if not("MATERIA" in df.keys()):
            df = pd.merge(df, df_materias[["CODIGOMATERIA", "MATERIA"]], left_on="COD_MATERIA_ACAD_MO", right_on="CODIGOMATERIA")

        df_complete = pd.concat([df_complete, df], ignore_index=True)

df_complete["COD_ESTUDIANTE"] = df_complete["COD_ESTUDIANTE"].astype(str)
print(df_complete.shape)

# group by anio and termino
df_complete.groupby(["anio", "termino"]).size() 


# #### Carrera con datos completos de estudiantes
df_carreras_estudiantes = pd.read_csv("../data/riesgo_academico/carreras_estudiantes.csv")
df_carreras_estudiantes["CODESTUDIANTE"] = df_carreras_estudiantes["CODESTUDIANTE"].astype(str)
df_carreras_estudiantes["CODESTUDIANTE"] = df_carreras_estudiantes["CODESTUDIANTE"].str.strip()

# # agrupa los CODESTUDIANTE y CARRERA y cuenta la cantidad de ocurrencias. Con CODESTUDIANTE y CARRERA como columnas separadas
df_carreras_estudiantes_new = df_carreras_estudiantes.groupby(['CODESTUDIANTE', 'CARRERA', 'ANIO']).size().reset_index(name='CANTIDAD').copy()


# Obtener el año máximo por cada combinación de CODESTUDIANTE y CARRERA
df_carreras_estudiantes_max_anio = df_carreras_estudiantes_new.loc[
    df_carreras_estudiantes_new.groupby(['CODESTUDIANTE', 'CARRERA'])['ANIO'].idxmax()
][['CODESTUDIANTE', 'CARRERA', 'ANIO']].reset_index(drop=True)


# Conservar solo una fila por CODESTUDIANTE con el ANIO máximo
df_carreras_estudiantes_max_anio = (
    df_carreras_estudiantes_max_anio
    .sort_values('ANIO', ascending=False)
    .groupby('CODESTUDIANTE', as_index=False)
    .first()
)


df_carreras_estudiantes_max_anio["CODESTUDIANTE"].value_counts()
df_carreras_estudiantes_max_anio[df_carreras_estudiantes_max_anio["CODESTUDIANTE"] == "201908803"]
df_complete.shape, df_carreras_estudiantes_max_anio.shape


# agregar a df_complete CARRERA desde df_carreras_estudiantes haciendo merge con COD_ESTUDIANTE de df_complete y CODESTUDIANTE de df_carreras_estudiantes
df_complete = pd.merge(df_complete, df_carreras_estudiantes_max_anio[['CODESTUDIANTE', 'CARRERA']], left_on='COD_ESTUDIANTE', right_on='CODESTUDIANTE', how='inner')
df_complete = df_complete.drop(columns=['CODESTUDIANTE'])


df_complete["termino_num"] = df_complete["termino"].map({"1S": 1, "2S": 2, "3S": 3})
df_complete['DIFICULTAD_MO'] = df_complete['DIFICULTAD_MO'].str.replace(',', '.').astype(float)
df_complete['PROM_MAT_REPROBADAS1'] = df_complete['PROM_MAT_REPROBADAS1'].str.replace(',', '.').astype(float)


#### GPA
list_gpa_gemeral = glob.glob("../data/riesgo_academico/gpa_*S.csv")

df_gpa_general = pd.DataFrame()
for file_gpa_gen in list_gpa_gemeral:
    print(file_gpa_gen)
    df_tmp = pd.read_csv(file_gpa_gen)
    df_gpa_general = pd.concat([df_gpa_general, df_tmp], ignore_index=True)


df_gpa_general['COD_ESTUDIANTE'] = df_gpa_general['COD_ESTUDIANTE'].astype(str).str.strip()
df_gpa_general = df_gpa_general.drop_duplicates()


#### Socioeconomico del estudiante objetivo
df_socioeconomico = pd.read_csv("../data/riesgo_academico/socioeconomico_17944.csv")
df_socioeconomico['CODESTUDIANTE'] = df_socioeconomico['CODESTUDIANTE'].astype(str).str.strip()


df_socioeconomico["GASTOS_RUBRO"] = ((df_socioeconomico["ALIMENTACION"] + df_socioeconomico["TRANSPORTE"] + df_socioeconomico["SERVICIOS"] +
  df_socioeconomico['ARRIENDO'] + df_socioeconomico['ALICUOTAS'] + df_socioeconomico['VESTIMENTA'] + df_socioeconomico['SALUD'] + df_socioeconomico['EDUCACION'] +
  df_socioeconomico['TARJETACREDITO'] + df_socioeconomico['ENTRETENIMIENTO'] + df_socioeconomico['OTROS']) / df_socioeconomico["NUMEROSFAMILIARES"]).round(2)


# eliminar duplicados de CODESTUDIANTE dejando la primera ocurrencia
df_socioeconomico = df_socioeconomico.drop_duplicates(subset=['CODESTUDIANTE'], keep='first')

### Estudiantes que estan viendo actualmente la materia objetivo
dir_estudiantes_viendo = '../database/planificacion_aprobacion/estudiantes_actualmente_viendo.sql'

### Prerequisitos necesarios de la materia objetivo
dir_pre_co_requisitos = '../database/planificacion_aprobacion\\corequisito_prerequisito_materias.sql'





anio_base, termino_base = 2025, 2  # Periodo actual
# cod_materia_objetivo = "TLMG1036" 

df_new_semester = pd.read_csv("../data/riesgo_academico/all_2026_1S.csv")
list_materias_ready = list(df_new_semester["COD_MATERIA_ACAD_MO"].unique())

df_materias_xslx = pd.read_excel('../data/riesgo_academico/saved/TODOESPOL.xlsx')
list_df_materias = list(df_materias_xslx["CodigoMateria"].unique())
list_cod_error = []
for cod_materia_objetivo in list_df_materias:
    if cod_materia_objetivo in list_materias_ready:
        print(f"⚠️ Materia {cod_materia_objetivo} está en la lista de materias objetivo. Saltando este ciclo.")
        continue

    try:
        with open(dir_estudiantes_viendo, 'r', encoding='utf-8') as file:
            sql_estudiantes_viendo_base = file.read()

        sql_estudiantes_viendo = sql_estudiantes_viendo_base.split("------------")[0]
        sql_estudiantes_viendo = sql_estudiantes_viendo.replace('\n', ' ')
        sql_estudiantes_viendo = sql_estudiantes_viendo.replace('TT', f"{termino_base}S")
        sql_estudiantes_viendo = sql_estudiantes_viendo.replace('AAAA', f"{anio_base}")
        sql_estudiantes_viendo = sql_estudiantes_viendo.replace('xxxxx', f"{cod_materia_objetivo}")

        # Fetch all rows
        data_list = get_data_from_query(sql_estudiantes_viendo)
        if len(data_list) == 0:
            print("⚠️ No se encontraron estudiantes actualmente viendo la materia objetivo", cod_materia_objetivo)
            print("+"*100)
            # stop run
            # list_cod_error.append(cod_materia_objetivo)
            df_estudiantes_viendo = pd.DataFrame(columns=["COD_ESTUDIANTE", "NOMBRE", "CARRERA", "COD_MATERIA_ACAD", "ANIO", "TERMINO", "VEZ_TOMADA"])
        else:
            df_estudiantes_viendo = pd.DataFrame(data_list)[["COD_ESTUDIANTE", "NOMBRE", "CARRERA", "COD_MATERIA_ACAD", "ANIO", "TERMINO", "VEZ_TOMADA"]].copy()

        # hacer antes el copy porque si no no sabe si es en el copy o en el original
        df_estudiantes_viendo["COD_MATERIA_ACAD"] = df_estudiantes_viendo["COD_MATERIA_ACAD"].astype(str)
        df_estudiantes_viendo["COD_MATERIA_ACAD"] = df_estudiantes_viendo["COD_MATERIA_ACAD"].str.strip() 
        print("Estudiantes viendo actualmente la materia objetivo", df_estudiantes_viendo.shape)

        # queries SQL parameters
        with open(dir_pre_co_requisitos, 'r', encoding='utf-8') as file:
            sql_pre_co_requisitos_base = file.read()

        sql_pre_co_requisitos = sql_pre_co_requisitos_base.split("------------")[0]
        sql_pre_co_requisitos = sql_pre_co_requisitos.replace('\n', ' ')
        sql_pre_co_requisitos = sql_pre_co_requisitos.replace('xxxxx', f"{cod_materia_objetivo}")

        # Fetch all rows
        data_list = get_data_from_query(sql_pre_co_requisitos)

        df_pre_requisito = pd.DataFrame(data_list)[["CARRERA", "NIVEL", "MATERIA_REQUISITO", "CODIGOMATERIA", "TIPO", "TIPOMATERIA", "MATERIA"]].copy()

        dic_terms = {
            "100II": 1,
            "200I": 2,
            "200II": 3,
            "300I": 4,
            "300II": 5,
            "400I": 6,
            "400II": 7,
            "500I": 8,
            "500II": 9
        }
        #min. terminos registrados de estudiantes que no hayan tomado la materia objetivo

        df_pre_requisito["NUM_MIN_TERMINOS"] = df_pre_requisito["NIVEL"].map(dic_terms)

        try:
            materia_objetivo = df_pre_requisito["MATERIA"].iloc[0]
            print("Materia objetivo:", materia_objetivo, "con codigo", cod_materia_objetivo)
        except IndexError:
            print("⚠️ No se encontraron prerrequisitos para la materia objetivo. Asumiendo que no tiene prerrequisitos.")
            materia_objetivo = "No tenemos en el nombre desde las prerequisitos, porque no tiene prerequisitos"

        df_pre_requisito_cp = df_pre_requisito.copy()
        df_pre_requisito = df_pre_requisito[df_pre_requisito["TIPO"] == "PR"]

        if df_pre_requisito.shape[0] == 0:
            print("⚠️ No se encontraron prerrequisitos para la materia", cod_materia_objetivo)
            print("Si no hay prerequisito, quiere decir que es de primera linea(por ahora). No se toma en cuenta.")
            # print("+"*100)
            # # stop run
            # list_cod_error.append(cod_materia_objetivo)
            # continue
        
        
        # *******************************************************************************************************************

        print(df_pre_requisito.shape)

        # ### Estudiantes de prerequisitos, cuales han aprobado para considerar en la planificacion
        lis_carreras_pre = df_pre_requisito["CARRERA"].unique().tolist()
        lis_cod_materias_pre = [i.strip() for i in df_pre_requisito["CODIGOMATERIA"].unique().tolist()]

        sql_estudiantes_viendo_pre = sql_estudiantes_viendo_base.split("------------")[0]
        sql_estudiantes_viendo_pre = sql_estudiantes_viendo_pre.replace('\n', ' ')
        sql_estudiantes_viendo_pre = sql_estudiantes_viendo_pre.replace('TT', f"{termino_base}S")
        sql_estudiantes_viendo_pre = sql_estudiantes_viendo_pre.replace('AAAA', f"{anio_base}")
        sql_estudiantes_viendo_pre = sql_estudiantes_viendo_pre.replace('xxxxx', "','".join(lis_cod_materias_pre))

        # Fetch all rows
        data_list = get_data_from_query(sql_estudiantes_viendo_pre)

        if len(data_list) == 0:
            print("⚠️ No se encontraron estudiantes viendo los prerrequisitos. Esto puede deberse a que no hay prerrequisitos o a un error en la consulta.")
            print("Si no ven prerequisito, quiere decir que son primera linea. No se toma en cuenta.")
            # dataframe vacio con columnas COD_ESTUDIANTE, COD_MATERIA_ACAD, NOMBRE, CARRERA, ANIO, TERMINO, VEZ_TOMADA
            df_estudiantes_viendo_pre = pd.DataFrame(columns=["COD_ESTUDIANTE", "COD_MATERIA_ACAD", "NOMBRE", "CARRERA", "ANIO", "TERMINO", "VEZ_TOMADA"])
        else:
            df_estudiantes_viendo_pre = pd.DataFrame(data_list)[["COD_ESTUDIANTE", "COD_MATERIA_ACAD", "NOMBRE", "CARRERA", "ANIO", "TERMINO", "VEZ_TOMADA"]].copy()

            # hacer antes el copy porque si no no sabe si es en el copy o en el original
            df_estudiantes_viendo_pre["COD_MATERIA_ACAD"] = df_estudiantes_viendo_pre["COD_MATERIA_ACAD"].str.strip() 

            print("Tamaño coincide", df_estudiantes_viendo_pre["COD_ESTUDIANTE"].shape[0] == len(data_list))

            df_estudiantes_viendo_pre = df_estudiantes_viendo_pre[df_estudiantes_viendo_pre["CARRERA"].isin(lis_carreras_pre)]

            df_estudiantes_viendo_pre["CARRERA"].value_counts()
            df_estudiantes_viendo_pre["NOMBRE"].value_counts()

            # Estudiantes que no deberian estar nuevamente si se quedan por tercera
            list_tercera = df_estudiantes_viendo_pre[df_estudiantes_viendo_pre["VEZ_TOMADA"] > 2]["COD_MATERIA_ACAD"]
            list_tercera

            dict_results = {}
            for cod_materia in lis_cod_materias_pre:
                list_matricula = df_estudiantes_viendo_pre[df_estudiantes_viendo_pre["COD_MATERIA_ACAD"] == cod_materia]["COD_ESTUDIANTE"].tolist()
                if len(list_matricula) == 0:
                    print(f"⚠️ No se encontraron estudiantes viendo el prerrequisito {cod_materia}. Esto puede deberse a que no hay estudiantes actualmente viendo ese prerrequisito o a un error en la consulta.")
                    continue
                results, mi_df, stats, list_student_off = make_analysis(list_matricula, cod_materia)

                if len(results) == 0:
                    
                    dificultad_materia_obj = df_complete[df_complete["COD_MATERIA_ACAD_MO"] == cod_materia_objetivo]["DIFICULTAD_MO"].unique()[0]

                    list_students_unique = df_estudiantes_viendo_pre["COD_ESTUDIANTE"].unique()
                    # quedarme con el ultimo registro unico de cada estudiante en df_complete, el año mayor y termino mayor
                    df_estudiantes_viendo_no_analizados = df_complete[df_complete["COD_ESTUDIANTE"].isin(list_students_unique)].sort_values(["anio", "termino_num"], ascending=[False, False])
                    df_estudiantes_viendo_no_analizados['CANT_ACTUAL_MAT_TOMADAS'] = df_estudiantes_viendo_no_analizados.groupby('COD_ESTUDIANTE')['COD_MATERIA_ACAD_MO'].transform('count')
                    df_estudiantes_viendo_no_analizados = df_estudiantes_viendo_no_analizados.drop_duplicates(subset=['COD_ESTUDIANTE'], keep='first')
                    
                    df_estudiantes_viendo_no_analizados["anio"] = df_estudiantes_viendo_no_analizados["anio"].astype(int)
                    df_estudiantes_viendo_no_analizados["DIFICULTAD_MO"] = dificultad_materia_obj
                    df_estudiantes_viendo_no_analizados["COD_MATERIA_ACAD_MO"] = cod_materia_objetivo
                    df_estudiantes_viendo_no_analizados["ESTADO_MAT_TOMADA_MO"] = "AC"
                    df_con_gpa_socioeconomico_interes = complete_data_to_model(df_estudiantes_viendo_no_analizados, df_gpa_general, df_socioeconomico)
                    df_con_gpa_socioeconomico_interes_clean = limpieza_df_con_gpa_socioeconomico_interes(df_con_gpa_socioeconomico_interes, label_encoders)

                    results = predict_academic_risk(modelo, feature_info, df_con_gpa_socioeconomico_interes_clean, return_dataframe=True)
                    stats = results['statistics']
                    mi_df = df_con_gpa_socioeconomico_interes_clean.copy()
                dict_results[cod_materia] = {
                    "results": results,
                    "dataframe": mi_df,
                    "statistics": stats
                }


            df_estudiantes_viendo_pre_tmp = df_estudiantes_viendo_pre.copy()
            df_estudiantes_viendo_pre_tmp["APROBADO"] = 0


            for cod_materia in dict_results.keys():
                list_matricula = df_estudiantes_viendo_pre[df_estudiantes_viendo_pre["COD_MATERIA_ACAD"] == cod_materia]["COD_ESTUDIANTE"].tolist()
                list_result = dict_results[cod_materia]["results"]["predictions"]
                if len(list_matricula) != len(list_result):
                    print(f"⚠️ Desalineación: {cod_materia} - {len(list_matricula)} estudiantes, {len(list_result)} predicciones")
                    print("IDs de estudiantes:", list_matricula)
                    print("IDs con datos completos:", dict_results[cod_materia]["dataframe"]["COD_ESTUDIANTE"].tolist())
                    # Estudiantes que faltan datos:
                    ids_con_datos = set(dict_results[cod_materia]["dataframe"]["COD_ESTUDIANTE"].tolist())
                    ids_sobrantes = [i for i in list_matricula if i not in ids_con_datos]
                    print("Estudiantes sobrantes (sin datos completos):", ids_sobrantes)
                for i, pred in zip(list_matricula, list_result):
                    df_estudiantes_viendo_pre_tmp.loc[
                        (df_estudiantes_viendo_pre_tmp["COD_ESTUDIANTE"] == i) & 
                        (df_estudiantes_viendo_pre_tmp["COD_MATERIA_ACAD"] == cod_materia), 
                        "APROBADO"
                    ] = pred


            print(df_estudiantes_viendo_pre.shape, df_estudiantes_viendo_pre_tmp.shape, df_estudiantes_viendo_pre_tmp["APROBADO"].value_counts())


        # ### Analizar los estudiantes actuales (2025-2S) con el modelo actual, para quedarnos con los reprobados para la planificacion 2026

        list_matricula = df_estudiantes_viendo["COD_ESTUDIANTE"].tolist()
        print(len(list_matricula), df_estudiantes_viendo["COD_ESTUDIANTE"].nunique())

        df_estudiantes_viendo_tmp = df_estudiantes_viendo.copy()
        df_estudiantes_viendo_tmp["APROBADO"] = 0
        
        results, mi_df, stats, list_student_off = make_analysis(list_matricula, cod_materia_objetivo)
        # ============================================================================================================= 
        df_con_gpa_socioeconomico_interes_clean = pd.DataFrame()
        if len(results) == 0 and df_estudiantes_viendo_tmp.shape[0] > 0:
            print("⚠️ No se encontraron resultados para los estudiantes viendo la materia objetivo. Esto puede deberse a que no hay datos completos para esos estudiantes o a un error en la consulta.")
            print("Es necesario que se completen todos los datos para que se analice correctamente el riesgo académico de los estudiantes viendo la materia objetivo.")
            need_reanalysis = True
            dificultad_materia_obj = df_complete[df_complete["COD_MATERIA_ACAD_MO"] == cod_materia_objetivo]["DIFICULTAD_MO"].unique()[0]

            list_students_unique = df_estudiantes_viendo_tmp["COD_ESTUDIANTE"].unique()
            # quedarme con el ultimo registro unico de cada estudiante en df_complete, el año mayor y termino mayor
            df_estudiantes_viendo_no_analizados = df_complete[df_complete["COD_ESTUDIANTE"].isin(list_students_unique)].sort_values(["anio", "termino_num"], ascending=[False, False])
            df_estudiantes_viendo_no_analizados['CANT_ACTUAL_MAT_TOMADAS'] = df_estudiantes_viendo_no_analizados.groupby('COD_ESTUDIANTE')['COD_MATERIA_ACAD_MO'].transform('count')
            df_estudiantes_viendo_no_analizados = df_estudiantes_viendo_no_analizados.drop_duplicates(subset=['COD_ESTUDIANTE'], keep='first')
            
            df_estudiantes_viendo_no_analizados["anio"] = df_estudiantes_viendo_no_analizados["anio"].astype(int)
            df_estudiantes_viendo_no_analizados["DIFICULTAD_MO"] = dificultad_materia_obj
            df_estudiantes_viendo_no_analizados["COD_MATERIA_ACAD_MO"] = cod_materia_objetivo
            df_estudiantes_viendo_no_analizados["ESTADO_MAT_TOMADA_MO"] = "AC"
            df_con_gpa_socioeconomico_interes = complete_data_to_model(df_estudiantes_viendo_no_analizados, df_gpa_general, df_socioeconomico)
            df_con_gpa_socioeconomico_interes_clean = limpieza_df_con_gpa_socioeconomico_interes(df_con_gpa_socioeconomico_interes, label_encoders)

            results = predict_academic_risk(modelo, feature_info, df_con_gpa_socioeconomico_interes_clean, return_dataframe=True)
            stats = results['statistics']

            print(df_con_gpa_socioeconomico_interes_clean.shape, len(results["predictions"]))
            df_con_gpa_socioeconomico_interes_clean["ESTADO_MAT_TOMADA_MO"] = df_con_gpa_socioeconomico_interes_clean.apply(
                lambda row: 'AP' if results["predictions"][row.name] == 1 else 'RP',
                axis=1
            )
        # ============================================================================================================= 

        index_matricula = 0
        for i in list_matricula:
            if i in list_student_off:
                # no agregar a ningun lado
                # df_estudiantes_viendo_tmp.loc[(df_estudiantes_viendo_tmp["COD_ESTUDIANTE"] == i), "APROBADO"] = "OFF"
                continue
            # print("Procesando estudiante:", i, "Índice:", index_matricula)
            df_estudiantes_viendo_tmp.loc[(df_estudiantes_viendo_tmp["COD_ESTUDIANTE"] == i), "APROBADO"] = results["predictions"][index_matricula]
            index_matricula += 1

        print("Estudiantes viendo actualmente resultados: ", df_estudiantes_viendo.shape, df_estudiantes_viendo_tmp.shape, df_estudiantes_viendo_tmp["APROBADO"].value_counts())
        
        ### Estudiantes que han visto el minimo numero de terminos para ver la materia objetivo que no tiene prerequisitos, y que no han visto la materia objetivo.
        df_estudiantes_materia_sin_prerequisito = pd.DataFrame()
        if df_pre_requisito.shape[0] == 0:
            estudiantes_con_materia = df_complete[df_complete['COD_MATERIA_ACAD_MO'] == cod_materia_objetivo]['COD_ESTUDIANTE']

            for row in df_pre_requisito_cp.itertuples():
                print("Carrera:", row.CARRERA, "Nivel:", row.NIVEL, "NUM_MIN_TERMINOS:", row.NUM_MIN_TERMINOS)
                df_estudiantes_materia_sin_prerequisito = pd.concat((df_estudiantes_materia_sin_prerequisito, df_complete[
                    (~df_complete['COD_ESTUDIANTE'].isin(estudiantes_con_materia)) & 
                    (df_complete['CARRERA'] == row.CARRERA) & 
                    (df_complete["TERMINOS_REGISTRADOS"] >= row.NUM_MIN_TERMINOS)
                ]), ignore_index=True)
            
            print("Estudiantes sin prerrequisito:", df_estudiantes_materia_sin_prerequisito.shape[0])
            print("Cantidad de estudiantes unicos sin prerrequisito:", df_estudiantes_materia_sin_prerequisito["COD_ESTUDIANTE"].nunique())
            # quedarme con el ultimo registro de df_estudiantes_materia_sin_prerequisito por cada estudiante COD_ESTUDIANTE priorizando el mayor termino y luego el mayor anio
            df_estudiantes_materia_sin_prerequisito = df_estudiantes_materia_sin_prerequisito.sort_values(['anio', 'termino_num'], ascending=[False, False])
            df_estudiantes_materia_sin_prerequisito['CANT_ACTUAL_MAT_TOMADAS'] = df_estudiantes_materia_sin_prerequisito.groupby('COD_ESTUDIANTE')['COD_MATERIA_ACAD_MO'].transform('count')
            df_estudiantes_materia_sin_prerequisito = df_estudiantes_materia_sin_prerequisito.drop_duplicates(subset=['COD_ESTUDIANTE'], keep='first')
            print("Estudiantes sin prerrequisito (registro único por estudiante):", df_estudiantes_materia_sin_prerequisito.shape[0])

        ### Estudiantes que ya han visto las prerequisitos pero no la objetivo y los reprobados de la materia objetivo. Y les tocaria ver la materia objetivo en 2026-1S
        ##### Descartar los RP y que estan viendo por tercera vez porque ya perdieron la carrera
        print("data_list", len(data_list))
        if len(data_list) > 0:
            list_tercera_and_rp = df_estudiantes_viendo_pre_tmp[(df_estudiantes_viendo_pre_tmp["APROBADO"] == 0) & (df_estudiantes_viendo_pre_tmp["VEZ_TOMADA"] > 2)]["COD_ESTUDIANTE"].unique().tolist()
        else:
            list_tercera_and_rp = []
        df_estudiantes_viendo_tmp = df_estudiantes_viendo_tmp[~df_estudiantes_viendo_tmp["COD_ESTUDIANTE"].isin(list_tercera_and_rp)]


        # df_estudiantes_viendo_tmp.shape, df_estudiantes_viendo_tmp["APROBADO"].value_counts()
        # df_complete["termino"].value_counts()

        ##### Actualizar la columna ESTADO_MAT_TOMADA_MO en df_complete

        # materias de pre requisito, periodo actual, estudiantes viendo esas materias

        # Mapeo de valores de APROBADO
        mapping = {1: 'AP', 0: 'RP'}

        # Actualizar df_complete con los que vieron la prerequisito y su estado de aprobado o reprobado
        if len(data_list) > 0:
            # Actualizar df_complete
            for index, row in df_estudiantes_viendo_pre_tmp.iterrows():
                # print("Procesando estudiante:", row['COD_ESTUDIANTE'], "Materia:", row['COD_MATERIA_ACAD'], "Aprobado:", row['APROBADO'])
                df_complete.loc[(df_complete['COD_ESTUDIANTE'] == row['COD_ESTUDIANTE']) & 
                                (df_complete['COD_MATERIA_ACAD_MO'] == row['COD_MATERIA_ACAD']) & 
                                (df_complete['anio'] == str(anio_base)) & 
                                (df_complete['termino'] == str(termino_base)+"S"), 
                                'ESTADO_MAT_TOMADA_MO'] = mapping[row['APROBADO']]  

        # df_complete[(df_complete["COD_ESTUDIANTE"] == '202515714') & (df_complete["COD_MATERIA_ACAD_MO"] == 'CCPG1043')]

        # Actualizar df_complete con los que vieron la materia objetivo y su estado de aprobado o reprobado
        for index, row in df_estudiantes_viendo_tmp.iterrows():
            # print("Procesando estudiante:", row['COD_ESTUDIANTE'], "Materia:", row['COD_MATERIA_ACAD'], "Aprobado:", row['APROBADO'])
            df_complete.loc[(df_complete['COD_ESTUDIANTE'] == row['COD_ESTUDIANTE']) & 
                            (df_complete['COD_MATERIA_ACAD_MO'] == row['COD_MATERIA_ACAD']) & 
                            (df_complete['anio'] == str(anio_base)) & 
                            (df_complete['termino'] == str(termino_base)+"S"), 
                            'ESTADO_MAT_TOMADA_MO'] = mapping[row['APROBADO']]  


        # df_complete[(df_complete["COD_ESTUDIANTE"] == '202400701') & (df_complete["COD_MATERIA_ACAD_MO"] == 'MATG1058')]

        ### Obtener los estudiantes que veran la materia objetivo en 2026-1S

        #### 1. Repitentes: Estudiantes con último estado RP o PF en la materia objetivo


        # Filtrar estudiantes que han cursado la materia objetivo
        df_cursaron_objetivo = df_complete[df_complete['COD_MATERIA_ACAD_MO'] == cod_materia_objetivo].copy()

        # Verificar si alguna vez aprobaron (AP) la materia objetivo
        estudiantes_con_ap = df_cursaron_objetivo[df_cursaron_objetivo['ESTADO_MAT_TOMADA_MO'] == 'AP']['COD_ESTUDIANTE'].unique()

        # Filtrar solo estudiantes que nunca aprobaron (excluir los que tienen AP)
        df_sin_ap = df_cursaron_objetivo[~df_cursaron_objetivo['COD_ESTUDIANTE'].isin(estudiantes_con_ap)]

        print("Cantidad de estudiantes que cursaron la materia objetivo mas de dos vez sin aprobar:", df_sin_ap['VEZ_TOMADA_MO'].value_counts()[2:].sum())

        # Filtrar solo RP o PF y han visto la materia mas de dos veces VEZ_TOMADA_MO
        df_rp_pf = df_sin_ap[(df_sin_ap['ESTADO_MAT_TOMADA_MO'].isin(['RP', 'PF'])) & (df_sin_ap['VEZ_TOMADA_MO'] < 3)].copy()
        print("Deberian ser igual: ", df_sin_ap.shape[0] == df_rp_pf.shape[0])

        # Ordenar por estudiante y fecha para obtener el último registro
        df_rp_pf = df_rp_pf.sort_values(['anio', 'termino_num'], ascending=[True, True])

        # Obtener el último registro por estudiante
        df_repitentes = df_rp_pf.groupby('COD_ESTUDIANTE').first().reset_index()


        df_repitentes.shape


        print(f"Total de repitentes: {df_repitentes.shape[0]}")
        df_repitentes.head()


        df_repitentes.groupby(["anio", "termino"]).size()


        df_repitentes["ESTADO_MAT_TOMADA_MO"].value_counts()

        #### 2. Nuevos: Estudiantes que cumplen prerrequisitos y nunca cursaron la materia objetivo

        # 1. Obtener las materias prerrequisito por carrera
        prereq_por_carrera = (
            df_pre_requisito.groupby('CARRERA')['CODIGOMATERIA']
            .apply(lambda x: set(x.str.strip()))
            .reset_index()
            .rename(columns={'CODIGOMATERIA': 'materias_requeridas'})
        )


        # 2. Filtrar registros de df_complete donde el estudiante APROBÓ los prerrequisitos
        df_complete_prereq_aprobados = df_complete[
            (df_complete['COD_MATERIA_ACAD_MO'].isin(lis_cod_materias_pre)) &
            (df_complete['CARRERA'].isin(lis_carreras_pre)) &
            (df_complete['ESTADO_MAT_TOMADA_MO'] == 'AP')  # Solo materias aprobadas
        ].copy()


        # 3. Agrupar por estudiante y carrera para obtener materias aprobadas
        materias_aprobadas_por_estudiante = (
            df_complete_prereq_aprobados.groupby(['COD_ESTUDIANTE', 'CARRERA'])['COD_MATERIA_ACAD_MO']
            .apply(lambda x: set(x.str.strip() if hasattr(x, 'str') else x))
            .reset_index()
            .rename(columns={'COD_MATERIA_ACAD_MO': 'materias_aprobadas'})
        )


        materias_aprobadas_por_estudiante



        # 4. Hacer merge para comparar con prerrequisitos requeridos
        df_comparacion = pd.merge(
            materias_aprobadas_por_estudiante,
            prereq_por_carrera,
            on='CARRERA',
            how='inner'
        )


        # 5. Verificar que tengan TODOS los prerrequisitos aprobados
        if not df_comparacion.empty:
            df_comparacion['tiene_todos_prereq'] = df_comparacion.apply(
                lambda row: row['materias_requeridas'].issubset(row['materias_aprobadas']),
                axis=1
            )
            estudiantes_con_prereq_completos = df_comparacion[df_comparacion['tiene_todos_prereq']]
        else:
            estudiantes_con_prereq_completos = pd.DataFrame()

        # 6. Filtrar estudiantes que NUNCA han visto la materia objetivo
        estudiantes_vieron_objetivo = set(
            df_complete[df_complete['COD_MATERIA_ACAD_MO'] == cod_materia_objetivo]['COD_ESTUDIANTE']
        )


        # 7. Resultado final: estudiantes elegibles (con prereq aprobados y sin haber visto objetivo)
        if not estudiantes_con_prereq_completos.empty and 'COD_ESTUDIANTE' in estudiantes_con_prereq_completos.columns:
            df_nuevos = estudiantes_con_prereq_completos[
                ~estudiantes_con_prereq_completos['COD_ESTUDIANTE'].isin(estudiantes_vieron_objetivo)
            ].copy()
        else:
            df_nuevos = pd.DataFrame()


        if len(estudiantes_con_prereq_completos) > 0:
            print(f"📊 Resumen:")
            print(f"  - Estudiantes con todos los prerrequisitos APROBADOS: {len(estudiantes_con_prereq_completos)}")
            print(f"  - Estudiantes que vieron {cod_materia_objetivo}: {len(estudiantes_vieron_objetivo)}")
            print(f"  - Estudiantes NUEVOS elegibles: {len(df_nuevos)}")
            print(f"\nDistribución por carrera:")
            print(df_nuevos['CARRERA'].value_counts())


            if not df_nuevos.empty:
                # 1. Validación final: Verificar que TODOS los prerrequisitos estén cumplidos
                print("🔍 Validación de prerrequisitos por estudiante:")
                for idx, row in df_nuevos.iterrows():
                    faltantes = row['materias_requeridas'] - row['materias_aprobadas']
                    if len(faltantes) > 0:
                        print(f"  ⚠️ Estudiante {row['COD_ESTUDIANTE']} - Carrera: {row['CARRERA']} - Faltantes: {faltantes}")

                # Verificar que no haya faltantes
                df_nuevos['prereq_completos'] = df_nuevos.apply(
                    lambda row: len(row['materias_requeridas'] - row['materias_aprobadas']) == 0,
                    axis=1
                )
                print(f"\n✅ Todos cumplen prerrequisitos: {df_nuevos['prereq_completos'].all()}")
                print(f"Total estudiantes con prerrequisitos completos: {df_nuevos['prereq_completos'].sum()}")


        # cod_materia_objetivo


        # para comprobar que ese estudiante no ha visto la materia objetivo y si ha visto las materias requestidas
        # df_complete[(df_complete['COD_ESTUDIANTE'] == "201229676") & (df_complete['COD_MATERIA_ACAD_MO'] == "MATG1057")]

        
        #### 3. Unión: DataFrame final con Repitentes y Nuevos


        # Agregar columna identificadora del tipo de estudiante
        df_repitentes['TIPO_ESTUDIANTE'] = 'REPITENTE'
        if len(df_nuevos) > 0:
            df_nuevos['TIPO_ESTUDIANTE'] = 'NUEVO'
            # Unir ambos dataframes
            df_final_nuevos_y_repitentes = pd.concat([df_repitentes, df_nuevos], ignore_index=True)
        elif df_estudiantes_materia_sin_prerequisito.shape[0] > 0:
            df_estudiantes_materia_sin_prerequisito['TIPO_ESTUDIANTE'] = 'SIN_PREREQUISITO'
            # Unir ambos dataframes
            df_final_nuevos_y_repitentes = pd.concat([df_repitentes, df_estudiantes_materia_sin_prerequisito], ignore_index=True)
        else:
            df_final_nuevos_y_repitentes = df_repitentes.copy()


        # Ordenar por tipo y código de estudiante
        df_final_nuevos_y_repitentes = df_final_nuevos_y_repitentes.sort_values(['TIPO_ESTUDIANTE', 'COD_ESTUDIANTE']).reset_index(drop=True)

        print(f"\n📊 RESUMEN FINAL:")
        print(f"  • Repitentes: {df_repitentes.shape[0]}")
        print(f"  • Nuevos: {df_nuevos.shape[0]}")
        print(f"  • TOTAL: {df_final_nuevos_y_repitentes.shape[0]}")
        print(f"\nDistribución por tipo:")
        print(df_final_nuevos_y_repitentes['TIPO_ESTUDIANTE'].value_counts())

        # Verificación: mostrar ejemplos de cada tipo
        print("\n🔍 Ejemplos de REPITENTES:")
        print(df_final_nuevos_y_repitentes[df_final_nuevos_y_repitentes['TIPO_ESTUDIANTE'] == 'REPITENTE'][['COD_ESTUDIANTE', 'TIPO_ESTUDIANTE', 'ESTADO_MAT_TOMADA_MO', 'anio', 'termino']].head())

        print("\n🔍 Ejemplos de NUEVOS:")
        print(df_final_nuevos_y_repitentes[df_final_nuevos_y_repitentes['TIPO_ESTUDIANTE'] == 'NUEVO'][['COD_ESTUDIANTE', 'TIPO_ESTUDIANTE']].head())

        print("\n🔍 Ejemplos de SIN PREREQUISITO:")
        print(df_final_nuevos_y_repitentes[df_final_nuevos_y_repitentes['TIPO_ESTUDIANTE'] == 'SIN_PREREQUISITO'][['COD_ESTUDIANTE', 'TIPO_ESTUDIANTE']].head())
        
        #### Obtener los ultimos registros de los estudiantes que veran la materia objetivo (df_final_nuevos_y_repitentes["COD_ESTUDIANTE"].unique())
        df_final_nuevos_y_repitentes["COD_ESTUDIANTE"].nunique(), df_final_nuevos_y_repitentes.shape[0]


        # 1. Filtrar el df_complete para tener solo los estudiantes de df_final_nuevos_y_repitentes
        estudiantes_ids = df_final_nuevos_y_repitentes["COD_ESTUDIANTE"].unique()
        df_filtrado = df_complete[df_complete["COD_ESTUDIANTE"].isin(estudiantes_ids)].copy()
        # eliminar los que tienen una VEZ_TOMADA_MO = 3 y ESTADO_MAT_TOMADA_MO = RP o PF
        df_filtrado = df_filtrado[~((df_filtrado["VEZ_TOMADA_MO"] == 3) & (df_filtrado["ESTADO_MAT_TOMADA_MO"].isin(["RP", "PF"])))]

        # 2. Crear un identificador numérico único para el periodo (Año + Término)
        # Multiplicamos el año por 100 para que 2020-2 sea mayor que 2020-1 de forma matemática
        df_filtrado['periodo_id'] = (df_filtrado['anio'].astype(int) * 100) + df_filtrado['termino_num']

        # 3. Calcular el periodo MÁXIMO por cada estudiante y asignarlo a una nueva columna
        # transform('max') repite el valor máximo del grupo en todas las filas de ese estudiante
        df_filtrado['max_periodo'] = df_filtrado.groupby('COD_ESTUDIANTE')['periodo_id'].transform('max')

        # 4. Filtrar las filas donde el periodo actual coincide con el máximo encontrado
        df_resultado = df_filtrado[df_filtrado['periodo_id'] == df_filtrado['max_periodo']].copy()

        # Limpiar columnas auxiliares
        df_resultado.drop(columns=['periodo_id', 'max_periodo'], inplace=True)

        list_student_resultado = df_resultado["COD_ESTUDIANTE"].unique()
        print(len(list_student_resultado), len(estudiantes_ids))

        
        #### Quedarme con el mayor y actualiza su DIFICULTAD_MO


        dificultad_materia_obj = df_complete[df_complete["COD_MATERIA_ACAD_MO"] == cod_materia_objetivo]["DIFICULTAD_MO"].unique()[0]


        # 1. Calcular la diferencia absoluta con la dificultad objetivo
        # (Asumiendo que 'dificultad_materia_obj' es una variable con el valor numérico)
        df_resultado['diff_gap'] = (df_resultado['DIFICULTAD_MO'].astype(float) - dificultad_materia_obj).abs()


        # 2. Ordenar los datos
        # - Primero por estudiante (para agrupar)
        # - Segundo por 'diff_gap' ASCENDENTE (el más cercano a 0 es el más similar)
        # - Tercero por 'PROMEDIO_MO' DESCENDENTE (el más alto gana en caso de empate o cercanía similar)
        df_ordenado = df_resultado.sort_values(
            by=['COD_ESTUDIANTE', 'diff_gap', 'PROMEDIO_MO'],
            ascending=[True, True, False]
        )


        # agregar la columna CANT_ACTUAL_MAT_TOMADAS  a df_ordenado antes de eliminar los duplicados
        # df_ordenado['CANT_ACTUAL_MAT_TOMADAS'] = df_ordenado.groupby('COD_ESTUDIANTE').cumcount() + 1
        df_ordenado['CANT_ACTUAL_MAT_TOMADAS'] = df_ordenado.groupby('COD_ESTUDIANTE')['COD_MATERIA_ACAD_MO'].transform('count')


        # 3. Quedarse con la primera fila de cada estudiante (la mejor opción según el orden)
        df_seleccion_final = df_ordenado.drop_duplicates(subset='COD_ESTUDIANTE', keep='first').copy()


        # Limpieza opcional
        df_seleccion_final.drop(columns=['diff_gap'], inplace=True)

        df_seleccion_final["COD_ESTUDIANTE"].nunique(), df_final_nuevos_y_repitentes["COD_ESTUDIANTE"].nunique(), df_resultado["COD_ESTUDIANTE"].nunique()


        df_seleccion_final["DIFICULTAD_MO"] = dificultad_materia_obj
        df_seleccion_final["COD_MATERIA_ACAD_MO"] = cod_materia_objetivo
        df_seleccion_final["ESTADO_MAT_TOMADA_MO"] = "AC"

        
        # ### Usar el modelo para 2026-1S
        df_seleccion_final["anio"] = df_seleccion_final["anio"].astype(int)


        df_final_nuevos_y_repitentes[df_final_nuevos_y_repitentes["TIPO_ESTUDIANTE"] == "NUEVO"]["COD_ESTUDIANTE"].nunique()

        df_con_gpa_socioeconomico_interes = complete_data_to_model(df_seleccion_final, df_gpa_general, df_socioeconomico)
        df_con_gpa_socioeconomico_interes_clean = limpieza_df_con_gpa_socioeconomico_interes(df_con_gpa_socioeconomico_interes, label_encoders)

        results = predict_academic_risk(modelo, feature_info, df_con_gpa_socioeconomico_interes_clean, return_dataframe=True)
        stats = results['statistics']

        print(df_con_gpa_socioeconomico_interes_clean.shape, len(results["predictions"]))

        
        ### Save dataframe with predictions
        # Para la primera ejecucion va comentado todo 
        df_new_semester = pd.read_csv("../data/riesgo_academico/all_2026_1S.csv")
        df_seleccion_final_3 = pd.read_csv("../data/riesgo_academico/PAO_2026_1S.csv")


        # df_new_semester.keys()
        list_keys = ['COD_ESTUDIANTE', 'COD_MATERIA_ACAD_MO',
            'ESTADO_MAT_TOMADA_MO', 'VEZ_TOMADA_MO', 'NOTA1_MO', 'NOTA2MO',
            'PROMEDIO_MO', 'DIFICULTAD_MO', 'T_MAT_TOMADAS', 'PROM_1PARCIAL',
            'PROM_2PARCIAL', 'PROM_CALIFICACIONES', 'MAT_APROBADAS',
            'PROM_CALIF_APROBADAS', 'TERMINOS_REGISTRADOS', 'PERDIO_CARRERA',
            'PROM_MAT_REPROBADAS1', 'PROM_MAT_REPROBADAS2', 'PROM_MAT_REPROBADAS3',
            'MUY_FACIL', 'FACIL', 'MODERADA', 'DIFICIL', 'MUY_DIFICIL',
            'promedio_general', 'CODIGOMATERIA', 'MATERIA']


        # df_con_gpa_socioeconomico_interes_clean["ESTADO_MAT_TOMADA_MO"] = if results["predictions"] = 0 "RP" else "AP"
        df_con_gpa_socioeconomico_interes_clean["ESTADO_MAT_TOMADA_MO"] = df_con_gpa_socioeconomico_interes_clean.apply(
            lambda row: 'AP' if results["predictions"][row.name] == 1 else 'RP',
            axis=1
        )

        print("Para la materia objetivo:", cod_materia_objetivo, ":", materia_objetivo)


        df_con_gpa_socioeconomico_interes_clean["ESTADO_MAT_TOMADA_MO"].value_counts()


        # agregar al final de df_new_semester lo que corresonda de df_con_gpa_socioeconomico_interes_clean
        df_tmp_new_semester = pd.concat([df_new_semester, df_con_gpa_socioeconomico_interes_clean[df_new_semester.keys()]], ignore_index=True)
        # Para primera ejecucion solo
        # df_tmp_new_semester = df_con_gpa_socioeconomico_interes_clean[list_keys].copy()

        df_tmp_new_semester.to_csv("../data/riesgo_academico/all_2026_1S.csv", index=False, float_format="%.2f")

        df_tmp_seleccion_final_3  = pd.concat([df_seleccion_final_3, df_con_gpa_socioeconomico_interes_clean], ignore_index=True)
        # Para primera ejecucion solo
        # df_tmp_seleccion_final_3 = df_con_gpa_socioeconomico_interes_clean.copy()



        df_tmp_seleccion_final_3.to_csv("../data/riesgo_academico/PAO_2026_1S.csv", index=False, float_format="%.2f")
        print("+"*100)
    except Exception as e:
        print(f"xx Error en el proceso para {cod_materia_objetivo} - {materia_objetivo}: {e}")
        print("x"*100)
        list_cod_error.append(cod_materia_objetivo)
        
ibm_db.close(conn)
print("++++"*20)
print("Proceso de planificación y aprobación para 2026-1S finalizado.")
print(len(list_cod_error), "materias con error.")
print("Proceso completado. Materias con error:", list_cod_error)
