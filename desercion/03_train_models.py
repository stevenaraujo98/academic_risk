import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, mean_squared_error, r2_score, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import json

df = pd.read_csv('./data/desercion/merge/desercion_analisis.csv', low_memory=False)

print("Forma del dataset:", df.shape)
print("\nColumnas:", df.columns.tolist())
print("\nPrimeras filas:")
print(df.head())

print("\nVariable objetivo 'desercion':")
print(df['desercion'].value_counts())

columns_to_drop = ['COD_ESTUDIANTE', 'IDPERIODO', 'IDPERSONA', 'FECHACREACION', 
                   'FECHAENVIOUBEP', 'FECHAENVIO', 'CODESTUDIANTE', 'APELLIDOS', 
                   'NOMBRES', 'EMAIL', 'NUMEROIDENTIFICACION', 'FECHANACIMIENTO',
                   'TELEFONOCELULAR', 'TELEFONOFIJO', 'CORREOALTERNO', 'DIRECCION', 'TIPOCOLEGIO_y'
                   'COORDENADAS', 'DIRECCIONVIVSEP', 'TIEMPOPROMEDIOCAMINATAENTRADAESPOL', 'TIEMPOPROMEDIOBICICLETASALIDAESPOL', 'TIEMPOPROMEDIOCAMINATASALIDAESPOL']

df_clean = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

print("\nValores nulos por columna:")
print(df_clean.isnull().sum()[df_clean.isnull().sum() > 0])

threshold = 0.5
df_clean = df_clean.loc[:, df_clean.isnull().mean() < threshold]

for col in df_clean.select_dtypes(include=['object']).columns:
    if col != 'desercion':
        df_clean[col].fillna(df_clean[col].mode()[0] if not df_clean[col].mode().empty else 'DESCONOCIDO', inplace=True)

for col in df_clean.select_dtypes(include=[np.number]).columns:
    df_clean[col].fillna(df_clean[col].median(), inplace=True)

label_encoders = {}
categorical_columns = df_clean.select_dtypes(include=['object']).columns.tolist()
if 'desercion' in categorical_columns:
    categorical_columns.remove('desercion')

print("\nCodificando variables categóricas...")
for col in categorical_columns:
    le = LabelEncoder()
    df_clean[col] = le.fit_transform(df_clean[col].astype(str))
    label_encoders[col] = le
    print(f"  {col}: {len(le.classes_)} categorías")

if 'desercion' in df_clean.columns:
    le_target = LabelEncoder()
    df_clean['desercion'] = le_target.fit_transform(df_clean['desercion'])
    label_encoders['desercion'] = le_target
    print(f"\nVariable objetivo 'desercion' codificada: {dict(zip(le_target.classes_, le_target.transform(le_target.classes_)))}")

os.makedirs('./models', exist_ok=True)
os.makedirs('./results', exist_ok=True)
os.makedirs('./results_desercion/confusion_matrices', exist_ok=True)

with open('./models_desercion/label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)
print("\nLabel encoders guardados en './models_desercion/label_encoders.pkl'")

X = df_clean.drop('desercion', axis=1)
y = df_clean['desercion']

print(f"\nForma de X: {X.shape}")
print(f"Forma de y: {y.shape}")
print(f"Distribución de clases: {np.bincount(y)}")

X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp)

print(f"\nConjunto de entrenamiento: {X_train.shape}")
print(f"Conjunto de validación: {X_val.shape}")
print(f"Conjunto de prueba: {X_test.shape}")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

