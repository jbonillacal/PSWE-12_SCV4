<template>
  <div class="container">
    <h1>Sube o Captura Imágenes</h1>
    <p>Selecciona dos imágenes o toma una foto desde la segunda caja.</p>

    <!-- Botón de inicio de sesión de Google -->
    <div v-if="!user" class="auth-container">
      <div id="g_id_onload"
           data-client_id="25106593702-5jgm5sm4c0s9vcmmc846l073o7ahkb9p.apps.googleusercontent.com"
           data-callback="handleCredentialResponse">
      </div>
      <div class="g_id_signin" data-type="standard"></div>
    </div>

    <!-- Mostrar el nombre e imagen del usuario autenticado -->
    <div v-if="user" class="user-info">
      <p>Bienvenido, {{ user.name }}</p>
      <img :src="user.picture" alt="Perfil" class="profile-pic"/>
    </div>

    <div class="form-container" v-if="user">
      <!-- Caja para Subir Imagen 1 -->
      <div class="upload-box">
        <label>Subir Imagen 1:</label>
        <input type="file" accept="image/*" @change="handleFileUpload($event, 'image1')" />
        <img v-if="image1" :src="image1Preview" alt="Vista Previa" class="preview" />
      </div>

      <!-- Caja para Subir o Capturar Imagen 2 -->
      <div class="upload-box">
        <label>Subir Imagen 2 o Capturar Foto:</label>
        <input type="file" accept="image/*" @change="handleFileUpload($event, 'image2')" />
        <video v-if="!image2" ref="video" autoplay class="preview"></video>
        <button v-if="!image2" @click="capturePhoto">📸 Tomar Foto</button>
        <img v-if="image2" :src="image2Preview" alt="Vista Previa" class="preview" />
      </div>
    </div>

    <button v-if="user" @click="verifyIdentity" :disabled="!image1 || !image2 || isLoading">Verificar Identidad</button>
    
    <div v-if="isLoading" class="loading-bar-container">
      <div class="loading-bar"></div>
    </div>

    <p v-if="result" :class="{'match': result === 'Las imágenes coinciden', 'no-match': result === 'Las imágenes no coinciden'}">
      {{ result }}
    </p>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      image1: null,
      image2: null,
      image1Preview: null,
      image2Preview: null,
      videoStream: null,
      result: null,
      isLoading: false,
      user: null
    };
  },
  methods: {
    loadGoogleSSO() {
      const script = document.createElement('script');
      script.src = "https://accounts.google.com/gsi/client";
      script.async = true;
      document.head.appendChild(script);
      window.handleCredentialResponse = this.handleCredentialResponse;
    },
    handleCredentialResponse(response) {
      const payload = JSON.parse(atob(response.credential.split('.')[1]));
      this.user = {
        name: payload.name,
        email: payload.email,
        picture: payload.picture
      };
      this.startCamera(); // 🔑 Inicia la cámara después de la autenticación
    },
    handleFileUpload(event, imageKey) {
      const file = event.target.files[0];
      if (file) {
        this[imageKey] = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          if (imageKey === 'image1') {
            this.image1Preview = e.target.result;
          } else {
            this.image2Preview = e.target.result;
          }
        };
        reader.readAsDataURL(file);
      }
    },
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
    capturePhoto() {
      const canvas = document.createElement("canvas");
      const video = this.$refs.video;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      canvas.toBlob(blob => {
        this.image2 = blob;
        this.image2Preview = URL.createObjectURL(blob);
      }, "image/png");
    },
    async verifyIdentity() {
      this.isLoading = true;
      this.result = null;
      const formData = new FormData();
      formData.append("id_picture", this.image1);
      formData.append("selfie", this.image2);
      
      try {
        const response = await fetch("https://us-central1-cenfotec2024.cloudfunctions.net/gcf-facial-recognition", {
          method: "POST",
          body: formData,
          mode: "cors"
        });
        const data = await response.json();
        this.result = data.match ? "Las imágenes coinciden" : "Las imágenes no coinciden";
      } catch (error) {
        console.error("Error en la verificación:", error);
        this.result = "Error al verificar identidad";
      } finally {
        this.isLoading = false;
      }
    }
  },
  mounted() {
    this.loadGoogleSSO();
  },
  beforeUnmount() {
    if (this.videoStream) {
      this.videoStream.getTracks().forEach(track => track.stop());
    }
  }
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

.loading-bar-container {
  width: 100%;
  height: 5px;
  background-color: #f0f0f0;
  margin-top: 10px;
}

.loading-bar {
  width: 100%;
  height: 100%;
  background-color: #42b983;
  animation: loading 1.5s infinite ease-in-out;
}

@keyframes loading {
  0% { transform: translateX(-100%); }
  50% { transform: translateX(0); }
  100% { transform: translateX(100%); }
}

.match {
  color: green;
  font-weight: bold;
  font-size: 1.5em;
}

.no-match {
  color: red;
  font-weight: bold;
  font-size: 1.5em;
  animation: blink 1s infinite alternate;
}

@keyframes blink {
  0% { opacity: 1; }
  100% { opacity: 0.5; }
}
</style>