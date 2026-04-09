import pandas as pd
import random
from datetime import datetime, timedelta

clientes = [
    "TechFix SA", "Romandie Services", "Alpine Mechanics",
    "Swiss Industrial Co", "Helvetic Repair",
    "Montreux Solutions", "Zurich Maintenance", "Ticino Tech"
]

zonas = ["Romandie", "Suisse Centrale", "Zürich Area", "Ticino"]

productos = {
    "Taladro industrial": ("Equipos", 800, 650),
    "Llave inglesa": ("Herramientas", 70, 40),
    "Filtros técnicos": ("Consumibles", 50, 20),
    "Lubricantes": ("Consumibles", 30, 10),
    "Kit mantenimiento": ("Repuestos", 120, 70),
    "Compresor": ("Equipos", 2000, 1700),
    "Sensor presión": ("Repuestos", 300, 180),
    "Válvula hidráulica": ("Repuestos", 400, 250)
}

rows = []

start_date = datetime(2025, 1, 1)

for i in range(300):
    fecha = start_date + timedelta(days=random.randint(0, 120))
    cliente = random.choice(clientes)
    zona = random.choice(zonas)

    producto = random.choice(list(productos.keys()))
    categoria, precio, coste = productos[producto]

    unidades = random.randint(1, 20)

    ventas = unidades * precio
    costes = unidades * coste
    margen = ventas - costes

    rows.append([
        fecha.strftime("%Y-%m-%d"), cliente, zona, producto,
        categoria, unidades, precio, coste, ventas, costes, margen
    ])

df = pd.DataFrame(rows, columns=[
    "fecha","cliente","zona","producto","categoria",
    "unidades","precio_unitario","coste_unitario",
    "ventas","costes","margen"
])

import pandas as pd

df = pd.read_csv("alpine_supplies.csv", encoding="utf-8")
df.to_csv("alpine_supplies_clean.csv", index=False, encoding="utf-8-sig")
