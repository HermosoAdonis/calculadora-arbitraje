import joblib
from sklearn.preprocessing import LabelEncoder

# Codificadores con clases estándar
le_resultado = LabelEncoder()
le_resultado.fit(["Gana X", "Empate", "Gana Y"])
joblib.dump(le_resultado, "label_resultado.pkl")

le_deporte = LabelEncoder()
le_deporte.fit(["⚽ Fútbol", "🏀 Básquetbol"])
joblib.dump(le_deporte, "label_deporte.pkl")

le_tiempo = LabelEncoder()
le_tiempo.fit([
    "Primer tiempo", "Segundo tiempo", "Primer tiempo extra", "Segundo tiempo extra", "Penales",
    "Primer cuarto", "Segundo cuarto", "Tercer cuarto", "Último cuarto", "Tiempo extra"
])
joblib.dump(le_tiempo, "label_tiempo.pkl")

print("✅ Codificadores guardados correctamente")
