tamano = int(input("Ingrese el tamaño del Cuadro impar: "))
if tamano % 2 == 0:
    print("El tamaño debe ser un número impar.")
    exit()
numero_magico = tamano * (pow(tamano,2) + 1) // 2
print(f"Número mágico: {numero_magico}")
centro = tamano // 2
cuadro = [[0]*tamano for i in range(tamano)]

num = 1
fila = 0
columna = centro
cuadro[fila][columna] = num

for _ in range(tamano*tamano - 1):
    num += 1
    ubifila, ubicolumna = fila, columna

    # intento moverse arriba-izquierda
    fila -= 1
    columna -= 1

    # wrap-around si salimos
    if fila < 0: fila = tamano - 1
    if columna < 0: columna = tamano - 1

    if cuadro[fila][columna] == 0:
        cuadro[fila][columna] = num
    else:
        # si está ocupada, mover una fila abajo desde la posición previa
        fila = ubifila + 1
        if fila >= tamano:
            fila = 0
        columna = ubicolumna
        cuadro[fila][columna] = num

# imprimir
for fila in cuadro:
    for r in fila:
        print(f"{r:4d}", end="")
    print()
  
