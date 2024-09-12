
# Explicación del Despliegue de Microservicios con un API Gateway en Kubernetes

## 1. ¿Qué es Kubernetes?

**Kubernetes** es una plataforma de orquestación de contenedores que automatiza el despliegue, escalado y operación de aplicaciones en contenedores. En otras palabras, Kubernetes nos ayuda a gestionar múltiples contenedores, asegurando que siempre estén disponibles, escalando según sea necesario y recuperándose de fallos.

### Componentes principales de Kubernetes:

- **Node**: Un nodo es una máquina (física o virtual) donde Kubernetes ejecuta tus aplicaciones.
- **Pod**: Es la unidad más pequeña que puede ser gestionada por Kubernetes. Un pod puede contener uno o más contenedores que comparten el mismo entorno de red y almacenamiento.
  
  - **Pregunta común**: *¿Por qué usar un pod en lugar de directamente un contenedor?*  
    **Respuesta**: Un pod encapsula contenedores y recursos relacionados (como almacenamiento y red). Aunque generalmente hay un solo contenedor por pod, puedes tener varios contenedores que necesiten compartir estos recursos.

- **Deployment**: Un objeto que define cómo se despliega una aplicación. Gestiona el ciclo de vida de los pods y permite actualizaciones sin tiempo de inactividad.
  
  - **Pregunta común**: *¿Qué pasa si un pod falla?*  
    **Respuesta**: El deployment asegura que siempre haya un número específico de pods corriendo. Si un pod falla, Kubernetes automáticamente lo reiniciará o creará uno nuevo.

- **Service**: Un servicio en Kubernetes expone los pods para hacerlos accesibles dentro o fuera del clúster. Los servicios permiten que diferentes componentes de tu aplicación se comuniquen.
  
  - **Pregunta común**: *¿Por qué necesitamos servicios?*  
    **Respuesta**: Los pods tienen ciclos de vida cortos y sus direcciones IP cambian cada vez que se reinician. Los servicios proporcionan una IP estable para acceder a los pods, independientemente de cuántas veces cambien.

- **ConfigMap**: Un objeto que almacena datos de configuración en formato clave-valor, que pueden ser consumidos por los contenedores en los pods. Es útil para separar las configuraciones del código.

---

## 2. ¿Cómo funciona el API Gateway?

El **API Gateway** es un componente que actúa como un intermediario entre los clientes (usuarios o aplicaciones) y los microservicios. En lugar de que los clientes accedan directamente a los microservicios, todas las solicitudes pasan a través del API Gateway, que puede:

- **Enrutar solicitudes**: Redirigir las solicitudes al microservicio adecuado.
- **Autenticación**: Validar las solicitudes antes de que lleguen a los microservicios.
- **Balanceo de carga**: Distribuir las solicitudes entre múltiples instancias de un microservicio.
  
En este caso, estamos usando **Nginx** como el API Gateway.

### Flujo de trabajo con Nginx como API Gateway:

1. **Cliente envía una solicitud** (por ejemplo, un cliente envía una solicitud a `/auth/`).
2. **Nginx recibe la solicitud** y la redirige al microservicio de autenticación que está corriendo en Kubernetes.
3. **Nginx devuelve la respuesta** al cliente una vez que el microservicio procesa la solicitud.

---

## 3. Explicación de los Archivos YAML

En Kubernetes, usamos archivos YAML para definir y describir los recursos que queremos crear. Aquí tienes una descripción de los archivos YAML que vamos a usar:

### a) **ConfigMap (nginx-config.yaml)**

El **ConfigMap** almacena la configuración de Nginx. Este archivo se utiliza para configurar cómo el API Gateway (Nginx) enruta las solicitudes a los diferentes microservicios. Ejemplo de la configuración:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  nginx.conf: |
    events {}
    http {
      upstream auth_service {
        server auth-service.default.svc.cluster.local:80;
      }
      upstream payments_service {
        server payments-service.default.svc.cluster.local:80;
      }
      upstream products_service {
        server products-service.default.svc.cluster.local:80;
      }
      server {
        listen 80;
        location /auth/ {
          proxy_pass http://auth_service;
        }
        location /payments/ {
          proxy_pass http://payments_service;
        }
        location /products/ {
          proxy_pass http://products_service;
        }
      }
    }
