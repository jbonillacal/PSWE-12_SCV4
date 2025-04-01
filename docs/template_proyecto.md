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

Procesamiento de Reconocimiento Facial en Tiempo Real: Respuesta sub-second mediante Cloud Functions configuradas para escalar dinámicamente de acuerdo con la demanda.

**Extracción de Texto desde Imágenes**: Procesamiento de imágenes para extraer información textual relevante mediante Google Cloud AI, especialmente para identificar y extraer información de cédulas de las personas.

**Publicación de Eventos**: Uso de Google Pub/Sub para la comunicación asincrónica y desacoplamiento de componentes.

**Almacenamiento en BigQuery**: Registro de transacciones por compañía para análisis posterior.

El sistema debe ser capaz de manejar múltiples solicitudes concurrentes de manera eficiente, garantizando tiempos de respuesta sub-second incluso bajo cargas elevadas mediante la escalabilidad automática de las Cloud Functions.

## 1.3. Definiciones, Acrónimos y Abreviaturas
Proporcionar definiciones para los términos y acrónimos utilizados a lo largo del documento.

## 1.4. Referencias
Enumerar otros documentos, sitios web o materiales referenciados en este documento.

## 1.5. Resumen
Proporcionar un breve resumen de las secciones siguientes del documento.

# 2. Representación Arquitectónica 
## 2.1.Estilo Arquitectónico y Justificación
Describir el estilo(s) arquitectónico(s) que guía el diseño (por ejemplo, microservicios, monolítico, etc.) y la justificación para su elección.

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
