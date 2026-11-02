# Documentos JSON y consultas MongoDB sobre clientes (Mongo Playground)

**Actividad:** RA1 — JSON y MongoDB  
**Plataforma:** [Mongo Playground](https://mongoplayground.net)

---

## Parte 1 — Documentos JSON (inserción)

Los 5 documentos cumplen todas las restricciones:

| Restricción | Clientes que la cumplen |
|-------------|------------------------|
| Al menos 1 cliente < 30 años | Ana (25), Carlos (22) |
| Al menos 2 clientes < 30 o de Madrid | Ana (25, Madrid), Carlos (22, Valencia) |
| Solo 3 clientes con compras > 100€ | Ana, Pedro, María |
| Al menos 1 compra de "Portátil" | Ana (Portátil 899.99€) |
| 1 cliente de ciudad distinta a Madrid/Barcelona/Sevilla | Carlos (Valencia) |

```javascript
db.clientes.insertMany([
  {
    "cliente_id": 1,
    "nombre": "Ana García",
    "edad": 25,
    "ciudad": "Madrid",
    "compras": [
      { "producto": "Portátil", "precio": 899.99, "fecha": "2024-03-15" },
      { "producto": "Ratón",    "precio": 29.99,  "fecha": "2024-03-20" }
    ]
  },
  {
    "cliente_id": 2,
    "nombre": "Pedro Martínez",
    "edad": 42,
    "ciudad": "Barcelona",
    "compras": [
      { "producto": "Teclado",  "precio": 149.99, "fecha": "2024-04-01" },
      { "producto": "Monitor",  "precio": 299.99, "fecha": "2024-04-10" }
    ]
  },
  {
    "cliente_id": 3,
    "nombre": "María López",
    "edad": 35,
    "ciudad": "Madrid",
    "compras": [
      { "producto": "Auriculares", "precio": 199.99, "fecha": "2024-02-14" }
    ]
  },
  {
    "cliente_id": 4,
    "nombre": "Carlos Ruiz",
    "edad": 22,
    "ciudad": "Valencia",
    "compras": [
      { "producto": "Cable USB", "precio": 9.99,  "fecha": "2024-05-01" },
      { "producto": "Funda",     "precio": 14.99, "fecha": "2024-05-03" }
    ]
  },
  {
    "cliente_id": 5,
    "nombre": "Laura Sánchez",
    "edad": 50,
    "ciudad": "Sevilla",
    "compras": [
      { "producto": "Impresora", "precio": 89.99, "fecha": "2024-01-20" }
    ]
  }
])
```

---

## Parte 2 — Consultas MongoDB (Mongo Playground)

### Consulta 1 — Clientes con alguna compra > 100€

```javascript
db.clientes.find({ "compras.precio": { $gt: 100 } })
```

**Explicación:**  
MongoDB puede buscar dentro de arrays de objetos directamente usando notación de punto (`compras.precio`). El operador `$gt` (greater than) compara el campo `precio` de cada elemento del array con 100. Si al menos uno de los elementos del array cumple la condición, el documento completo se devuelve. Esta consulta retorna Ana, Pedro y María — los tres clientes con al menos una compra superior a 100€, cumpliendo exactamente la restricción del ejercicio.

---

### Consulta 2 — Nombre y ciudad de compradores de "Portátil"

```javascript
db.clientes.find(
  { "compras.producto": "Portátil" },
  { nombre: 1, ciudad: 1, _id: 0 }
)
```

**Explicación:**  
El primer argumento de `find()` es el filtro: busca documentos donde el array `compras` tenga al menos un elemento con `producto` igual a `"Portátil"`. El segundo argumento es la **proyección**: `1` incluye el campo y `0` lo excluye. Al poner `_id: 0` se omite el identificador interno de MongoDB. El resultado contiene solo `nombre` y `ciudad`, devolviendo únicamente a Ana García de Madrid.

---

### Consulta 3 — Clientes de Madrid con edad > 30

```javascript
db.clientes.find({
  ciudad: "Madrid",
  edad: { $gt: 30 }
})
```

**Explicación:**  
Cuando se pasan múltiples condiciones en el mismo objeto de filtro, MongoDB las combina con un **AND implícito**: ambas condiciones deben cumplirse simultáneamente. `ciudad: "Madrid"` hace una comparación exacta de igualdad sobre el campo. `edad: { $gt: 30 }` filtra los mayores de 30 años. De los clientes de Madrid (Ana, 25; María, 35), solo María cumple ambas condiciones y es devuelta.

---

### Consulta 4 — Compras del cliente más joven

```javascript
db.clientes.find(
  {},
  { nombre: 1, edad: 1, compras: 1, _id: 0 }
).sort({ edad: 1 }).limit(1)
```

**Explicación:**  
Se ordena toda la colección por `edad` de forma ascendente (`1` = ascending), lo que pone al cliente más joven en primer lugar. `limit(1)` toma únicamente ese primer documento. La proyección incluye `nombre`, `edad` y `compras` para ver tanto quién es el cliente más joven (Carlos, 22 años) como sus compras. Esta técnica de sort+limit(1) es el patrón estándar en MongoDB para obtener el mínimo o el máximo de una colección.

---

### Consulta 5 — Clientes con al menos 2 compras

```javascript
db.clientes.find({
  $expr: { $gte: [{ $size: "$compras" }, 2] }
})
```

**Explicación:**  
`$size` devuelve el número de elementos en el array `$compras`. `$gte` (greater than or equal) compara ese número con 2. El operador `$expr` permite usar **expresiones de agregación** dentro de un filtro de `find()`, algo que operadores como `$gt` normales no permiten hacer sobre el tamaño de un array. Esta consulta devuelve Ana (2 compras), Pedro (2 compras) y Carlos (2 compras), excluyendo a María (1) y Laura (1).

---

## Verificación de restricciones

| Restricción | ¿Cumplida? | Justificación |
|-------------|-----------|---------------|
| ≥1 cliente < 30 años | ✓ | Ana (25), Carlos (22) |
| ≥2 clientes < 30 O de Madrid | ✓ | Ana (25, Madrid), Carlos (22), María (Madrid) |
| Exactamente 3 con compras > 100€ | ✓ | Ana (899.99), Pedro (149.99, 299.99), María (199.99) |
| ≥1 compra de "Portátil" | ✓ | Ana compró Portátil a 899.99€ |
| 1 ciudad ≠ Madrid/Barcelona/Sevilla | ✓ | Carlos vive en Valencia |
