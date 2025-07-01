
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

# Cargar historial desde Excel
df = pd.read_excel("historial_apuestas.xlsx")

# Preprocesar columnas categóricas
df['Deporte'] = df['Deporte'].fillna("Desconocido")
df['Tiempo'] = df['Tiempo'].fillna("Desconocido")
df['Mejor Resultado'] = df['Mejor Resultado'].fillna("Desconocido")

le_deporte = LabelEncoder()
le_tiempo = LabelEncoder()
le_resultado = LabelEncoder()

df['Deporte_cod'] = le_deporte.fit_transform(df['Deporte'])
df['Tiempo_cod'] = le_tiempo.fit_transform(df['Tiempo'])
df['Resultado_cod'] = le_resultado.fit_transform(df['Mejor Resultado'])

# Selección de características
X = df[['Cuota X', 'Cuota Empate', 'Cuota Y', 'ROI %', 'Deporte_cod', 'Tiempo_cod']]
y = df['Resultado_cod']

# División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Evaluación
y_pred = modelo.predict(X_test)
print(classification_report(y_test, y_pred, target_names=le_resultado.classes_))

# Guardar el modelo y los codificadores
joblib.dump(modelo, 'modelo_apuestas.pkl')
joblib.dump(le_resultado, 'label_resultado.pkl')
joblib.dump(le_deporte, 'label_deporte.pkl')
joblib.dump(le_tiempo, 'label_tiempo.pkl')

print("✅ Modelo entrenado y guardado exitosamente.")
