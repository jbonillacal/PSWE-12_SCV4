<template>
  <div class="container">
    <h1>Sube o Captura Imágenes</h1>
    <p>Selecciona dos imágenes o toma una foto desde la segunda caja.</p>

    <div class="form-container">
      <!-- Caja para Subir Imagen 1 -->
      <div class="upload-box">
        <label>Subir Imagen 1:</label>
        <input type="file" accept="image/*" @change="handleFileUpload($event, 'image1')" />
        <img v-if="image1" :src="image1" alt="Vista Previa" class="preview" />
      </div>

      <!-- Caja para Subir o Capturar Imagen 2 -->
      <div class="upload-box">
        <label>Subir Imagen 2 o Capturar Foto:</label>
        <input type="file" accept="image/*" @change="handleFileUpload($event, 'image2')" />
        <video v-if="!image2" ref="video" autoplay class="preview"></video>
        <button v-if="!image2" @click="capturePhoto">📸 Tomar Foto</button>
        <img v-if="image2" :src="image2" alt="Vista Previa" class="preview" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      image1: null,
      image2: null,
      videoStream: null,
    };
  },
  mounted() {
    this.startCamera();
  },
  methods: {
    // Manejar la carga de imágenes
    handleFileUpload(event, imageKey) {
      const file = event.target.files[0];
      if (file) {
        this[imageKey] = URL.createObjectURL(file);
      }
    },

    // Iniciar la cámara para capturar imágenes
    async startCamera() {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
          this.videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
          this.$refs.video.srcObject = this.videoStream;
        } catch (error) {
          console.error("Error al acceder a la cámara:", error);
        }
      }
    },

    // Capturar una imagen desde la webcam
    capturePhoto() {
      const canvas = document.createElement("canvas");
      const video = this.$refs.video;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      this.image2 = canvas.toDataURL("image/png"); // Convertir a imagen base64
    },
  },
  beforeUnmount() {
    // Detener la cámara cuando el componente se destruye
    if (this.videoStream) {
      this.videoStream.getTracks().forEach(track => track.stop());
    }
  },
};
</script>

<style>
/* Diseño General */
.container {
  text-align: center;
  font-family: Arial, sans-serif;
  padding: 20px;
  max-width: 900px;
  margin: auto;
}

/* Contenedor del Formulario */
.form-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

/* Caja de Carga/Captura */
.upload-box {
  border: 2px dashed #42b983;
  padding: 20px;
  width: 100%;
  max-width: 350px;
  text-align: center;
  background-color: #f9f9f9;
  border-radius: 10px;
}

/* Estilo para input */
input[type="file"] {
  margin-top: 10px;
  width: 100%;
}

/* Vista Previa de Imágenes */
.preview {
  width: 100%;
  height: auto;
  margin-top: 10px;
  border-radius: 8px;
}

/* Botón para Capturar Foto */
button {
  margin-top: 10px;
  padding: 10px 15px;
  border: none;
  background-color: #42b983;
  color: white;
  cursor: pointer;
  font-size: 16px;
  border-radius: 5px;
  width: 100%;
}

button:hover {
  background-color: #358a67;
}

/* 📌 RESPONSIVE DESIGN 📌 */
@media (max-width: 768px) {
  .form-container {
    flex-direction: column;
    align-items: center;
  }
  .upload-box {
    width: 90%;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 10px;
  }
  h1 {
    font-size: 22px;
  }
  .upload-box {
    width: 100%;
  }
}
</style>
