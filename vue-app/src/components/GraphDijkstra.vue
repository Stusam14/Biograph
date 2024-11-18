<script setup lang="ts">
import { ref, type Ref } from 'vue'
import { VueForceGraph2D } from 'vue-force-graph'

const DATA_URL = 'http://localhost:8000/source-data'

let graphData = ref<any>({
  nodes: [],
  links: []
})
fetch(DATA_URL)
  .then((res) => res.json())
  .then((data) => (graphData.value = data))
</script>

<template>
  <VueForceGraph2D
    v-if="!graphData.length"
    :graphData
    nodeLabel="name"
    nodeAutoColorBy="community"
    linkDirectionalParticles="value"
    :linkDirectionalParticleSpeed="(d: Ref<number>) => d.value * 0.008"
    backgroundColor="#090723"
    :linkColor="() => 'rgba(255,255,255,.2)'"
  ></VueForceGraph2D>
</template>
