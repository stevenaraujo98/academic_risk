import pandas as pd
import joblib

Q1_RIESGO_ACADEMICO = 0.3
Q2_RIESGO_ACADEMICO = 0.5
Q3_RIESGO_ACADEMICO = 0.7

def get_model_available():
    # Cargar modelos y encoders
    print("\n📂 Cargando modelos y configuración...")
    label_encoders = joblib.load('../models/label_encoders.pkl')
    feature_info = joblib.load('../models/feature_info.pkl')


    nombre_modelo, ruta_modelo = ('Random Forest', '../models/random_forest_model.pkl')
    print(f"\n✅ Modelo seleccionado: {nombre_modelo}: {ruta_modelo}")

    # Cargar modelo
    modelo = joblib.load(ruta_modelo)
    print(f"✓ Modelo cargado desde '{ruta_modelo}'")

    return modelo, label_encoders, feature_info

def get_data_academic_risk(list_matricula, cod_materia, label_encoders):
    file_dir = "../data/riesgo_academico/saved/inference_data.csv"
    print("file_dir", file_dir)
    df_inference = pd.read_csv(file_dir)
    print(f"✅ Datos de inferencia cargados: {len(df_inference)} registros")

    materia_encoder = label_encoders['COD_MATERIA_ACAD_MO']
    if cod_materia in materia_encoder.classes_:
        valor_encoded = materia_encoder.transform([cod_materia])[0]
        print(f"\n✅ {cod_materia} encontrado!")
        print(f"   Valor original: {cod_materia}, Valor encoded: {valor_encoded}")
    else:
        print(f"⚠️ La materia '{cod_materia}' no se encuentra en los datos de inferencia.")
        return pd.DataFrame(), list_matricula  # Retornar DataFrame vacío y lista original de matrículas

    df_inference['COD_ESTUDIANTE'] = df_inference['COD_ESTUDIANTE'].astype(str)
    
    # Filtrar por materia primero
    df_materia = df_inference[df_inference['COD_MATERIA_ACAD_MO_encoded'] == valor_encoded]
    
    # Verificar si hay datos para esta materia
    if df_materia.shape[0] == 0:
        print(f"⚠️ No se encontraron datos para la materia '{cod_materia}' (encoded: {valor_encoded}) en los datos de inferencia.")
        return pd.DataFrame(), list_matricula  # Retornar DataFrame vacío y lista original de matrículas

    # MANTENER ORDEN: Crear DataFrame vacío para resultados ordenados
    df_ordenado = pd.DataFrame()
    matriculas_encontradas = []
    matriculas_no_encontradas = []
    
    # Iterar por la lista de matrículas EN EL ORDEN ORIGINAL
    for matricula in list_matricula:
        matricula_str = str(matricula).strip()
        fila = df_materia[df_materia['COD_ESTUDIANTE'].str.strip() == matricula_str]
        
        if len(fila) > 0:
            df_ordenado = pd.concat([df_ordenado, fila], ignore_index=True)
            matriculas_encontradas.append(matricula_str)
        else:
            matriculas_no_encontradas.append(matricula_str)
    
    print(f"📊 Matrículas encontradas ({len(matriculas_encontradas)}): {matriculas_encontradas}")
    if matriculas_no_encontradas:
        print(f"⚠️ Matrículas NO encontradas ({len(matriculas_no_encontradas)}): {matriculas_no_encontradas}")
    
    # Verificar si encontramos estudiantes
    if df_ordenado.shape[0] == 0:
        return f"No se encontraron estudiantes para la materia '{cod_materia}' con las matrículas proporcionadas: {list_matricula}."
    
    return df_ordenado, matriculas_no_encontradas


