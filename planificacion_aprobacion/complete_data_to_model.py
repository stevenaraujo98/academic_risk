import pandas as pd
import numpy as np

def complete_data_to_model(df, df_gpa_general, df_socioeconomico):
    # Agregar el GPA general al dataframe final
    df_con_gpa = pd.merge(
        df,
        df_gpa_general[['COD_ESTUDIANTE', 'ANIO', 'TERMINO', 'NUMERADOR', 'DENOMINADOR']],
        left_on=['COD_ESTUDIANTE', 'anio', "termino"],
        right_on=['COD_ESTUDIANTE', 'ANIO', "TERMINO"],
        how='left'
    )

    # Calcular GPA
    df_con_gpa['GPA'] = round(df_con_gpa['NUMERADOR'] / df_con_gpa['DENOMINADOR'], 2)
    # Limpiar columnas auxiliares si es necesario
    df_con_gpa = df_con_gpa.drop(columns=['NUMERADOR', 'DENOMINADOR', 'ANIO'], errors='ignore')

    df_con_gpa_socioeconomico = pd.merge(
        df_con_gpa,
        df_socioeconomico[['CODESTUDIANTE', 'GASTOS_RUBRO']],
        left_on='COD_ESTUDIANTE',
        right_on='CODESTUDIANTE',
        how='left',
        # validate='one_to_one'
    ).drop(columns=['CODESTUDIANTE']).copy()

    df_con_gpa_socioeconomico["GASTOS_RUBRO"].fillna(df_con_gpa_socioeconomico["GASTOS_RUBRO"].mean(), inplace=True)

    # Interacciones
    df_con_gpa_socioeconomico['VEZ_x_DIFICULTAD'] =  (df_con_gpa_socioeconomico['VEZ_TOMADA_MO'] * df_con_gpa_socioeconomico['DIFICULTAD_MO']) ** 2

    # Ratios
    df_con_gpa_socioeconomico['RATIO_APROBADAS'] = np.log(df_con_gpa_socioeconomico['MAT_APROBADAS'] / (df_con_gpa_socioeconomico['T_MAT_TOMADAS'] + 1))
    df_con_gpa_socioeconomico['TASA_REPROBACION'] = df_con_gpa_socioeconomico['PROM_MAT_REPROBADAS1'] / (df_con_gpa_socioeconomico['T_MAT_TOMADAS'] + 1)
    # No lineales
    df_con_gpa_socioeconomico['GPA_CUADRADO'] = df_con_gpa_socioeconomico['GPA'] ** 2
    df_con_gpa_socioeconomico['LOG_CANT_MAT'] = np.log1p(df_con_gpa_socioeconomico['CANT_ACTUAL_MAT_TOMADAS'])
    df_con_gpa_socioeconomico['LOG_GASTOS_RUBRO'] = np.log1p(df_con_gpa_socioeconomico['GASTOS_RUBRO'])

    df_socioeconomico["FECHANACIMIENTO"] = pd.to_datetime(df_socioeconomico["FECHANACIMIENTO"], errors='coerce', format="%Y-%m-%d")
    anio_ingreso = df_socioeconomico["ANIO_TERMINO_INGRESO"].str.split(' ').str[0].astype(int)
    df_socioeconomico["edad_ingreso"] = (anio_ingreso - df_socioeconomico["FECHANACIMIENTO"].dt.year)

    # apartir de la columna IDIOMAS se genere otra que sea NUMERO_IDIOMAS y si es nan sea cero
    df_socioeconomico["NUMERO_IDIOMAS"] = df_socioeconomico["IDIOMAS"].fillna("0").apply(
        lambda x: 0 if x == "0" or pd.isna(x) or str(x).lower() in ['nan', 'ninguno', 'no', ''] 
        else len(str(x).split(';')) if ';' in str(x) 
        else len(str(x).split(',')) if ',' in str(x)
        else 1 if str(x).strip() != '' 
        else 0
    )

    df_socioeconomico_interes =  df_socioeconomico[["CODESTUDIANTE", "PORCENTAJEDISCAPACIDAD", "VECESBUSENTRADA", "VECESBUSSALIDA", "NUMERO_IDIOMAS", "CANTIDADCUARTOS", "CANTIDADBANIO", "edad_ingreso", "TIPOCOLEGIO", "BECACOLEGIO", "TIENEDISCAPACIDAD", "TIPODISCAPACIDAD", "ESTADOCIVIL", "OTROSIDIOMAS", "TIEMPOPROMEDIOLLEGARESPOL", "NIVELINGLES", "NIVELINSTRUCCIONPADRE", "NIVELINSTRUCCIONMADRE", "ESTADOCIVILPADRES", "FAMILIARDISCAPACIDAD", "FAMILIARENFERMEDAD", "TIPOPARROQUIA", "VIVEGRUPOFAMILIAR", "SEXO"]]
    # todas las columnas str a minusculas
    for col in df_socioeconomico_interes.select_dtypes(include=['object']).columns:
        df_socioeconomico_interes[col] = df_socioeconomico_interes[col].str.lower().str.strip()

    df_con_gpa_socioeconomico_interes = pd.merge(
        df_con_gpa_socioeconomico,
        df_socioeconomico_interes,
        left_on='COD_ESTUDIANTE',
        right_on='CODESTUDIANTE',
        how='left',
        # validate='one_to_one'
    )

    df_con_gpa_socioeconomico_interes["TIPODISCAPACIDAD"] = df_con_gpa_socioeconomico_interes["TIPODISCAPACIDAD"].fillna("no definida")
    df_con_gpa_socioeconomico_interes["TIENEDISCAPACIDAD"] = df_con_gpa_socioeconomico_interes["TIENEDISCAPACIDAD"].fillna("n")
    df_con_gpa_socioeconomico_interes[df_con_gpa_socioeconomico_interes["TIENEDISCAPACIDAD"] == "nan"] = "n"
    df_con_gpa_socioeconomico_interes["TIPOCOLEGIO"] = df_con_gpa_socioeconomico_interes["TIPOCOLEGIO"].fillna("nacional")
    df_con_gpa_socioeconomico_interes["BECACOLEGIO"] = df_con_gpa_socioeconomico_interes["BECACOLEGIO"].fillna("ninguna")
    df_con_gpa_socioeconomico_interes["ESTADOCIVIL"] = df_con_gpa_socioeconomico_interes["ESTADOCIVIL"].fillna("soltero")
    df_con_gpa_socioeconomico_interes["OTROSIDIOMAS"] = df_con_gpa_socioeconomico_interes["OTROSIDIOMAS"].fillna("no")
    df_con_gpa_socioeconomico_interes["TIEMPOPROMEDIOLLEGARESPOL"] = df_con_gpa_socioeconomico_interes["TIEMPOPROMEDIOLLEGARESPOL"].fillna("61 a 90 minutos")
    df_con_gpa_socioeconomico_interes["NIVELINGLES"] = df_con_gpa_socioeconomico_interes["NIVELINGLES"].fillna("básico")
    df_con_gpa_socioeconomico_interes["NIVELINSTRUCCIONPADRE"] = df_con_gpa_socioeconomico_interes["NIVELINSTRUCCIONPADRE"].fillna("desconocido")
    df_con_gpa_socioeconomico_interes["NIVELINSTRUCCIONMADRE"] = df_con_gpa_socioeconomico_interes["NIVELINSTRUCCIONMADRE"].fillna("desconocido")
    df_con_gpa_socioeconomico_interes["ESTADOCIVILPADRES"] = df_con_gpa_socioeconomico_interes["ESTADOCIVILPADRES"].fillna("unión de hecho")
    df_con_gpa_socioeconomico_interes["FAMILIARDISCAPACIDAD"] = df_con_gpa_socioeconomico_interes["FAMILIARDISCAPACIDAD"].fillna("no")
    df_con_gpa_socioeconomico_interes["FAMILIARENFERMEDAD"] = df_con_gpa_socioeconomico_interes["FAMILIARENFERMEDAD"].fillna("no")
    df_con_gpa_socioeconomico_interes["TIPOPARROQUIA"] = df_con_gpa_socioeconomico_interes["TIPOPARROQUIA"].fillna("urbana")
    df_con_gpa_socioeconomico_interes["VIVEGRUPOFAMILIAR"] = df_con_gpa_socioeconomico_interes["VIVEGRUPOFAMILIAR"].fillna("si")
    df_con_gpa_socioeconomico_interes["SEXO"] = df_con_gpa_socioeconomico_interes["SEXO"].fillna("masculino")
    df_con_gpa_socioeconomico_interes["PERDIO_CARRERA"] = df_con_gpa_socioeconomico_interes["PERDIO_CARRERA"].str.lower()

    return df_con_gpa_socioeconomico_interes


