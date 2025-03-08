<template>
  <div class="container">
    <h1>Upload or Capture Images</h1>
    <p>Select two images or take a photo from the second box.</p>

    <div class="form-container">
      <!-- Image Upload Box 1 -->
      <div class="upload-box">
        <label>Upload Image 1:</label>
        <input type="file" accept="image/*" @change="handleFileUpload($event, 'image1')" />
        <img v-if="image1" :src="image1" alt="Preview" class="preview" />
      </div>

      <!-- Image Upload / Capture Box -->
      <div class="upload-box">
        <label>Upload Image 2 or Take a Photo:</label>
        <input type="file" accept="image/*" @change="handleFileUpload($event, 'image2')" />
        <video v-if="!image2" ref="video" autoplay class="preview"></video>
        <button v-if="!image2" @click="capturePhoto">Capture Photo</button>
        <img v-if="image2" :src="image2" alt="Preview" class="preview" />
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
    // Handle image upload
    handleFileUpload(event, imageKey) {
      const file = event.target.files[0];
      if (file) {
        this[imageKey] = URL.createObjectURL(file);
      }
    },

    // Start the camera for capturing images
    async startCamera() {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
          this.videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
          this.$refs.video.srcObject = this.videoStream;
        } catch (error) {
          console.error("Error accessing webcam:", error);
        }
      }
    },

    // Capture an image from the webcam
    capturePhoto() {
      const canvas = document.createElement("canvas");
      const video = this.$refs.video;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      this.image2 = canvas.toDataURL("image/png"); // Convert to Base64 image
    },
  },
  beforeUnmount() {
    // Stop the camera stream when the component is destroyed
    if (this.videoStream) {
      this.videoStream.getTracks().forEach(track => track.stop());
    }
  },
};
</script>

<style>
.container {
  text-align: center;
  font-family: Arial, sans-serif;
}

.form-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.upload-box {
  border: 2px dashed #42b983;
  padding: 20px;
  width: 250px;
  text-align: center;
  background-color: #f9f9f9;
}

input[type="file"] {
  margin-top: 10px;
}

.preview {
  width: 100%;
  height: auto;
  margin-top: 10px;
}

button {
  margin-top: 10px;
  padding: 8px 15px;
  border: none;
  background-color: #42b983;
  color: white;
  cursor: pointer;
  font-size: 14px;
}

button:hover {
  background-color: #358a67;
}
</style>