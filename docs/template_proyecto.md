# 1. Introducción
## 1.1. Propósito
El propósito de este documento es describir detalladamente la arquitectura técnica del sistema de reconocimiento facial basado en Google Cloud Functions y DeepFace, con funcionalidades de extracción de texto desde imágenes, publicación de eventos en Google Pub/Sub y almacenamiento de datos en BigQuery. El propósito de la base de datos de BigQuery es llevar un registro detallado del conteo de transacciones por compañía. Este documento sirve como una guía técnica para todos los involucrados en el desarrollo, despliegue, mantenimiento y evolución del sistema.

### Audiencia Prevista

Este documento está dirigido a:

**Arquitectos de Software**: Para evaluar y validar las decisiones de arquitectura adoptadas, asegurando su alineación con los requisitos técnicos y de negocio.

**Desarrolladores**: Para comprender los componentes, patrones y tecnologías involucradas, así como las interfaces y dependencias del sistema.

**Ingenieros de DevOps**: Para facilitar la implementación, monitoreo, escalabilidad y mantenimiento de la infraestructura en la nube.

**Stakeholders de Negocio**: Para obtener una visión general del sistema y su alineación con los objetivos comerciales.

**Personal de Seguridad y Cumplimiento**: Para evaluar los aspectos relacionados con la seguridad, privacidad y conformidad regulatoria.

### Uso Previsto

Este documento debe ser utilizado como referencia técnica principal durante las fases de diseño, desarrollo, implementación y mantenimiento del sistema. Además, servirá como base para futuras mejoras y actualizaciones de la arquitectura, asegurando que cualquier cambio o extensión sea consistente con las decisiones previas y con la visión general del proyecto. Este documento es elaborado como parte del curso de Arquitectura de Software impartido por Cenfotec.

## 1.2 Alcance
El sistema que cubrirá esta arquitectura se enfoca en ofrecer un servicio de reconocimiento facial de alta disponibilidad y rendimiento mediante Google Cloud Functions con DeepFace, almacenamiento de resultados en BigQuery y comunicación asincrónica a través de Google Pub/Sub.

Las principales características incluyen:

**Procesamiento de Reconocimiento Facial en Tiempo Real**: Respuesta sub-second mediante Cloud Functions configuradas para escalar dinámicamente de acuerdo con la demanda.

**Extracción de Texto desde Imágenes**: Procesamiento de imágenes para extraer información textual relevante mediante Google Cloud AI, especialmente para identificar y extraer información de cédulas de las personas.

**Publicación de Eventos**: Uso de Google Pub/Sub para la comunicación asincrónica y desacoplamiento de componentes.

**Almacenamiento en BigQuery**: Registro de transacciones por compañía para análisis posterior.

El sistema debe ser capaz de manejar múltiples solicitudes concurrentes de manera eficiente, garantizando tiempos de respuesta sub-second incluso bajo cargas elevadas mediante la escalabilidad automática de las Cloud Functions.

## 1.3. Definiciones, Acrónimos y Abreviaturas
### 1.3.1 Definiciones
- **Reconocimiento Facial**: Técnica de identificación o verificación de la identidad de un individuo utilizando características biométricas extraídas de su rostro.
- **DeepFace**: Framework de código abierto basado en aprendizaje profundo (Deep Learning) que proporciona herramientas para análisis facial, incluyendo verificación de identidad, reconocimiento de emociones, edad y género.
- **Extracción de Texto (OCR)**: Proceso mediante el cual se convierte información textual presente en imágenes a un formato digital legible por máquina.
- **Google Cloud Pub/Sub**: Servicio de mensajería asíncrona proporcionado por Google Cloud que permite la comunicación entre aplicaciones a través de un modelo Publisher-Subscriber (Publicador-Suscriptor).
- **Google Cloud Functions**: Plataforma sin servidor que permite la ejecución de funciones en respuesta a eventos, como peticiones HTTP o mensajes de Pub/Sub.
- **Aprendizaje Profundo (Deep Learning)**: Rama de la Inteligencia Artificial que utiliza redes neuronales profundas para analizar grandes conjuntos de datos y aprender patrones complejos.
- **Red Neuronal Convolucional (CNN)**: Arquitectura de red neuronal comúnmente utilizada en tareas de visión por computadora como clasificación de imágenes y reconocimiento facial.
- **Endpoint**: Punto de acceso a un servicio o función expuesta a través de una URL para comunicación o procesamiento de datos.
- **Pipeline**: Conjunto de procesos secuenciales que transforman y transfieren datos de un estado inicial a uno final.
- **Microservicio**: Componente independiente que realiza una tarea específica dentro de una arquitectura más grande, comunicándose con otros servicios a través de APIs.
- **JSON (JavaScript Object Notation)**: Formato ligero de intercambio de datos fácil de leer y escribir para humanos, y fácil de interpretar y generar para máquinas.

