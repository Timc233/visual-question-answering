<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
</script>

<template>
  <transition name="fade">
    <router-view></router-view>
  </transition>

  <div class="buttons">
    <div class="button"><router-link to="/photo">Take photo</router-link></div>
    <div class="button"><router-link to="/recorder">Record voice</router-link></div>
  </div>
  
  
</template>

<style scoped>
.buttons{
  position: absolute;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: space-around;
}
.button{
 padding: 20px;
 background: #f9f9f9;
}
</style>
