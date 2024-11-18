<template>
  <aside :class="`${ isExtended && 'is-extended' }`">
    <div class="menu-toggle-wrap">
      <button class="menu-toggle" @click="ToggleMenu">
        <span class="material-symbols-outlined">
          arrow_forward_ios
        </span>
    </button>
    </div>

    <h3>menu</h3>
    <div class="menu">
      <router-link class="button" to="/">
        <span class="material-symbols-outlined">
          home
        </span>
        <span class="text">Home</span>
      </router-link>
      <router-link class="button" to="/files">
        <span class="material-symbols-outlined">
          folder
        </span>
        <span class="text">Files</span>
      </router-link>
      <router-link class="button" to="/details">
        <span class="material-symbols-outlined">
          analytics
        </span>
        <span class="text">Details</span>
      </router-link>
      
    </div>

    <div class="flex"></div>

    <div class="menu">
    <router-link class="button" to="/search">
      <span class="material-symbols-outlined">
        search
      </span>
      <span class="text">Search</span>
    </router-link>

    <router-link class="button" to="/settings">
      <span class="material-symbols-outlined">
        settings
      </span>
      <span class="text">Settings</span>
    </router-link>
    </div>
  </aside>
  
</template>

<script setup>
import { ref } from 'vue'

const isExtended = ref(false)
const ToggleMenu = () => {
  isExtended.value = !isExtended.value

} 

</script>

<style lang="scss" scoped>
  aside {
    display : flex;
    flex-direction: column;
    width: calc(2rem + 32px);
    min-height: 100vh;
    overflow: hidden;
    background-color: var(--primary);
    color : white;
    padding : 1rem;

    transition: 0.2s ease-out;

    .flex {
      flex: 1 1 0;
    }

    .menu-toggle-wrap {
      display: flex;
      justify-content: flex-end;

      margin-bottom : 1rem;
      // position: relative;

      top:0rem;
      transition: 0.2s ease-out;

      .menu-toggle {
        transition: 0.2s ease-out;

        .material-symbols-outlined {
          font-size: 2rem;
          color: var(white);
          transition: 0.2s ease-out;

        }

        &:hover {
          .material-symbols-outlined{
            color: var(--primary);
            transform: translateY(0.5rem);
          }
        }
      }
    }

    h3, .button .text {
      opacity: 0;
      transition: 0.3s ease-out;
    }

    h3 {
      color: white;
      font-size: 0.875rem;
      margin-bottom: 0.5rem;
      text-transform: uppercase;
    }

    .menu {
      margin: 0 -1rem;

      .button {

        display: flex;
        align-items: center;
        text-decoration: none;

        padding: 0.5rem 1rem;
        transition:0.2s ease-out;

        .material-symbols-outlined {
          font-size: 2rem;
          color: white;
          transition: 0.2s ease-out;
        }

        .text {
          color: white;
          transition: 0.2s ease-out;
        }

        &:hover , &.router-link-exact-active{

          background: var(--primary);

          .material-symbols-outlined ,.text {
            color: var(--primary-on);
          }
        }

        &.router-link-exact-active{
          border-right: 5px solid var(--primary-on);
        }
      }
    }

    &.is-extended{
      width: 300px;

      .menu-toggle-wrap {
        top: -3rem;
        .menu-toggle {
          transform: rotate(-180deg);
        }
      }

      h3, .button .text {
        opacity: 1;
      }

      .button {
        .material-symbols-outlined {
          margin-right: 1rem;
        }
      }
    }

    @media (max-width: 768px) {
      position: fixed;
      z-index: 99;
    }
    
    

  }
</style>