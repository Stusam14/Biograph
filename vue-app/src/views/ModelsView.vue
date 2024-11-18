<template>
  <h1>Models :</h1>
  <DataTable
    :value="data"
    paginator
    :rows="25"
    :rowsPerPageOptions="[25, 50]"
    tableStyle="min-width: 50rem"
    class="center"
  >
    <Column field="name" header="Molecule"></Column>
    <Column field="cluster" header="Cluster"></Column>
  </DataTable>
</template>

<script setup lang="ts">
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { useFetch } from '@/api/api'
const { data, error } = useFetch('http://localhost:8000/species')
</script>

<style scoped>
.center {
  margin: 0 auto;
  width: 95%;
}
</style>
