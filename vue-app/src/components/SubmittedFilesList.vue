<template>
    <div class="submitted-files">
      <h2>Submitted Files</h2>
      <ul>
        <li v-for="(file, index) in files" :key="index">
          {{ file.name }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SubmittedFilesList',
    props: {
      files: {
        type: Array,
        required: true
      }
    }
  }
  </script>
  
  <style scoped>
  .submitted-files {
    background-color: #333333;
    padding: 20px;
    border-radius: 8px;
  }
  
  h2 {
    color: white;
    margin-bottom: 10px;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    color: #999999;
    margin-bottom: 5px;
  }
  </style>
  