### 1.3.2 Acrónimos y Abreviaturas
- AI: Artificial Intelligence (Inteligencia Artificial)
- CNN: Convolutional Neural Network (Red Neuronal Convolucional)
- DL: Deep Learning (Aprendizaje Profundo)
- OCR: Optical Character Recognition (Reconocimiento Óptico de Caracteres)
- API: Application Programming Interface (Interfaz de Programación de Aplicaciones)
- GCP: Google Cloud Platform
- HTTP: HyperText Transfer Protocol (Protocolo de Transferencia de Hipertexto)
- JSON: JavaScript Object Notation
- Pub/Sub: Publisher-Subscriber (Publicador-Suscriptor)
- ML: Machine Learning (Aprendizaje Automático)
- ID: Identification (Identificación)
- URL: Uniform Resource Locator (Localizador Uniforme de Recursos)
- REST: Representational State Transfer (Transferencia de Estado Representacional)

## 1.4. Referencias
Enumerar otros documentos, sitios web o materiales referenciados en este documento.

## 1.5. Resumen
Proporcionar un breve resumen de las secciones siguientes del documento.

# 2. Representación Arquitectónica 
## 2.1.Estilo Arquitectónico

El sistema implementa un estilo arquitectónico Basado en Microservicios Serverless desplegado principalmente en Google Cloud Platform (GCP). Cada componente del sistema es independiente y ejecuta una función específica, comunicándose a través de eventos y mensajes asincrónicos mediante Pub/Sub.

En este tipo de arquitectura, los servicios no están activos permanentemente, sino que se activan en respuesta a eventos específicos (ej. solicitudes de autenticación facial). Este modelo se integra de manera fluida con un ecosistema sin servidor (serverless), permitiendo escalabilidad automática y pago basado en uso real.

## 2.2 Justificación del Uso del Estilo Arquitectónico
**Modularidad y Escalabilidad:**

La arquitectura basada en microservicios permite que cada componente (Cloud Functions, Cloud Run, BigQuery, Cloud Vision AI, DeepFace) sea independiente, facilitando el desarrollo, despliegue y escalado individual.
En caso de un incremento de solicitudes de autenticación facial, los componentes involucrados pueden escalar automáticamente sin afectar otros servicios.

**Eficiencia de Costos:**

Serverless Computing ofrece un modelo de pago por uso real. Específicamente:
**Cloud Functions y Cloud Run:** Solo generan costos cuando se ejecutan, lo cual es ideal para procesos que se disparan por eventos o solicitudes (como las solicitudes de autenticación facial).

**BigQuery:** 
Facturado por consulta y almacenamiento, lo cual permite optimizar costos almacenando solo la información necesaria y accediéndola bajo demanda.

**Pub/Sub:** 
Bajo costo y eficiente para sistemas basados en eventos y comunicación asíncrona.
La naturaleza event-driven (basada en eventos) permite que el sistema permanezca inactivo cuando no hay solicitudes, eliminando costos de infraestructura asociados a servicios en constante ejecución.

