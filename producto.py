import os
import json
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Producto:
    """
    Clase base para los productos.
    """
    id: str
    nombre: str
    precio: float
    categoria: str
    stock: int

    def mostrar_detalles(self):
        return f"{self.id:<10} {self.nombre:<20} {self.precio:<10.2f} {self.categoria:<15} {self.stock:<10}"

    def actualizar_stock(self, cantidad):
        if cantidad <= self.stock:
            self.stock -= cantidad
            return True
        return False


@dataclass
class ProductoEspecial(Producto):
    """
    Clase derivada para productos especiales que tienen descuento.
    """
    descuento: float

    def calcular_precio_final(self):
        return self.precio * (1 - self.descuento)


class ProductoManager:
    """
    Clase encargada de gestionar los productos.
    """
    def __init__(self, archivo="productos.txt"):
        self.archivo = archivo

    def cargar_productos(self):
        """Carga los productos desde el archivo."""
        if not os.path.exists(self.archivo):
            return []
        try:
            with open(self.archivo, 'r') as archivo:
                return [Producto(**producto) if 'descuento' not in producto else ProductoEspecial(**producto) for producto in json.load(archivo)]
        except json.JSONDecodeError:
            print("Error al leer el archivo de productos.")
            return []

    def guardar_productos(self, productos):
        """Guarda los productos en el archivo."""
        with open(self.archivo, 'w') as archivo:
            json.dump([producto.__dict__ for producto in productos], archivo, indent=4)

    def registrar_producto(self, nuevo_producto):
        """Registra un nuevo producto en el archivo."""
        productos = self.cargar_productos()
        if any(producto.id == nuevo_producto.id for producto in productos):
            print("ERROR: Ya existe un producto con ese ID.")
            return
        productos.append(nuevo_producto)
        self.guardar_productos(productos)
        print(f"Producto '{nuevo_producto.nombre}' registrado exitosamente.")

    def actualizar_producto(self, id, nombre=None, precio=None, categoria=None, stock=None):
        """Actualiza los detalles de un producto."""
        productos = self.cargar_productos()
        for producto in productos:
            if producto.id == id:
                if nombre:
                    producto.nombre = nombre
                if precio:
                    producto.precio = precio
                if categoria:
                    producto.categoria = categoria
                if stock is not None:
                    producto.stock = stock
                self.guardar_productos(productos)
                print("Producto actualizado exitosamente.")
                return
        print("ERROR: No se encontró un producto con ese ID.")

    def eliminar_producto(self, id):
        """Elimina un producto."""
        productos = self.cargar_productos()
        for i, producto in enumerate(productos):
            if producto.id == id:
                productos.pop(i)
                self.guardar_productos(productos)
                print(f"Producto con ID {id} eliminado exitosamente.")
                return
        print("ERROR: No se encontró un producto con ese ID.")


@dataclass
class Venta:
    """
    Clase que representa una venta de un producto.
    """
    producto_id: str
    cantidad: int
    fecha: str
    total: float


class VentaManager:
    """
    Clase encargada de gestionar las ventas.
    """
    def __init__(self, archivo="ventas.txt"):
        self.archivo = archivo

    def cargar_ventas(self):
        """Carga las ventas desde el archivo."""
        if not os.path.exists(self.archivo):
            return []
        try:
            with open(self.archivo, 'r') as archivo:
                return [Venta(**venta) for venta in json.load(archivo)]
        except json.JSONDecodeError:
            print("Error al leer el archivo de ventas.")
            return []

    def guardar_ventas(self, ventas):
        """Guarda las ventas en el archivo."""
        with open(self.archivo, 'w') as archivo:
            json.dump([venta.__dict__ for venta in ventas], archivo, indent=4)

    def registrar_venta(self, producto_id, cantidad, productos, productos_manager):
        """Registra una venta."""
        for producto in productos:
            if producto.id == producto_id:
                if producto.stock >= cantidad:
                    producto.stock -= cantidad
                    total = producto.precio * cantidad
                    nueva_venta = Venta(producto_id, cantidad, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total)
                    ventas = self.cargar_ventas()
                    ventas.append(nueva_venta)
                    self.guardar_ventas(ventas)
                    productos_manager.guardar_productos(productos)
                    print(f"Venta registrada exitosamente. Total: ${total:.2f}")
                    return
                else:
                    print("ERROR: Stock insuficiente.")
                    return
        print("ERROR: No se encontró un producto con ese ID.")


class Sistema:
    """
    Clase que gestiona la ejecución del sistema de productos y ventas.
    """
    def __init__(self):
        self.productos_manager = ProductoManager()
        self.venta_manager = VentaManager()

    def ejecutar(self):
        while True:
            print("\n===== SISTEMA DE REGISTRO DE PRODUCTOS =====")
            print("1. Registrar producto")
            print("2. Consultar productos")
            print("3. Actualizar producto")
            print("4. Eliminar producto")
            print("5. Registrar venta")
            print("6. Generar reporte de ventas")
            print("7. Salir")

            opcion = input("\nSeleccione una opción: ")

            if opcion == '1':
                self.registrar_producto()
            elif opcion == '2':
                self.consultar_productos()
            elif opcion == '3':
                self.actualizar_producto()
            elif opcion == '4':
                self.eliminar_producto()
            elif opcion == '5':
                self.registrar_venta()
            elif opcion == '6':
                self.generar_reporte()
            elif opcion == '7':
                print("¡Gracias por usar el sistema!")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def registrar_producto(self):
        id = input("ID del producto: ")
        nombre = input("Nombre del producto: ")
        precio = float(input("Precio del producto: "))
        categoria = input("Categoría del producto: ")
        stock = int(input("Stock del producto: "))
        nuevo_producto = Producto(id, nombre, precio, categoria, stock)
        self.productos_manager.registrar_producto(nuevo_producto)

    def consultar_productos(self):
        productos = self.productos_manager.cargar_productos()
        if productos:
            print(f"{'ID':<10} {'Nombre':<20} {'Precio':<10} {'Categoría':<15} {'Stock':<10}")
            for producto in productos:
                print(producto.id, producto.nombre, producto.precio, producto.categoria, producto.stock)

    def actualizar_producto(self):
        id = input("ID del producto a actualizar: ")
        nombre = input("Nuevo nombre (Enter para mantener): ")
        precio = input("Nuevo precio (Enter para mantener): ")
        categoria = input("Nueva categoría (Enter para mantener): ")
        stock = input("Nuevo stock (Enter para mantener): ")
        self.productos_manager.actualizar_producto(id, nombre, precio, categoria, stock)

    def eliminar_producto(self):
        id = input("ID del producto a eliminar: ")
        self.productos_manager.eliminar_producto(id)

    def registrar_venta(self):
        producto_id = input("ID del producto vendido: ")
        cantidad = int(input("Cantidad vendida: "))
        productos = self.productos_manager.cargar_productos()
        self.venta_manager.registrar_venta(producto_id, cantidad, productos, self.productos_manager)

    def generar_reporte(self):
        ventas = self.venta_manager.cargar_ventas()
        if ventas:
            for venta in ventas:
                print(f"ID Producto: {venta.producto_id} - Cantidad: {venta.cantidad} - Total: {venta.total}")
        else:
            print("No hay ventas registradas.")


if __name__ == "__main__":
    sistema = Sistema()
    sistema.ejecutar()
