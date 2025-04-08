workspace "Aplicación de Validación de Identidad con Reconocimiento Facial" "Sistema serverless en GCP para verificar identidades con procesamiento facial" {

    model {
        # Actores
        usuario = person "Usuario" {
            description "Persona que sube su documento y selfie para validar su identidad."
        }

        administrador = person "Administrador" {
            description "Supervisa métricas y casos fallidos de validación."
        }

        # Sistema principal
        sistemaValidacion = softwareSystem "Sistema de Validación de Identidad" {
            description "Plataforma que valida identidades comparando rostros de documentos y selfies usando reconocimiento facial."

            # Contenedores
            frontend = container "Frontend Web" {
                description "Interfaz para que el usuario suba sus imágenes."
            }

            funcionComparacion = container "Cloud Function - Comparación Facial" {
                description "Compara la selfie con la imagen del documento usando DeepFace."
                technology "Python + DeepFace"
            }

            funcionOCR = container "Cloud Function - OCR" {
                description "Extrae texto y la foto del documento usando Google Vision AI."
                technology "Python + GCP Vision API"
            }

            pubsub = container "Cloud Pub/Sub" {
                description "Distribuye eventos de validación para procesamiento asíncrono."
                technology "Pub/Sub"
            }

            bigquery = container "BigQuery" {
                description "Almacena resultados de validación para análisis posteriores."
                technology "Google Big Query"
            }

            # Relaciones
            usuario -> frontend "Sube imágenes"
            frontend -> funcionComparacion "Envía imágenes y dispara comparación facial"
            funcionComparacion -> funcionOCR "Dispara procesamiento OCR[
            funcionOCR -> funcionComparacion "Lee imagen de documento y retorna datos de OCR"
            funcionComparacion -> pubsub "Publica evento con datos de validación y OCR"
            pubsub -> bigquery "Guarda métricas de validación"

            administrador -> bigquery "Consulta estadísticas"
        }

        usuario -> sistemaValidacion "Usa"
        administrador -> sistemaValidacion "Monitorea y revisa"
    }

    views {
        systemContext sistemaValidacion {
            include *
            autolayout lr
        }

        container sistemaValidacion {
            include *
            autolayout lr
        }

        theme default

        styles {
            element "SoftwareSystem" {
                background "#1168bd"
                color "#ffffff"
            }
            element "Container" {
                background "#438dd4"
                color "#ffffff"
            }
            element "Person" {
                background "#08427b"
                color "#ffffff"
                shape person
            }
        }
    }

    configuration {
        scope softwareSystem
    }
}