**Elasticidad y Escalabilidad Automática:**
Google Cloud Functions y Cloud Run pueden escalar desde cero hasta miles de instancias automáticamente, respondiendo a la demanda sin necesidad de intervención manual o planificación previa.
Esto es crucial dado que la autenticación facial no es un proceso constante sino que responde a solicitudes esporádicas.

**Despliegue Simplificado y Alta Disponibilidad:**
Los servicios sin servidor proporcionan alta disponibilidad automáticamente, distribuyendo la carga y mejorando la tolerancia a fallos.
Este enfoque simplifica el despliegue continuo y la integración de nuevas funcionalidades sin afectar la operación de componentes ya existentes.

**Reducción de Costos de Mantenimiento:**
Al no gestionar servidores o infraestructura, se reduce significativamente el costo operativo y de mantenimiento.
Todo el monitoreo, actualización de parches de seguridad y escalabilidad son manejados automáticamente por Google Cloud.

# 3. Partes Interesadas y Preocupaciones del Sistema
## 3.1. Partes Interesadas

| Parte interesada           | Rol / Relación con el sistema                                       | Intereses / Preocupaciones clave |
|----------------------------|---------------------------------------------------------------------|---------------------------------------------------------------|
| **Usuarios finales**       | Personas que usan el sistema para validar su identidad.             | - Facilidad de uso  - Tiempo de respuesta rápido  - Privacidad y seguridad de sus imágenes - Confiabilidad del resultado |
| **Equipo de desarrollo**   | Encargados del diseño, desarrollo y mantenimiento del sistema.      | - Simplicidad y claridad de la arquitectura - Mantenibilidad del código - Facilidad para pruebas y despliegue |
| **Administradores del sistema** | Supervisa el comportamiento del sistema y los resultados de validación. | - Acceso a resultados de procesamiento - Trazabilidad de errores - Posibilidad de diagnóstico ante fallos |
| **Equipo de seguridad**    | Responsable de garantizar que el sistema cumpla con buenas prácticas de seguridad. | - Protección de los datos sensibles - Control de acceso a los recursos - Minimización del almacenamiento de datos |
| **Stakeholders de negocio**| Responsables de la viabilidad y sostenibilidad del sistema.         | - Bajo costo operativo - Escalabilidad del sistema - Tiempo de implementación rápido - Cumplimiento de objetivos funcionales |
| **Proveedor de infraestructura (GCP)** | Plataforma que ejecuta el sistema y provee los servicios gestionados. | - Uso correcto y eficiente de los recursos - Seguridad en la configuración de los servicios - Disponibilidad del entorno |


## 3.2. Preocupaciones del Sistema

| Categoría           | Preocupación del Sistema                                                        | Estrategia de Mitigación Propuesta                                     |
|---------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------|
| **Rendimiento**     | El sistema debe validar identidades en tiempo razonable, sin demoras perceptibles para el usuario. | Uso de funciones *serverless* (Cloud Functions) con procesamiento concurrente. Se espera < 3 segundos en el 95% de los casos. |
| **Escalabilidad**   | El sistema debe manejar picos de demanda sin degradación del servicio.          | Arquitectura basada en eventos y componentes *serverless* que escalan automáticamente (Cloud Functions, Pub/Sub). |
| **Seguridad**       | Protección de imágenes personales y datos sensibles durante el almacenamiento y procesamiento. | Uso de **Cloud Storage buckets privados**, encriptación en tránsito y en reposo, y acceso controlado mediante IAM. |
| **Privacidad**      | Protección de la identidad del usuario final.                                   | Eliminación automática de imágenes después de 24h, almacenamiento temporal, y cumplimiento con principios de minimización de datos. |
| **Costo**           | Optimización del uso de recursos para evitar costos innecesarios.               | Pago por uso con servicios *serverless* (solo se incurre en costos cuando hay actividad). No hay servidores siempre encendidos. |
| **Mantenibilidad**  | Facilidad para actualizar o extender el sistema sin afectar a los usuarios.     | Componentes desacoplados mediante Pub/Sub. Código modular en Python con funciones independientes. |
| **Auditoría y trazabilidad** | Posibilidad de auditar el flujo de validaciones, identificar errores o abusos. | Firestore guarda los eventos de validación. Todos los pasos clave se registran con timestamps. |
| **Disponibilidad**  | El sistema debe estar disponible 24/7, incluso ante fallos parciales.           | Infraestructura distribuida en GCP, servicios de alta disponibilidad y escalabilidad automática. |

