# Requerimientos del producto - Validación de Identidad con Reconocimiento Facial(Serverless)

## 1. Requerimientos del negocio
### **Objetivo del proyecto**

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

### **Beneficios esperados**

- **Automatización**: Reduce la necesidad de validaciones manuales, ahorrando tiempo y costos operativos.
- **Seguridad**: Evita el fraude en el registro de usuarios a través de una validación biométrica confiable.
- **Escalabilidad**: Manejo automático de la carga de trabajo sin necesidad de infraestructura dedicada.

## 2. Requerimientos funcionales
### **2.1. Subida de documentos e imágenes**

### **Historia de usuario**

> Como usuario, quiero subir una imagen de mi documento de identidad y una selfie para que el sistema valide mi identidad.
> 

### **Criterios de aceptación**

- Se deben aceptar formatos **PNG, JPEG, JPG** con un tamaño máximo de **5MB** por imagen.
- Se validará que el usuario suba **dos imágenes**: (1) Documento de identidad y (2) Selfie.
- Las imágenes se almacenarán temporalmente en un **bucket seguro** en la nube.

---

### **2.2. Extracción de información del documento**

### **Historia de usuario**

> Como sistema, quiero extraer automáticamente el nombre y la foto de la identificación del usuario para compararla con su selfie.
> 

### **Criterios de aceptación**

- Se usará un **OCR (Optical Character Recognition)** para extraer texto de la imagen del documento.
- Se extraerá la **foto del documento** mediante procesamiento de imágenes.
- Si la calidad del documento no es suficiente, se notificará al usuario para que suba una mejor imagen.

---

### **2.3. Comparación biométrica de la selfie con el documento**

### **Historia de usuario**

> Como sistema, quiero comparar la selfie del usuario con la foto extraída de su documento de identidad para verificar su identidad.
> 

### **Criterios de aceptación**

- Se usará una **API de reconocimiento facial** para calcular la similitud entre ambas imágenes.
- Se establecerá un **umbral mínimo del 85%** de coincidencia para aprobar la validación.
- Si la coincidencia es menor al umbral, el sistema marcará la validación como fallida.

---

### **2.4. Generación del resultado de validación**

### **Historia de usuario**

> Como usuario, quiero recibir un resultado indicando si mi validación fue exitosa o rechazada.
> 

### **Criterios de aceptación**

- El usuario debe recibir **un correo o una notificación en la app** con el resultado de su validación.
- Si la validación es rechazada, se debe proporcionar una razón clara (ej. baja calidad de imagen, no coincidencia facial).
- Se debe permitir reintentar el proceso hasta un máximo de **tres intentos**.

### **Criterios de aceptación**

- Se debe generar un **dashboard** con métricas sobre validaciones realizadas y su tasa de éxito.
- Los intentos fallidos deben almacenarse con detalles sobre la causa de la falla.
- Se debe permitir revisar manualmente casos dudosos.

## 3. Requerimientos No-funcionales o de calidad

| Atributo de Calidad   | Fuente                                     | Estímulo                                                              | Entorno                             | Respuesta                                                                                                                         | Métrica                                                                 |
|-----------------------|--------------------------------------------|-----------------------------------------------------------------------|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| Escalabilidad         | Aumento de usuarios simultáneos            | Incremento repentino en solicitudes de validación facial              | Operación normal                     | Escalamiento automático hasta 10 instancias serverless (mínimo 1 activa). Cada instancia con 8GB RAM y 2 vCPU para evitar cold starts | Manejo de hasta 10x carga base sin degradación. Cold start ≤ 1 vez por día |
| Disponibilidad        | Usuarios accediendo desde cualquier lugar  | Solicitudes concurrentes o carga alta                                 | 24/7                                 | Sistema se mantiene disponible sin interrupciones                                                                                | ≥ 99.9% de uptime mensual                                              |
| Seguridad             | Usuario envía imágenes personales          | Transmisión de datos entre cliente y servidor                         | Durante el proceso de autenticación  | Comunicación sobre HTTPS, servicios protegidos por VPN, acceso mediante token OAuth. No se almacena información del usuario       | 100% conexiones HTTPS, VPN activa, OAuth requerido. 0% de almacenamiento en reposo |
| Latencia              | Usuario solicita autenticación             | Backend recibe imagen para verificación facial                        | Carga normal y picos                 | Respuesta rápida del sistema con resultado de validación                                                                          | 95% de respuestas en ≤ 3 segundos                                      |
| Costo-Eficiencia      | Operación continua                         | Uso variable del sistema                                              | Ciclo de vida del sistema            | Arquitectura serverless con escalado automático y pago por uso real                                                               | Sin costos fijos; facturación basada en invocaciones y recursos utilizados |
| Registro de Auditoría| Usuario solicita autenticación             | Finalización de verificación facial                                   | Operación normal                     | Registro detallado del resultado con timestamp, éxito o fallo, y razón (si aplica)                                                | 100% de autenticaciones auditadas                                     |


