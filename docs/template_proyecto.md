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
Enumerar las partes interesadas del sistema y sus intereses/preocupaciones.

## 3.2. Preocupaciones del Sistema
Describir las preocupaciones del sistema, como rendimiento, escalabilidad y seguridad.

# 4. Visión General del Sistema 
## 4.1.	Descripción de Alto Nivel
Proporcionar una descripción de alto nivel de la funcionalidad y los componentes del sistema.

# 5. Estrategias Arquitectónicas
## 5.1. Estrategias Clave
Describir las estrategias arquitectónicas clave y cómo abordan las preocupaciones específicas de las partes interesadas.

# 6. Arquitectura del Sistema
## 6.1. Resumen de Capas/Módulos
Proporcionar un resumen de las capas o módulos del sistema.

## 6.2 Diagramas de Componentes
Incluir cualquier diagrama de componentes relevante que ilustre partes significativas del sistema.

## 6.3 Diseño de la Base de Datos
Incluir el diseño y la estructura de la base de datos.

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
##10.1. Glosario
Proporcionar un glosario de términos utilizados a lo largo del documento.

## 10.2. Índice
Incluir un índice de términos y secciones para facilitar la navegación.

# 10.3. Historial de Revisión
Documentar el historial de revisiones de este documento.