# 4. Visión General del Sistema

## 4.1. Descripción de Alto Nivel

El sistema de **Validación de Identidad con Reconocimiento Facial** es una solución *serverless* desarrollada sobre Google Cloud Platform (GCP) que permite verificar la identidad de una persona comparando una selfie con una imagen de su documento de identidad.

La solución está diseñada para ser **escalable**, **segura** y **eficiente**, eliminando la necesidad de servidores dedicados y aprovechando servicios gestionados que se activan bajo demanda. Está compuesta por varios módulos funcionales que trabajan en conjunto para realizar las siguientes tareas:

### Funcionalidades principales:

- **Carga de imágenes:** El usuario sube dos imágenes: una de su documento de identidad y otra de su rostro (selfie).
- **Extracción de datos del documento:** A través de Google Vision AI (OCR), se extraen el texto y la fotografía del documento.
- **Comparación biométrica:** Se compara la imagen del documento con la selfie utilizando detección facial.
- **Determinación del resultado:** Se determina si la identidad es válida en base a un umbral de coincidencia facial.
- **Notificación al usuario:** Se notifica al usuario con el resultado de la validación.
- **Almacenamiento y trazabilidad:** Se guarda el resultado de la validación para auditoría y análisis posteriores.

### Componentes clave del sistema:

| Componente                     | Descripción                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| **Google Cloud Storage (GCS)** | Almacena temporalmente las imágenes subidas por los usuarios.              |
| **Cloud Functions (Python)**   | Procesan cada etapa del flujo: carga, extracción OCR, comparación facial, etc. |
| **Google Vision AI**           | API que permite extraer texto y realizar detección facial en las imágenes. |
| **Cloud Pub/Sub**              | Facilita la comunicación asíncrona entre funciones para enviar notificaciones. |
| **Big Query**                  | Almacenamiento de registros de validación para análisis histórico.      |

Este enfoque modular permite que el sistema se adapte fácilmente a cambios o mejoras, manteniendo bajo control los costos operativos y asegurando un rendimiento óptimo.

# 5. Estrategias Arquitectónicas

## 5.1. Estrategias Clave

Las siguientes estrategias arquitectónicas se han definido para abordar de forma efectiva las preocupaciones de las partes interesadas, garantizando que el sistema sea escalable, seguro, eficiente y fácil de mantener:

### 1. **Arquitectura Serverless basada en eventos**
- Se utiliza Google Cloud Functions para construir un sistema reactivo y desacoplado.
- Las funciones se activan en respuesta a eventos (como la subida de una imagen o la finalización del procesamiento).
- **Preocupaciones abordadas**: escalabilidad, costos, rendimiento, mantenibilidad.

### 2. **Desacoplamiento mediante Cloud Pub/Sub**
- Se emplea Cloud Pub/Sub para comunicar funciones asíncronamente sin acoplamiento directo entre ellas.
- Esto permite escalar, distribuir carga y realizar tareas como el envío de notificaciones de forma independiente.
- **Preocupaciones abordadas**: escalabilidad, resiliencia, extensibilidad.

