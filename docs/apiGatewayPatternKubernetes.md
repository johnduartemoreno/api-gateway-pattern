# Reto: Desplegando Microservicios con un API Gateway en Kubernetes

## Objetivo
El objetivo del ejercicio es que los estudiantes desplieguen una infraestructura completa de microservicios gestionados por un **API Gateway** en un cl�ster de **Kubernetes**. Los estudiantes deben desplegar tres microservicios: **auth**, **payments**, y **products**, y enrutar todas las solicitudes a trav�s del **API Gateway**.

## Tareas

1. **Configurar el entorno**: 
   - Aseg�rate de que tu entorno local est� listo para desplegar en Kubernetes. Aseg�rate de tener `kubectl` instalado y configurado, y acceso a un cl�ster de Kubernetes.

2. **Descargar los archivos YAML**:
   - Clona el repositorio del proyecto y navega a la carpeta `k8s`:
     ```bash
     git clone https://github.com/johnduartemoreno/api-gateway-pattern.git
     cd api-gateway-pattern/k8s
     ```

3. **Desplegar el ConfigMap de Nginx**:
   - El primer paso ser� desplegar la configuraci�n de Nginx que se usar� en el API Gateway:
     ```bash
     kubectl apply -f nginx-config.yaml
     ```

4. **Desplegar los microservicios**:
   - Despliega cada uno de los tres microservicios (`auth`, `payments`, `products`):
     ```bash
     kubectl apply -f deployment-auth.yaml
     kubectl apply -f service-auth.yaml
     
     kubectl apply -f deployment-payments.yaml
     kubectl apply -f service-payments.yaml
     
     kubectl apply -f deployment-products.yaml
     kubectl apply -f service-products.yaml
     ```

5. **Desplegar el API Gateway**:
   - Una vez que los microservicios est�n en ejecuci�n, despliega el API Gateway (basado en Nginx) para gestionar las solicitudes entrantes:
     ```bash
     kubectl apply -f deployment-gateway.yaml
     kubectl apply -f service-gateway.yaml
     ```

6. **Verificar que todo est� corriendo**:
   - Revisa que todos los pods y servicios est�n corriendo correctamente con los siguientes comandos:
     ```bash
     kubectl get pods
     kubectl get services
     ```

7. **Probar los endpoints**:
   - Usa `kubectl port-forward` para probar los microservicios a trav�s del API Gateway en tu m�quina local:
     ```bash
     kubectl port-forward service/api-gateway-service 8080:80
     ```
   - Luego, puedes acceder a los microservicios a trav�s de las siguientes URLs:
     - Microservicio de Autenticaci�n: `http://localhost:8080/auth/`
     - Microservicio de Pagos: `http://localhost:8080/payments/`
     - Microservicio de Productos: `http://localhost:8080/products/`

## Tiempo estimado
- Se espera que el reto sea completado en **2 horas**.
