<!-- <script setup >
    import GraphDijkstra from '../components/GraphDijkstra.vue'

</script>

<template>
    <main class="files-page">
          <GraphDijkstra/>
    </main>
</template> -->

<template>
    <main class="files-page">
          <!-- <h1>Files page</h1>
          <p>
              This is the Files page.
          </p> -->
          <FileUploader/>
          <!-- <SubmittedFilesList/> -->
    </main>
</template>

<script setup>
    import FileUploader from '../components/FileUploader.vue'
    // import SubmittedFilesList from '../components/SubmittedFilesList.vue';
</script>