### 3. **Procesamiento inteligente con Google Vision AI y DeepFace**
- Se utiliza Google Vision AI para realizar OCR y detectar rostros en imágenes de documentos.
- Para la comparación facial entre la selfie y la imagen del documento, se emplea la librería DeepFace, que facilita la implementación de reconocimiento facial sin necesidad de construir modelos desde cero.
- Esta combinación permite integrar capacidades avanzadas de visión por computadora con simplicidad y rapidez de desarrollo.
- **Preocupaciones abordadas**: precisión de resultados, rendimiento, mantenimiento.

### 4. **No almacenamiento persistente de las imágenes en base de datos**
- Las imágenes subidas por los usuarios (documento y selfie) tienen un ciclo de vida muy corto: se procesan de inmediato y luego se eliminan.
- Evitar el almacenamiento permanente de imágenes o resultados ayuda a minimizar el riesgo de exposición de datos sensibles, alineándose con los principios de privacidad desde el diseño (privacy by design).
- Al eliminar componentes de almacenamiento persistente, se reducen los costos operativos y se eliminan dependencias adicionales.
- **Preocupaciones abordadas**: seguridad, privacidad, cumplimiento de normativas.

### 5. **Minimización del costo operativo**
- La arquitectura está basada en servicios gestionados y pago por uso.
- Se evita el aprovisionamiento de infraestructura o mantenimiento de servidores.
- **Preocupaciones abordadas**: eficiencia operativa, costos de infraestructura.

### 6. **Separación de responsabilidades y modularidad**
- Cada función realiza una tarea específica (subida, OCR, comparación, notificación).
- Se sigue el principio de responsabilidad única (SRP) para facilitar la mantenibilidad.
- **Preocupaciones abordadas**: mantenibilidad, extensibilidad, facilidad de pruebas.

# 6. Arquitectura del Sistema
## 6.1. Resumen de Capas/Módulos
Proporcionar un resumen de las capas o módulos del sistema.

## 6.2 Diagramas de Componentes
### 6.2.1 Vista general del sistema
![Vista general del sistema](diags/system-context-structurizr.png)

### 6.2.2 Vista detallada del sistema
![Vista detallada del sistema](diags/container-structurizr.png)

## 6.3 Diseño de la Base de Datos
No se utilizó una base de datos en el sistema ya que las imágenes y los resultados de validación se procesan de forma inmediata y no requieren persistencia. Esta decisión reduce la complejidad arquitectónica, minimiza los costos operativos y refuerza la privacidad del usuario al evitar el almacenamiento de datos sensibles. El enfoque se alinea con el modelo serverless y con principios de seguridad como la minimización de datos, ya que toda la información se maneja de manera efímera y se elimina una vez finalizado el procesamiento.

# 7. Decisiones Arquitectónicas Clave 
## 7.1. Registro de Decisiones
Registrar las decisiones arquitectónicas clave tomadas y la justificación detrás de ellas:
### 7.1.1 Pros y Contras.
### 7.1.2 Alternativas y balance de factores.
### 7.1.3 Problemas potenciales.
### 7.1.4 Dependencias a considerar.


# 8. Atributos de Calidad 
## 8.1. Rendimiento
Describir los requisitos de rendimiento y cómo la arquitectura los respalda.

## 8.2. Escalabilidad
Describir las consideraciones y estrategias de escalabilidad.

## 8.3. Seguridad
Describir las medidas de seguridad y consideraciones dentro de la arquitectura.

## 8.4. Mantenibilidad
Describir cómo se ha diseñado el sistema para facilitar su mantenimiento.

# 9. Riesgos y Deuda Técnica 
## 9.1. Riesgos Identificados
Enumerar los riesgos identificados y su posible impacto en el proyecto.

## 9.2. Deuda Técnica
Describir cualquier área de deuda técnica y los planes para su resolución.

# 10. Apéndices 
## 10.1. Glosario
Ver sección _1.3. Definiciones, Acrónimos y Abreviaturas_.

## 10.2. Índice
Incluir un índice de términos y secciones para facilitar la navegación.

# 10.3. Historial de Revisión
Documentar el historial de revisiones de este documento.
