<template>
  <div class="file-uploader">
    <h1>SBML to Graph Converter</h1>

    <!-- File Upload Section -->
    <div
      class="upload-area"
      @dragover.prevent
      @drop.prevent="handleDrop"
      v-if="selectedFiles.length === 0"
    >
      <div class="icon">📄</div>
      <label for="file-input" class="choose-files-button">
        CHOOSE FILES
        <input
          id="file-input"
          type="file"
          @change="handleFileChange"
          accept=".xml"
          multiple
          class="hidden-input"
        />
      </label>
      <p class="drop-text">or drop files here</p>
    </div>

    <div v-else>
      <!-- Display Selected Files in Grid Format -->
      <div class="file-grid">
        <div v-for="(file, index) in selectedFiles" :key="file.name" class="file-item">
          <button @click="removeFile(index)" class="remove-button">
            <img :src="removeIcon" alt="Remove Icon" />
          </button>
          <div class="file-icon">
            <img :src="frameIcon" alt="Frame Icon" />
          </div>
          <span class="file-name">{{ file.name }}</span>
        </div>
      </div>

      <!-- Add More Files and Convert Button -->
      <div class="button-group">
        <label for="add-more-files" class="add-file-button">
          Add more files
          <input
            id="add-more-files"
            type="file"
            @change="handleFileChange"
            accept=".xml"
            multiple
            class="hidden-input"
          />
        </label>
        <button class="convert-button" @click="convert">Convert</button>
      </div>
    </div>

    <!-- Display Submitted Files -->
    <SubmittedFilesList v-if="submittedFiles.length > 0" :files="submittedFiles" />
  </div>
</template>

<script>
// Import the SubmittedFilesList component
import SubmittedFilesList from './SubmittedFilesList.vue'
import frameIcon from '@/assets/Frame 1.svg' // Import image for Vite support
import removeIcon from '@/assets/Frame 2.svg' // Import remove image
import { uploadFiles } from '@/api/api'

export default {
  name: 'DarkFileUploader',
  components: {
    SubmittedFilesList
  },
  data() {
    return {
      selectedFiles: [], // Files selected for upload
      submittedFiles: [], // Files that have been submitted
      frameIcon, // Referencing imported image
      removeIcon // Referencing imported remove image
    }
  },
  methods: {
    handleFileChange(event) {
      const newFiles = Array.from(event.target.files)
      // Filter to avoid duplicate files
      const uniqueFiles = newFiles.filter(
        (newFile) => !this.selectedFiles.some((existingFile) => existingFile.name === newFile.name)
      )
      this.selectedFiles = [...this.selectedFiles, ...uniqueFiles]

      // Reset input value to allow re-selection of same files
      event.target.value = ''
    },
    handleDrop(event) {
      const droppedFiles = Array.from(event.dataTransfer.files)
      this.handleFileChange({ target: { files: droppedFiles } })
    },
    removeFile(index) {
      this.selectedFiles.splice(index, 1) // Remove the selected file by index
    },
    async convert() {
      // Move selected files to submittedFiles
      this.submittedFiles = [...this.submittedFiles, ...this.selectedFiles]
      // Clear selected files after submission
      console.log('Files submitted:', this.submittedFiles)

      try {
        await uploadFiles(this.selectedFiles)
        this.selectedFiles = []
      } catch (error) {
        // TODO : <Error/> to render
      }
    }
  }
}
</script>

<style scoped>
.file-uploader {
  font-family: Arial, sans-serif;
  background-color: #1a1a1a;
  color: #ffffff;
  padding: 20px;
  border-radius: 8px;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.upload-area {
  background-color: #333333;
  border: 2px dashed #666666;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  margin-bottom: 20px;
}

.icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.choose-files-button,
.add-file-button,
.convert-button {
  background-color: #4a4a4a;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  display: inline-block;
  margin-bottom: 10px;
  font-size: 14px;
  border: none;
}

.convert-button {
  background-color: #2c5282;
}

.drop-text {
  color: #999999;
  margin-top: 10px;
}

/* Grid layout for file display */
.file-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
  background-color: #333333;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.file-item {
  position: relative; /* Make position relative to position the button */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between; /* Align items */
  background-color: #444444;
  border-radius: 8px;
  padding: 10px;
  width: 150px; /* Fixed width */
  height: 150px; /* Fixed height */
}

