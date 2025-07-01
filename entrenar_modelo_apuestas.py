
# Contenido del script entrenar_modelo_apuestas.py
# Este archivo contiene el código para entrenar un modelo de apuestas.
# Puedes copiar y pegar el código completo de tu celda de Colab aquí
# para tener una copia descargable.

# Importar las librerías necesarias
import pandas as pd
import numpy as np
import joblib
import io
from google.colab import files

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Carga del Dataset desde Google Colab ---
print("--- Paso 1: Carga del Dataset ---")
print("Por favor, sube tu archivo CSV con los datos de entrenamiento (ej. 'dataset_apuestas_simulado.csv'):")
uploaded = files.upload()
if uploaded:
    file_name = list(uploaded.keys())[0]
    print(f"✅ Archivo '{file_name}' subido exitosamente.")
    df = pd.read_csv(io.BytesIO(uploaded[file_name]))
    print("\nPrimeras 5 filas del dataset cargado:")
    print(df.head())
    print(f"\nDimensiones del dataset: {df.shape[0]} filas, {df.shape[1]} columnas")
else:
    print("❌ No se subió ningún archivo. El script finalizará.")
    exit()

# --- 2. Separar Variables (Características X y Variable Objetivo y) ---
print("\n--- Paso 2: Separación de Variables ---")
target_column = "target"
if target_column not in df.columns:
    print(f"❌ Error: La columna '{target_column}' no se encontró en el dataset. Por favor, verifica el nombre.")
    print(f"Columnas disponibles: {df.columns.tolist()}")
    exit()
X = df.drop(target_column, axis=1)
y = df[target_column]
print(f"Características (X) shape: {X.shape}")
print(f"Variable Objetivo (y) shape: {y.shape}")
print(f"Características usadas: {X.columns.tolist()}")

# --- 3. División de Datos en Entrenamiento y Prueba ---
print("\n--- Paso 3: División de Datos (Entrenamiento y Prueba) ---")
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
print(f"Tamaño del conjunto de entrenamiento: {X_train.shape[0]} muestras")
print(f"Tamaño del conjunto de prueba: {X_test.shape[0]} muestras")

# --- 4. Entrenamiento del Modelo con Búsqueda de Hiperparámetros (GridSearchCV) ---
print("\n--- Paso 4: Entrenamiento del Modelo y Optimización de Hiperparámetros ---")
param_grid = {
    "n_estimators": [100, 200, 300],
    "max_depth": [None, 10, 20, 30],
    "min_samples_leaf": [1, 2, 4, 8]
}
model = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(model, param_grid, cv=5, n_jobs=-1, verbose=2)
print("Iniciando GridSearchCV para encontrar los mejores hiperparámetros...")
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
print(f"\n✅ Entrenamiento completado. Mejores parámetros encontrados: {grid_search.best_params_}")
print(f"Mejor puntuación de validación cruzada: {grid_search.best_score_:.4f}")

# --- 5. Evaluación del Modelo ---
print("\n--- Paso 5: Evaluación del Modelo ---")
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión (Accuracy) en el conjunto de prueba: {accuracy:.4f}")
class_names = ["Gana Local", "Empate", "Gana Visitante"]
print("\nReporte de Clasificación:")
print(classification_report(y_test, y_pred, target_names=class_names))
print("\nMatriz de Confusión:")
cm = confusion_matrix(y_test, y_pred)
print(cm)
# plt.figure(figsize=(8, 6))
# sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=class_names, yticklabels=class_names)
# plt.title("Matriz de Confusión")
# plt.xlabel("Etiqueta Predicha")
# plt.ylabel("Etiqueta Verdadera")
# plt.show()

# --- 6. Análisis de Importancia de Características ---
print("\n--- Paso 6: Análisis de Importancia de Características ---")
feature_importances = best_model.feature_importances_
features = X.columns
importance_df = pd.DataFrame({'Feature': features, 'Importance': feature_importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)
print("\nImportancia de las características:")
print(importance_df)
# plt.figure(figsize=(10, 7))
# sns.barplot(x='Importance', y='Feature', data=importance_df, palette='viridis')
# plt.title('Importancia de las Características en RandomForest')
# plt.xlabel('Importancia')
# plt.ylabel('Característica')
# plt.show()

# --- 7. Guardar el Modelo Entrenado ---
print("\n--- Paso 7: Guardar el Modelo Entrenado ---")
model_filename = "modelo_apuestas_optimizado.pkl"
joblib.dump(best_model, model_filename)
print(f"✅ Modelo guardado como '{model_filename}' en Google Colab.")

# --- 8. Descargar el Modelo desde Google Colab ---
print(f"\n--- Paso 8: Descargando el modelo '{model_filename}' a tu computadora ---")
files.download(model_filename)
print("✅ Descarga del modelo completada. Revisa la carpeta de descargas de tu navegador.")