def limpieza_df_con_gpa_socioeconomico_interes(df_con_gpa_socioeconomico_interes_clean, label_encoders):
    list_enfermedad = [
        "yo mismo (estudiante):no tiene discapacidad;pareja:no tiene discapacidad;hijo(a):intelectual (retraso mental);hijo(a):no tiene discapacidad;",
        "hijo(a):no tiene enfermedad;hijo(a):no tiene enfermedad;hijo(a):no tiene enfermedad;yo mismo (estudiante):otro;madre:no tiene enfermedad;padre:todo tipo de malformaciones congénitas del corazón y todo tipo de valvulopatías cardíacas;otro:no tiene enfermedad;hermano(a):no tiene enfermedad;",
        "hijo(a):no tiene discapacidad;hijo(a):no tiene discapacidad;hijo(a):no tiene discapacidad;yo mismo (estudiante):no tiene discapacidad;madre:no tiene discapacidad;padre:no tiene discapacidad;otro:intelectual (retraso mental);hermano(a):no tiene discapacidad;",
    ]
    for enfermedad in list_enfermedad:
        if df_con_gpa_socioeconomico_interes_clean[df_con_gpa_socioeconomico_interes_clean["FAMILIARENFERMEDAD"] == enfermedad]["FAMILIARENFERMEDAD"].size > 0:
            # entonces reemplazar ese valor por "no"
            df_con_gpa_socioeconomico_interes_clean.loc[df_con_gpa_socioeconomico_interes_clean["FAMILIARENFERMEDAD"] == enfermedad, "FAMILIARENFERMEDAD"]  = "no"

    # Diagnosticar qué columna tiene valores desconocidos
    print("🔍 Verificando valores en cada columna categórica...\n")

    encoded_columns = {
        'TIPOCOLEGIO': 'TIPOCOLEGIO_encoded',
        'BECACOLEGIO': 'BECACOLEGIO_encoded',
        'COD_MATERIA_ACAD_MO': 'COD_MATERIA_ACAD_MO_encoded',
        'TIENEDISCAPACIDAD': 'TIENEDISCAPACIDAD_encoded',
        'TIPODISCAPACIDAD': 'TIPODISCAPACIDAD_encoded',
        'ESTADOCIVIL': 'ESTADOCIVIL_encoded',
        'OTROSIDIOMAS': 'OTROSIDIOMAS_encoded',
        'TIEMPOPROMEDIOLLEGARESPOL': 'TIEMPOPROMEDIOLLEGARESPOL_encoded',
        'NIVELINGLES': 'NIVELINGLES_encoded',
        'NIVELINSTRUCCIONPADRE': 'NIVELINSTRUCCIONPADRE_encoded',
        'NIVELINSTRUCCIONMADRE': 'NIVELINSTRUCCIONMADRE_encoded',
        'ESTADOCIVILPADRES': 'ESTADOCIVILPADRES_encoded',
        'FAMILIARDISCAPACIDAD': 'FAMILIARDISCAPACIDAD_encoded',
        'FAMILIARENFERMEDAD': 'FAMILIARENFERMEDAD_encoded',
        'TIPOPARROQUIA': 'TIPOPARROQUIA_encoded',
        'VIVEGRUPOFAMILIAR': 'VIVEGRUPOFAMILIAR_encoded',
        'SEXO': 'SEXO_encoded',
        'PERDIO_CARRERA': 'PERDIO_CARRERA_encoded',
        'termino': 'termino_encoded'
    }

    for original_col in encoded_columns.keys():
        if original_col in df_con_gpa_socioeconomico_interes_clean.columns and original_col in label_encoders:
            valores_encoder = set(label_encoders[original_col].classes_)
            valores_datos = set(df_con_gpa_socioeconomico_interes_clean[original_col].astype(str).unique())
            desconocidos = valores_datos - valores_encoder
            
            if desconocidos:
                print(f"⚠️ {original_col}:")
                print(f"   Valores en encoder: {valores_encoder}")
                print(f"   Valores en datos: {valores_datos}")
                print(f"   DESCONOCIDOS: {desconocidos}\n")

                if original_col == "FAMILIARDISCAPACIDAD" or original_col == "FAMILIARENFERMEDAD":
                    print(desconocidos)
                    print(f"   Como es {original_col} y es desconocido será reemplazado por 'no'")
                    df_con_gpa_socioeconomico_interes_clean.loc[df_con_gpa_socioeconomico_interes_clean[original_col].isin(desconocidos), original_col] = "no"

            # else:
            #     print(f"✅ {original_col}: OK\n")

    
    # Aplicar label encoders a las columnas categóricas
    encoded_columns = {
        'TIPOCOLEGIO': 'TIPOCOLEGIO_encoded',
        'BECACOLEGIO': 'BECACOLEGIO_encoded',
        'COD_MATERIA_ACAD_MO': 'COD_MATERIA_ACAD_MO_encoded',
        'TIENEDISCAPACIDAD': 'TIENEDISCAPACIDAD_encoded',
        'TIPODISCAPACIDAD': 'TIPODISCAPACIDAD_encoded',
        'ESTADOCIVIL': 'ESTADOCIVIL_encoded',
        'OTROSIDIOMAS': 'OTROSIDIOMAS_encoded',
        'TIEMPOPROMEDIOLLEGARESPOL': 'TIEMPOPROMEDIOLLEGARESPOL_encoded',
        'NIVELINGLES': 'NIVELINGLES_encoded',
        'NIVELINSTRUCCIONPADRE': 'NIVELINSTRUCCIONPADRE_encoded',
        'NIVELINSTRUCCIONMADRE': 'NIVELINSTRUCCIONMADRE_encoded',
        'ESTADOCIVILPADRES': 'ESTADOCIVILPADRES_encoded',
        'FAMILIARDISCAPACIDAD': 'FAMILIARDISCAPACIDAD_encoded',
        'FAMILIARENFERMEDAD': 'FAMILIARENFERMEDAD_encoded',
        'TIPOPARROQUIA': 'TIPOPARROQUIA_encoded',
        'VIVEGRUPOFAMILIAR': 'VIVEGRUPOFAMILIAR_encoded',
        'SEXO': 'SEXO_encoded',
        'PERDIO_CARRERA': 'PERDIO_CARRERA_encoded',
        'termino': 'termino_encoded'
    }

    # Aplicar transformación con los label_encoders
    for original_col, encoded_col in encoded_columns.items():
        try:
            if original_col in df_con_gpa_socioeconomico_interes_clean.columns and original_col in label_encoders:
                # print(f"Transformando {original_col}...")
                df_con_gpa_socioeconomico_interes_clean[encoded_col] = label_encoders[original_col].transform(
                    df_con_gpa_socioeconomico_interes_clean[original_col].astype(str)
                )
                # print(f"✅ {original_col} → {encoded_col}")
            else:
                print(f"⚠️ {original_col} no encontrada o sin encoder disponible")
        except Exception as e:
            print(f"Error transformando {original_col}: {e}")

    
    df_con_gpa_socioeconomico_interes_clean["PROMEDIO_MO"] = df_con_gpa_socioeconomico_interes_clean["PROMEDIO_MO"].str.replace(",", ".").astype(float)
    df_con_gpa_socioeconomico_interes_clean["PROM_CALIFICACIONES"] = df_con_gpa_socioeconomico_interes_clean["PROM_CALIFICACIONES"].str.replace(",", ".").astype(float)
    df_con_gpa_socioeconomico_interes_clean["PROM_CALIF_APROBADAS"] = df_con_gpa_socioeconomico_interes_clean["PROM_CALIF_APROBADAS"].str.replace(",", ".").astype(float)
    df_con_gpa_socioeconomico_interes_clean["PROM_MAT_REPROBADAS2"] = df_con_gpa_socioeconomico_interes_clean["PROM_MAT_REPROBADAS2"].str.replace(",", ".").astype(float)
    df_con_gpa_socioeconomico_interes_clean["PROM_MAT_REPROBADAS3"] = df_con_gpa_socioeconomico_interes_clean["PROM_MAT_REPROBADAS3"].str.replace(",", ".").astype(float)

    return df_con_gpa_socioeconomico_interes_clean