def predict_academic_risk(modelo, feature_info, df_datos=None, return_dataframe=True):
    """
    Realiza predicciones de riesgo académico
    
    Args:
        df_datos (DataFrame): Datos para predicción (opcional)
        data_file_path (str): Ruta al archivo de datos (opcional)
        return_dataframe (bool): Si retornar DataFrame completo con resultados
    
    Returns:
        dict: Resultados de la predicción
    """
    # # Buscar modelo si no se especifica ID
    # if model_id is None:
    #     academic_models = [k for k, v in loaded_models.items() if v['type'] == 'academic_risk']
    #     if not academic_models:
    #         raise ValueError("No hay modelos de riesgo académico cargados")
    #     model_id = academic_models[0]
    #     print(f"📍 Usando modelo: {model_id}")
    
    # if model_id not in loaded_models:
    #     raise ValueError(f"Modelo {model_id} no está cargado")
    
    # model_data = loaded_models[model_id]
    # if model_data['type'] != 'academic_risk':
    #     raise ValueError(f"Modelo {model_id} no es de tipo 'academic_risk'")
    
    # Cargar datos de inferencia
    if df_datos is not None:
        print("📊 Usando DataFrame proporcionado")
        df_inferencia = df_datos.copy()
        df_inferencia = df_inferencia.reset_index(drop=True)
    else:
        return ValueError("Debe proporcionar un DataFrame de datos para inferencia")
    
    if len(df_inferencia) == 0:
        raise ValueError("No hay datos disponibles para inferencia")
    
    print(f"   ✅ Datos cargados: {len(df_inferencia)} registros")
    
    # Extraer features
    # X_columns = model_data['feature_info']['X_columns']
    X_columns = feature_info['X_columns']
    
    
    # Verificar que todas las columnas necesarias estén presentes
    missing_columns = [col for col in X_columns if col not in df_inferencia.columns]
    if missing_columns:
        raise ValueError(f"Columnas faltantes en los datos: {missing_columns}")
    
    X_inferencia = df_inferencia[X_columns]
    
    # Realizar predicciones
    print(f"🔮 Realizando predicciones con {len(X_inferencia)} registros...")
    
    # model = model_data['model']
    model = modelo
    predicciones = model.predict(X_inferencia)
    
    results = {
        'predictions': predicciones.tolist() if hasattr(predicciones, 'tolist') else predicciones,
        # 'model_name': model_data['model_name'],
        'total_records': len(X_inferencia),
        # 'features_used': X_columns
    }
    
    # Calcular probabilidades si es posible
    probabilities = None
    if hasattr(model, 'predict_proba'):
        try:
            probabilities = model.predict_proba(X_inferencia)[:, 1]  # Probabilidad de aprobar
            results['probabilities'] = probabilities.tolist() if hasattr(probabilities, 'tolist') else probabilities
            # menor igual que
            tmp_categoria_riesgo = pd.cut(probabilities, bins=[0, Q1_RIESGO_ACADEMICO, Q2_RIESGO_ACADEMICO, Q3_RIESGO_ACADEMICO, 1], labels=['MUY POCO PROBABLE', 'POCO PROBABLE', 'PROBABLE APROBACIÓN', 'MUY PROBABLE APROBACIÓN'])
            print("** tmp_categoria_riesgo", type(tmp_categoria_riesgo))
            results["CATEGORIA_RIESGO"] = tmp_categoria_riesgo.to_list()
            results["RANGO"] = [Q1_RIESGO_ACADEMICO, Q2_RIESGO_ACADEMICO, Q3_RIESGO_ACADEMICO]
            print(f"   ✅ Probabilidades calculadas")
        except Exception as e:
            print(f"   ⚠️ No se pudieron calcular probabilidades: {e}")
    
    # matriculas_originales = df_inferencia['COD_ESTUDIANTE'].tolist()
    # results['students_code'] = matriculas_originales
    
    # Crear DataFrame de resultados si se solicita
    if return_dataframe:
        df_result = df_inferencia.copy()
        df_result['PREDICCION'] = predicciones
        df_result['PREDICCION_TEXTO'] = [
            'APROBARÁ' if pred == 1 else 'REPROBARÁ' for pred in predicciones
        ]
        
        if probabilities is not None:
            df_result['PROB_APROBAR'] = probabilities    
            # Categorías de riesgo
            df_result['CATEGORIA_RIESGO'] = tmp_categoria_riesgo
        
        # results['dataframe'] = df_result
    
    # Calcular estadísticas
    stats = {
        'total_estudiantes': len(predicciones),
        'pred_aprobar': int((predicciones == 1).sum()),
        'pred_reprobar': int((predicciones == 0).sum()),
        'pct_aprobar': float((predicciones == 1).mean() * 100),
        'pct_reprobar': float((predicciones == 0).mean() * 100)
    }
    
    if probabilities is not None:
        stats.update({
            'prob_promedio': float(probabilities.mean()),
            'prob_std': float(probabilities.std()),
            'prob_min': float(probabilities.min()),
            'prob_max': float(probabilities.max())
        })
        
        # Estadísticas por categoría de riesgo
        if return_dataframe and 'CATEGORIA_RIESGO' in df_result.columns:
            risk_stats = df_result['CATEGORIA_RIESGO'].value_counts().to_dict()
            stats['distribucion_riesgo'] = risk_stats
    
    results['statistics'] = stats
    
    print(f"   ✅ Predicciones completadas")
    print(f"   📊 {stats['pred_aprobar']} estudiantes aprobarán ({stats['pct_aprobar']:.2f}%)")
    print(f"   📊 {stats['pred_reprobar']} estudiantes reprobarán ({stats['pct_reprobar']:.2f}%)")
    
    return results
