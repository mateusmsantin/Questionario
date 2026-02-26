<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title class="text-center">
          Projeto Lagoa Mirim
        </q-toolbar-title>

        <q-btn
          v-if="isLoggedIn"
          flat
          round
          dense
          icon="logout"
          @click="logout"
        >
          <q-tooltip>Sair</q-tooltip>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-page-container class="bg-grey-1">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Verifica se o usuário está logado apenas checando se existe um token
const isLoggedIn = computed(() => !!localStorage.getItem('token'))

const logout = () => {
  localStorage.removeItem('token')
  router.push('/')
  // Força um refresh se necessário ou apenas redireciona
  window.location.reload()
}
</script>

<style scoped>
/* Estilo opcional para dar um ar mais limpo */
.q-toolbar-title {
  font-weight: bold;
  letter-spacing: 1px;
}
</style>
