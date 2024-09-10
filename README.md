# Ejercicio 1: Implementación del API Gateway (60 minutos)

## Instrucciones:
El objetivo de este ejercicio es que los estudiantes implementen un **API Gateway** que gestione la comunicación entre los clientes y tres microservicios: **autenticación**, **pagos**, y **catálogo de productos**. Los estudiantes deberán crear un entorno donde todas las solicitudes pasen a través del API Gateway.

### Paso 1: Configuración del Entorno
Los estudiantes deben preparar su entorno local o en la nube (opcionalmente en Kubernetes o Docker) para ejecutar el **API Gateway** junto a tres microservicios.

El **API Gateway** puede ser configurado usando herramientas como **Nginx** o **Kong API Gateway**. Estos son dos de los gateways más utilizados y ofrecen funcionalidades como enrutamiento de solicitudes, autenticación y balanceo de carga.

### Paso 2: Enrutamiento Básico
Los estudiantes deben configurar las rutas en el **API Gateway** para que cada solicitud sea redirigida al microservicio correcto basado en el endpoint al que apunta.

**Ejemplo:**
- `/auth` debería ser redirigido al microservicio de autenticación.
- `/payments` redirige al microservicio de pagos.
- `/products` apunta al catálogo de productos.

### Paso 3: Prueba de Comunicación
Utilizando una herramienta como **Postman**, los estudiantes deben probar que todas las solicitudes HTTP están siendo redirigidas correctamente por el **API Gateway** a los microservicios correspondientes.

Se deben crear solicitudes **GET**, **POST**, **PUT**, y **DELETE** dependiendo del microservicio.

## Herramientas y Entorno:
- **Nginx** o **Kong API Gateway** configurado en contenedores **Docker** o en un clúster de **Kubernetes**.
- Microservicios de ejemplo implementados en **Node.js** o **Python**.
- **Postman** para realizar y probar solicitudes HTTP hacia el **API Gateway**.
- Proporcionar un repositorio en **GitHub** con el código base y configuraciones iniciales para que los estudiantes puedan clonar el proyecto.

## Resultados Esperados:
- Los estudiantes deben ser capaces de implementar un **API Gateway** funcional que redirija solicitudes a los microservicios correctos.
- Los microservicios deben poder interactuar de manera correcta y recibir las solicitudes a través del **API Gateway**.
- Se deben generar logs de las solicitudes para verificar que todas pasaron a través del **API Gateway**.
