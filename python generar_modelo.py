# Entrena y guarda un modelo compatible para apuestas

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 🧪 Datos simulados (puedes reemplazarlos con tus datos reales)
X = pd.DataFrame({
    'deporte': [0, 0, 1, 1, 0],  # Ej: 0 = fútbol, 1 = básquet
    'tiempo': [0, 1, 0, 1, 2],   # Ej: codificado (primer tiempo, segundo, etc.)
    'cuota_x': [1.2, 1.3, 1.25, 1.4, 1.5],
    'cuota_empate': [6.0, 6.5, 6.1, 6.3, 6.8],
    'cuota_y': [9.5, 9.8, 10.0, 9.7, 10.2]
})
y = [0, 1, 1, 0, 2]  # 0 = Gana X, 1 = Empate, 2 = Gana Y

# 🎯 Entrenar el modelo
modelo = RandomForestClassifier(n_estimators=10, random_state=42)
modelo.fit(X, y)

# 💾 Guardar el modelo
joblib.dump(modelo, 'modelo_apuestas.pkl')
print("✅ Modelo guardado como modelo_apuestas.pkl")
