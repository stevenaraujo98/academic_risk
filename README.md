# Codigos de riesgos academicos

#### Codigos:
- script_pdf.ipynb: trabaja con el data set de [Student Performance](https://archive.ics.uci.edu/dataset/320/student+performance) y usando como referencia Predicción de Rendimiento Académico de alumnos usando Machine Learning de la universidad de LIMA.  


#### Mas datasets:
- [Predict Students' Dropout and Academic Success](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success)
- [Higher Education Students Performance Evaluation](https://archive.ics.uci.edu/dataset/856/higher+education+students+performance+evaluation)
- [Assessing Mathematics Learning in Higher Education](https://archive.ics.uci.edu/dataset/1031/dataset+for+assessing+mathematics+learning+in+higher+education)


#### Pasos
0. Descargar los valores de tasa de reprobacion y dificultad de matera. Con "3_download_data.ipynb" que lee con el query tasa_reprobacion se guarda en "./data/materias/tasa_reprobacion.csv" y dificultad_materia en "./data/materias/dificultad_materia.csv" y junto en "./data/materias/tasa_reprobacion_dificultad.csv" estos queries como base es tasa_reprobacion_dificultad##.sql
1. Descargar de todas las materias por año y termino usando el notebook "download_anio_semester_20##_#S.ipynb".
2. Asociarlo con su factor socioeconomico.
- Descargar manualmente en este caso "socioeconomico_17897.csv" usando "socioeconomico_##.sql".
3. Filtro 1.
4. Asociarlo con GPA.
- Descargar manualmente por año y termino en este casi "gpa_general_20##_#S.csv" usando "gpa_estudiante_general_##.sql".
- Esto analiza los que tienen y los que no GPA.
5. Los estudiantes que estudian el mismo año de ingreso quiere decir que son novatos, y se valida si tiene GPA.
6. Si siendo novato tiene GPA se aplica Filtro 2.
7. Para novatos se obtiene de la base DAGO su gpa del pre.
8. Se aplica el filtro 3.
9. Se filtra para estudiantes que realizaron savatico inmediatamente despues de ingresar.

#### Consideraciones de filtro
1. Se eliminan los estudiantes que ingresaron antes del 2006, para no tener estudiantes super resagados.
2. Los convalidados de antes de ingresar a primer termino, se modifica el GPA por el pre.
3. Se descartaron los estudiantes que no estan en admisiones pero si en semestre.
4. La columna TERMINOS_REGISTRADOS nos permite saber si es el primer semestre ya que existen estudiantes que se retiran despues de pasar el pre y esperan unos semestres para volver.

