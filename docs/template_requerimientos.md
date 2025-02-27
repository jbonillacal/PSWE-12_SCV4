# Requerimientos del producto - Validación de Identidad con Reconocimiento Facial(Serverless)

## 1. Requerimientos del negocio
### **Objetivo del Proyecto**

Desarrollar un sistema de **validación de identidad** basado en reconocimiento facial que permita a los usuarios subir una foto de su documento de identidad junto con una selfie para verificar su autenticidad. La aplicación comparará la selfie con la foto del documento y devolverá un resultado de validación.

### **Justificación**

Este sistema es ideal para una arquitectura *serverless* porque:

- La validación de identidad es una **tarea esporádica** y **event-driven**, que no requiere servidores en ejecución constante.
- La carga de trabajo es **impredecible**, ya que la demanda puede variar significativamente en función de la cantidad de usuarios intentando registrarse.
- El costo del sistema se optimiza porque solo se paga por las validaciones realizadas.
- Se puede escalar automáticamente en función del número de solicitudes sin intervención manual.

| Actor | Descripción|
|---------------|-------------------------------------------------------------------------------------------------|
| Usuario       | Persona que quiere validar su identidad. Sube su documento y una selfie.                        |
| Sistema       | Procesa la solicitud, extrae la información y verifica la identidad.                            |  
| Administrador | Supervisa las validaciones, accede a reportes y puede revisar manualmente validaciones fallidas.|  

### **Beneficios Esperados**

- **Automatización**: Reduce la necesidad de validaciones manuales, ahorrando tiempo y costos operativos.
- **Seguridad**: Evita el fraude en el registro de usuarios a través de una validación biométrica confiable.
- **Escalabilidad**: Manejo automático de la carga de trabajo sin necesidad de infraestructura dedicada.

## 2. Requerimientos funcionales
### **2.1. Subida de Documentos e Imágenes**

### **Historia de Usuario**

> Como usuario, quiero subir una imagen de mi documento de identidad y una selfie para que el sistema valide mi identidad.
> 

### **Criterios de Aceptación**

- Se deben aceptar formatos **PNG, JPEG, JPG** con un tamaño máximo de **5MB** por imagen.
- Se validará que el usuario suba **dos imágenes**: (1) Documento de identidad y (2) Selfie.
- Las imágenes se almacenarán temporalmente en un **bucket seguro** en la nube.

---

### **2.2. Extracción de Información del Documento**

### **Historia de Usuario**

> Como sistema, quiero extraer automáticamente el nombre y la foto de la identificación del usuario para compararla con su selfie.
> 

### **Criterios de Aceptación**

- Se usará un **OCR (Optical Character Recognition)** para extraer texto de la imagen del documento.
- Se extraerá la **foto del documento** mediante procesamiento de imágenes.
- Si la calidad del documento no es suficiente, se notificará al usuario para que suba una mejor imagen.

---

### **2.3. Comparación Biométrica de la Selfie con el Documento**

### **Historia de Usuario**

> Como sistema, quiero comparar la selfie del usuario con la foto extraída de su documento de identidad para verificar su identidad.
> 

### **Criterios de Aceptación**

- Se usará una **API de reconocimiento facial** para calcular la similitud entre ambas imágenes.
- Se establecerá un **umbral mínimo del 85%** de coincidencia para aprobar la validación.
- Si la coincidencia es menor al umbral, el sistema marcará la validación como fallida.

---

### **2.4. Generación del Resultado de Validación**

### **Historia de Usuario**

> Como usuario, quiero recibir un resultado indicando si mi validación fue exitosa o rechazada.
> 

### **Criterios de Aceptación**

- El usuario debe recibir **un correo o una notificación en la app** con el resultado de su validación.
- Si la validación es rechazada, se debe proporcionar una razón clara (ej. baja calidad de imagen, no coincidencia facial).
- Se debe permitir reintentar el proceso hasta un máximo de **tres intentos**.

---

### **2.5. Reportes y Monitoreo para Administradores**

### **Historia de Usuario**

> Como administrador, quiero acceder a reportes sobre el número de validaciones realizadas, su tasa de éxito y las razones de fallos.
> 

### **Criterios de Aceptación**

- Se debe generar un **dashboard** con métricas sobre validaciones realizadas y su tasa de éxito.
- Los intentos fallidos deben almacenarse con detalles sobre la causa de la falla.
- Se debe permitir revisar manualmente casos dudosos.

## 3. Requerimientos No-funcionales o de calidad

| Categoría              | Requerimiento|
|------------------------|----------|
| Escalabilidad          | La aplicación debe escalar automáticamente según la cantidad de usuarios sin intervención manual.  |
| Disponibilidad         | El sistema debe estar disponible 24/7 con un 99.9% de uptime.  | 
| Seguridad              | Las imágenes y datos del usuario deben almacenarse en un bucket privado encriptado. - Se deben eliminar imágenes temporales después de 24 horas.  | 
| Latencia               | El tiempo de procesamiento por validación no debe exceder los 3 segundos en el 95% de los casos.  | 
| Costo-Eficiencia       | Se debe utilizar un modelo serverless para minimizar costos, con pago basado en uso.  | 
| Registro de Auditoría  | Se debe registrar cada validación con su resultado y razones de fallo.  | 