```

- **Pregunta común**: *¿Qué es `proxy_pass`?*  
  **Respuesta**: `proxy_pass` es una directiva de Nginx que reenvía solicitudes a otro servidor. Aquí, estamos reenviando solicitudes a los servicios de Kubernetes que exponen nuestros microservicios.

### b) **Deployments y Services**

Cada microservicio tiene dos archivos YAML: uno para el deployment y otro para el servicio.

1. **Deployment (deployment-auth.yaml)**:
   Este archivo define cómo Kubernetes debe desplegar el microservicio de autenticación. Por ejemplo:

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: auth
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: auth
     template:
       metadata:
         labels:
           app: auth
       spec:
         containers:
         - name: auth
           image: jduartem/auth-service:latest
           ports:
           - containerPort: 5000
   ```

   - **Pregunta común**: *¿Qué hace el campo `replicas: 1`?*  
     **Respuesta**: Indica que solo queremos una réplica del microservicio de autenticación. Kubernetes se asegurará de que siempre haya un pod en ejecución para este microservicio.

2. **Service (service-auth.yaml)**:
   Define cómo exponer el microservicio para que otros componentes puedan acceder a él:

   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: auth-service
   spec:
     selector:
       app: auth
     ports:
       - protocol: TCP
         port: 80
         targetPort: 5000
   ```

   - **Pregunta común**: *¿Cuál es la diferencia entre `port` y `targetPort`?*  
     **Respuesta**: `port` es el puerto por el que el servicio será accesible, mientras que `targetPort` es el puerto en el contenedor donde la aplicación escucha.

---

## 4. Comandos Esenciales de Kubernetes

### **kubectl apply -f <archivo.yaml>**
Este comando aplica el contenido del archivo YAML, creando o actualizando recursos en Kubernetes.

Ejemplo:
```bash
kubectl apply -f deployment-auth.yaml
```

### **kubectl get pods**
Muestra el estado de todos los pods. Los estados más comunes son:
- **Running**: El pod está en ejecución y funciona correctamente.
- **Pending**: Kubernetes está esperando recursos (como CPU o memoria) para iniciar el pod.
- **CrashLoopBackOff**: El pod intenta reiniciarse después de fallar repetidamente.

### **kubectl get services**
Este comando muestra los servicios activos en el clúster. En nuestro caso, podemos usarlo para verificar que los servicios que exponen los microservicios están corriendo correctamente.

Ejemplo:
```bash
kubectl get services
```

### **kubectl logs <pod-name>**
Muestra los logs de un pod. Esto es útil para depurar problemas en un microservicio.

Ejemplo:
```bash
kubectl logs auth-service-<id>
```

### **kubectl port-forward <service> <local-port>:<service-port>**
Redirige el tráfico desde un puerto en tu máquina local hacia un servicio en Kubernetes. Esto te permitirá acceder a los microservicios desde tu navegador o Postman.

Ejemplo:
```bash
kubectl port-forward service/api-gateway-service 8080:80
```

---

## 5. Pruebas Locales

Una vez que todo esté desplegado, podemos probar los microservicios a través del **API Gateway** usando `curl` o un navegador. Las URLs para los microservicios serán:

- **Autenticación**: `http://localhost:8080/auth/`
- **Pagos**: `http://localhost:8080/payments/`
- **Productos**: `http://localhost:8080/products/`

### Comando de prueba con `curl`:
```bash
curl http://localhost:8080/auth/
```

Este comando debería devolver una respuesta del microservicio de autenticación. Si todo está configurado correctamente, ¡el ejercicio habrá sido un éxito!