with open('./models_desercion/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("\nScaler guardado en './models_desercion/scaler.pkl'")

models = {
    'Regresion_Lineal': LinearRegression(),
    'Regresion_Logistica': LogisticRegression(max_iter=1000, random_state=42),
    # 'SVM': SVC(kernel='rbf', random_state=42),
    'Random_Forest': RandomForestClassifier(n_estimators=1000, random_state=42, )
}

results = {}
all_accuracies = {}

print("\n" + "="*80)
print("ENTRENAMIENTO DE MODELOS")
print("="*80)

for name, model in models.items():
    print(f"\n{'='*80}")
    print(f"Entrenando: {name}")
    print(f"{'='*80}")
    
    if name == 'Regresion_Lineal':
        model.fit(X_train_scaled, y_train)
        
        y_train_pred = model.predict(X_train_scaled)
        y_val_pred = model.predict(X_val_scaled)
        y_test_pred = model.predict(X_test_scaled)
        
        y_train_pred_class = np.round(y_train_pred).astype(int)
        y_val_pred_class = np.round(y_val_pred).astype(int)
        y_test_pred_class = np.round(y_test_pred).astype(int)
        
        train_mse = mean_squared_error(y_train, y_train_pred)
        val_mse = mean_squared_error(y_val, y_val_pred)
        test_mse = mean_squared_error(y_test, y_test_pred)
        
        train_r2 = r2_score(y_train, y_train_pred)
        val_r2 = r2_score(y_val, y_val_pred)
        test_r2 = r2_score(y_test, y_test_pred)
        
        train_acc = accuracy_score(y_train, y_train_pred_class)
        val_acc = accuracy_score(y_val, y_val_pred_class)
        test_acc = accuracy_score(y_test, y_test_pred_class)
        
        print(f"\nMétricas de Entrenamiento:")
        print(f"  MSE: {train_mse:.4f}")
        print(f"  R²: {train_r2:.4f}")
        print(f"  Accuracy: {train_acc:.4f}")
        
        print(f"\nMétricas de Validación:")
        print(f"  MSE: {val_mse:.4f}")
        print(f"  R²: {val_r2:.4f}")
        print(f"  Accuracy: {val_acc:.4f}")
        
        print(f"\nMétricas de Prueba:")
        print(f"  MSE: {test_mse:.4f}")
        print(f"  R²: {test_r2:.4f}")
        print(f"  Accuracy: {test_acc:.4f}")
        
        results[name] = {
            'train_mse': train_mse,
            'val_mse': val_mse,
            'test_mse': test_mse,
            'train_r2': train_r2,
            'val_r2': val_r2,
            'test_r2': test_r2,
            'train_accuracy': train_acc,
            'val_accuracy': val_acc,
            'test_accuracy': test_acc
        }
        
        all_accuracies[name] = {
            'train': train_acc,
            'validation': val_acc,
            'test': test_acc
        }
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        cm_train = confusion_matrix(y_train, y_train_pred_class)
        cm_val = confusion_matrix(y_val, y_val_pred_class)
        cm_test = confusion_matrix(y_test, y_test_pred_class)
        
        sns.heatmap(cm_train, annot=True, fmt='d', cmap='Blues', ax=axes[0])
        axes[0].set_title(f'{name} - Entrenamiento\nAccuracy: {train_acc:.4f}')
        axes[0].set_ylabel('Real')
        axes[0].set_xlabel('Predicción')
        
        sns.heatmap(cm_val, annot=True, fmt='d', cmap='Blues', ax=axes[1])
        axes[1].set_title(f'{name} - Validación\nAccuracy: {val_acc:.4f}')
        axes[1].set_ylabel('Real')
        axes[1].set_xlabel('Predicción')
        
        sns.heatmap(cm_test, annot=True, fmt='d', cmap='Blues', ax=axes[2])
        axes[2].set_title(f'{name} - Prueba\nAccuracy: {test_acc:.4f}')
        axes[2].set_ylabel('Real')
        axes[2].set_xlabel('Predicción')
        
        plt.tight_layout()
        plt.savefig(f'./results_desercion/confusion_matrices/{name}_confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\nMatriz de confusión guardada en './results_desercion/confusion_matrices/{name}_confusion_matrix.png'")
        
    else:
        model.fit(X_train_scaled, y_train)
        
        y_train_pred = model.predict(X_train_scaled)
        y_val_pred = model.predict(X_val_scaled)
        y_test_pred = model.predict(X_test_scaled)
        
        train_acc = accuracy_score(y_train, y_train_pred)
        val_acc = accuracy_score(y_val, y_val_pred)
        test_acc = accuracy_score(y_test, y_test_pred)
        
        print(f"\nAccuracy Entrenamiento: {train_acc:.4f}")
        print(f"Accuracy Validación: {val_acc:.4f}")
        print(f"Accuracy Prueba: {test_acc:.4f}")
        
        print(f"\nReporte de Clasificación (Conjunto de Prueba):")
        print(classification_report(y_test, y_test_pred))
        
        print(f"\nMatriz de Confusión (Conjunto de Prueba):")
        print(confusion_matrix(y_test, y_test_pred))
        
        results[name] = {
            'train_accuracy': train_acc,
            'val_accuracy': val_acc,
            'test_accuracy': test_acc
        }
        
        all_accuracies[name] = {
            'train': train_acc,
            'validation': val_acc,
            'test': test_acc
        }
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        cm_train = confusion_matrix(y_train, y_train_pred)
        cm_val = confusion_matrix(y_val, y_val_pred)
        cm_test = confusion_matrix(y_test, y_test_pred)
        
        sns.heatmap(cm_train, annot=True, fmt='d', cmap='Blues', ax=axes[0])
        axes[0].set_title(f'{name} - Entrenamiento\nAccuracy: {train_acc:.4f}')
        axes[0].set_ylabel('Real')
        axes[0].set_xlabel('Predicción')
        
        sns.heatmap(cm_val, annot=True, fmt='d', cmap='Blues', ax=axes[1])
        axes[1].set_title(f'{name} - Validación\nAccuracy: {val_acc:.4f}')
        axes[1].set_ylabel('Real')
        axes[1].set_xlabel('Predicción')
        
        sns.heatmap(cm_test, annot=True, fmt='d', cmap='Blues', ax=axes[2])
        axes[2].set_title(f'{name} - Prueba\nAccuracy: {test_acc:.4f}')
        axes[2].set_ylabel('Real')
        axes[2].set_xlabel('Predicción')
        
        plt.tight_layout()
        plt.savefig(f'./results_desercion/confusion_matrices/{name}_confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"\nMatriz de confusión guardada en './results_desercion/confusion_matrices/{name}_confusion_matrix.png'")
    
    model_filename = f'./models_desercion/{name}.pkl'
    with open(model_filename, 'wb') as f:
        pickle.dump(model, f)
    print(f"\nModelo guardado en '{model_filename}'")

with open('./results_desercion/accuracies.json', 'w') as f:
    json.dump(all_accuracies, f, indent=4)
print("\n" + "="*80)
print("Accuracies guardados en './results_desercion/accuracies.json'")

fig, ax = plt.subplots(figsize=(12, 6))
model_names = list(all_accuracies.keys())
train_accs = [all_accuracies[m]['train'] for m in model_names]
val_accs = [all_accuracies[m]['validation'] for m in model_names]
test_accs = [all_accuracies[m]['test'] for m in model_names]

x = np.arange(len(model_names))
width = 0.25

bars1 = ax.bar(x - width, train_accs, width, label='Entrenamiento', color='#2ecc71')
bars2 = ax.bar(x, val_accs, width, label='Validación', color='#3498db')
bars3 = ax.bar(x + width, test_accs, width, label='Prueba', color='#e74c3c')

ax.set_xlabel('Modelos', fontsize=12, fontweight='bold')
ax.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
ax.set_title('Comparación de Accuracy por Modelo', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(model_names, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('./results_desercion/accuracy_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("Gráfico de comparación guardado en './results_desercion/accuracy_comparison.png'")

print("\n" + "="*80)
print("RESUMEN DE RESULTADOS")
print("="*80)
for name, metrics in results.items():
    print(f"\n{name}:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")

print("\n" + "="*80)
print("ENTRENAMIENTO COMPLETADO")
print("="*80)
print("\nArchivos guardados:")
print("  - ./models_desercion/label_encoders.pkl")
print("  - ./models_desercion/scaler.pkl")
for name in models.keys():
    print(f"  - ./models_desercion/{name}.pkl")
    print(f"  - ./results_desercion/confusion_matrices/{name}_confusion_matrix.png")
print("  - ./results_desercion/accuracies.json")
print("  - ./results_desercion/accuracy_comparison.png")