.remove-button {
  position: absolute; /* Position at the top right corner */
  top: 10px;
  right: 10px;
  background-color: #ff4136;
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
}

.file-icon {
  padding: 5px;
  border-radius: 3px;
  margin-bottom: 5px; /* Reduced margin */
  width: 100px; /* Set a fixed width for the icon */
  height: 150px; /* Set a fixed height for the icon */
}

.file-icon img {
  width: 100%; /* Make the icon responsive within the fixed dimensions */
  height: auto; /* Maintain aspect ratio */
}

.file-name {
  color: #ffffff;
  margin-top: 15px; /* Adjusted to lower the position */
  font-size: 14px;
  text-align: center; /* Center text */
}

.button-group {
  display: flex;
  gap: 10px;
  justify-content: space-between;
}

.hidden-input {
  display: none;
}
</style>

<!-- <template>
  <div class="file-uploader">
    <h1>SBML to Graph converter</h1>
    <div class="upload-area" v-if="selectedFiles.length === 0">
      <div class="icon">
        📄
      </div>
      <label for="file-input" class="choose-files-button">
        CHOOSE FILES
        <input
          id="file-input"
          type="file"
          @change="handleFileChange"
          accept=".xml"
          multiple
          class="hidden-input"
        >
      </label>
      <p class="drop-text">or drop files here</p>
    </div>
    <div v-else>
      <div class="file-display">
        <div v-for="(file, index) in selectedFiles" :key="file.name" class="file-item">
          <div class="file-icon"><img :src="require('@/assets/Frame 1.svg')" alt="Frame Icon"></div>
          <span class="file-name">{{ file.name }}</span>
          <button @click="removeFile(index)" class="remove-button">
            <img :src="require('@/assets/Frame 2.svg')" alt="Frame Icon">
          </button>
        </div>
      </div>
      <div class="button-group">
        <label for="add-more-files" class="add-file-button">
          Add file
          <input
            id="add-more-files"
            type="file"
            @change="handleFileChange"
            accept=".xml"
            multiple
            class="hidden-input"
          >
        </label>
        <button class="convert-button" @click="convert">Convert</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DarkFileUploader',
  data() {
    return {
      selectedFiles: []
    }
  },
  methods: {
    handleFileChange(event) {
      const newFiles = Array.from(event.target.files)
      this.selectedFiles = [...this.selectedFiles, ...newFiles]
    },
    removeFile(index) {
      this.selectedFiles.splice(index, 1)
    },
    convert() {
      // Placeholder for conversion functionality
      console.log('Convert button clicked')
    }
  }
}
</script>

<style scoped>
.file-uploader {
  font-family: Arial, sans-serif;
  background-color: #1a1a1a;
  color: #ffffff;
  padding: 20px;
  border-radius: 8px;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.upload-area {
  background-color: #333333;
  border: 2px dashed #666666;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  margin-bottom: 20px;
}

.icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.choose-files-button, .add-file-button, .convert-button {
  background-color: #4a4a4a;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  display: inline-block;
  margin-bottom: 10px;
  font-size: 14px;
  border: none;
}

.convert-button {
  background-color: #2c5282;
}

.drop-text {
  color: #999999;
  margin-top: 10px;
}

.file-display {
  background-color: #333333;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.file-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.file-icon {
  padding: 2px 5px;
  border-radius: 3px;
  margin-right: 10px;

}

.file-name {
  flex-grow: 1;
}

.remove-button {
  background-color: #ff4136;
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
}

.button-group {
  display: flex;
  justify-content: space-between;
}

.hidden-input {
  display: none;
}
</style> -->
