# Planificacion de desercion

## Variables del modelo actual
features_numericas = [
    'VEZ_x_DIFICULTAD', 
    'MAT_APROBADAS', 
    'PROM_CALIF_APROBADAS', 'TERMINOS_REGISTRADOS',
    'PROM_MAT_REPROBADAS1', 'PROM_MAT_REPROBADAS2', 'PROM_MAT_REPROBADAS3',
    'MUY_FACIL', 'FACIL', 'MODERADA', 'DIFICIL', 'MUY_DIFICIL', 
    'PORCENTAJEDISCAPACIDAD', "NUMERO_IDIOMAS", 
    'VECESBUSENTRADA', 'VECESBUSSALIDA', 'CANTIDADCUARTOS', 'CANTIDADBANIO', 
    'edad_ingreso',
    'RATIO_APROBADAS', 
    'TASA_REPROBACION',
    'LOG_CANT_MAT', 'GPA_CUADRADO', 'LOG_GASTOS_RUBRO'
]

features_categoricas = [
    'TIPOCOLEGIO', 'BECACOLEGIO', 'COD_MATERIA_ACAD_MO',
    'TIENEDISCAPACIDAD', 'TIPODISCAPACIDAD', 'ESTADOCIVIL', 'OTROSIDIOMAS', 
    'TIEMPOPROMEDIOLLEGARESPOL', 'NIVELINGLES', 
    'NIVELINSTRUCCIONPADRE', 'NIVELINSTRUCCIONMADRE', 'ESTADOCIVILPADRES',
    'FAMILIARDISCAPACIDAD', 'FAMILIARENFERMEDAD', 'TIPOPARROQUIA',
    'VIVEGRUPOFAMILIAR', 'SEXO', "PERDIO_CARRERA", 'termino'
]

["COD_ESTUDIANTE"] + features_numericas + features_categoricas + ['anio', 'APROBO']

## Variables que se van a actualizar:
1. df_merge_gpa_real_novatos['RATIO_APROBADAS'] = np.log(df_merge_gpa_real_novatos['MAT_APROBADAS'] / (df_merge_gpa_real_novatos['T_MAT_TOMADAS'] + 1))
2. df_merge_gpa_real_novatos['TASA_REPROBACION'] = df_merge_gpa_real_novatos['PROM_MAT_REPROBADAS1'] / (df_merge_gpa_real_novatos['T_MAT_TOMADAS'] + 1)

## Especificación del nuevo subproyecto

Este subproyecto tiene como objetivo obtener la probabilidad de que los estudiantes aprueben una materia específica utilizando un modelo de aprendizaje automático.

### Proceso
1. **Obtener estudiantes actualmente viendo la materia**: Utilizar el query en `database\planificacion_aprobacion\estudiantes_actualmente_viendo.sql` para obtener la lista de estudiantes que están inscritos en la materia con el código específico (por ejemplo, `CCPG1052`) en un año y término determinados. Es importante filtrar los resultados por carrera.

2. **Obtener lista de pre-requisitos y co-requisitos**: Ejecutar el query en `database\planificacion_aprobacion\corequisito_prerequisito_materias.sql` para obtener la lista de materias que son pre-requisitos y co-requisitos de la materia en cuestión. También se debe dividir esta información por carrera.

3. **Cargar el modelo de predicción**: Con la lista de estudiantes obtenida, cargar el modelo `models/random_forest_model.pkl`, así como los `label_encoders` y `feature_info` necesarios para la predicción.

4. **Calcular la probabilidad de aprobación**: A partir de la lista de estudiantes, utilizar el modelo para obtener la probabilidad de que cada estudiante apruebe la materia.

### Notas
- Asegurarse de que todos los datos estén correctamente preprocesados antes de realizar las predicciones.
- Documentar cualquier cambio en el modelo o en los datos utilizados para la predicción.


