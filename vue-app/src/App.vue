<script setup lang="ts">
  import Sidebar from './components/Sidebar.vue';
</script>

<template>
  <main class="app">
    <Sidebar/>
    <router-view/>
  </main>
</template>

<style lang="scss">

:root{
  --primary : #2b2e2d;
  --primary-on : #D0D0D1;
  --graph-background : #161515;

}

*{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'josefin', 'rubik';

}

body{
  background: var(--graph-background);
  color: white;
}

button{
  cursor : pointer;
  appearance: none;
  border : none;
  outline: none;
  background: none;
}

.app{
  // position: relative;
  margin: 0;
  display: flex;
  // padding: 2rem;
  // margin: 0;
  // background-color : blue ;

  main{
    flex: 1 1 0;
    padding: 2rem;


    @media (max-width : 768px) {
    padding-left: 6rem;
  }
  }
}
</style>

