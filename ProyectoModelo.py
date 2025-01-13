import pulp
import matplotlib.pyplot as plt

# Datos del problema
n = 10  # Número de proyectos
beneficios = [100, 200, 150, 300, 250, 400, 350, 500, 450, 600]  # Beneficio de cada proyecto
costos = [50, 80, 60, 100, 90, 120, 110, 140, 130, 160]  # Costo de cada proyecto
presupuesto_total = 700  # Presupuesto total
recursos = [60, 80, 70, 90, 85, 100, 95, 110, 105, 120]  # Horas requeridas por proyecto
recurso_total = 800  # Total de horas disponibles


# Crear el modelo extendido
modelo = pulp.LpProblem("Planificación_de_Inversiones_Extendida", pulp.LpMaximize)

# Variables de decisión (binarias: 1 si el proyecto se selecciona, 0 si no)
x = [pulp.LpVariable(f"x_{i}", cat="Binary") for i in range(n)]

# Función objetivo: Maximizar el beneficio total
modelo += pulp.lpSum(beneficios[i] * x[i] for i in range(n)), "Beneficio_Total"

# Restricciones
# Restricción de presupuesto
modelo += pulp.lpSum(costos[i] * x[i] for i in range(n)) <= presupuesto_total, "Presupuesto"
# Restricción de recurso disponible
modelo += pulp.lpSum(recursos[i] * x[i] for i in range(n)) <= recurso_total, "Recurso"

# Resolver el problema
modelo.solve()

# Resultados
print("Estado del modelo:", pulp.LpStatus[modelo.status])
print("Beneficio total óptimo:", pulp.value(modelo.objective))
print("Proyectos seleccionados:")

for i in range(n):
    if x[i].value() == 1:
        print(f" - Proyecto {i + 1} (Beneficio: {beneficios[i]}, Costo: {costos[i]}, Recurso: {recursos[i]})")

# Resultados para visualización
proyectos = [f"P{i+1}" for i in range(n)]
seleccionados = [x[i].value() for i in range(n)]

# Crear la gráfica
plt.figure(figsize=(12, 8))
bars = plt.bar(proyectos, seleccionados, color="skyblue")

# Agregar etiquetas a las barras
for i, bar in enumerate(bars):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, f"{int(yval)}\nB: {beneficios[i]}\nC: {costos[i]}\nR: {recursos[i]}", 
             ha='center', va='bottom', fontsize=10) 

plt.title("Proyectos Seleccionados")
plt.ylabel("Seleccionado (1=Sí, 0=No)")
plt.xlabel("Proyectos")
plt.ylim(0, 1.5)  # Ajustar el límite del eje y para mejor visualización
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()