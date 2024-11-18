<script setup >
    import GraphDijkstra from '../components/GraphDijkstra.vue'

</script>

<template>
    <div class="graph-container">
        <main class="files-page">
          <GraphDijkstra/>
        </main>
    </div>
</template>

<style scoped>

.graph-container {
    width: 100vw; /* Full viewport width */
    height: 100vh; /* Full viewport height */
    /* border: 1px solid #3E403F; */
    /* overflow: hidden; Prevent overflow */
    overflow:scroll;
    margin: 0;
    padding: 0;
}

canvas {
    margin: 0;
    padding: 0;
}

</style>