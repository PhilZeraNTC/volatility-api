<script setup>
import LigaLogo from './assets/Liga.svg'
import { ref } from 'vue'
  
const menuAberto = ref(false)
</script>

<template>
  <header class="header-estilizado">
    <div class="container">
      <a href="/" class="logo">
        <img :src="LigaLogo" alt="Logo" class="icone-logo" />
        <div class="logo-text-wrapper">
          <span class="texto-logo">Liga UTFPR</span>
          <span class="subtexto-logo">Predictor</span>
        </div>
      </a>


      <nav :class="['navegacao', { 'ativo': menuAberto }]">
        <router-link to="/" class="nav-link">Início</router-link>
        <router-link to="/playground" class="nav-link">Playground</router-link>
        <router-link to="/#sobre" class="nav-link">Sobre</router-link>
      </nav>
    </div>
  </header>

  <main class="conteudo-principal">
    <router-view />
  </main>
  <footer class="footer-simples">
    <p>&copy; 2026 Liga de Mercado Financeiro - UTFPR</p>
  </footer>
</template>


<style scoped>
.conteudo-principal {
  flex-grow: 1; 
  min-height: calc(100vh - 150px);
  padding-bottom: 40px;
}
.header-estilizado {
  background: rgba(15, 17, 26, 0.8); /* Fundo semi-transparente */
  backdrop-filter: blur(12px);      /* Efeito de vidro embaçado */
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 1000;
}
.navegacao {
  display: flex;
  align-items: center;
  gap: 24px; /* Espaço entre os links */
}

.nav-link {
  text-decoration: none;
  color: var(--text);
  font-weight: 600;
  font-size: 0.95rem;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: var(--accent);
  background: var(--accent-bg);
}

.router-link-active {
  color: var(--accent);
}

.container {
  max-width: 1126px;
  margin: 0 auto;
  padding: 0.8rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
}

.icone-logo {
  height: 40px;
  width: auto;
}

.logo-text-wrapper {
  color: #fff;
  display: flex;
  flex-direction: column;
}

.texto-logo {
  color: var(--text-h);
  font-weight: 700;
  font-size: 1.1rem;
  line-height: 1;
}

.subtexto-logo {
  color: var(--accent);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-shadow: 0 0 10px rgba(243, 189, 72, 0.3);
  animation: pulse-glow 3s infinite;
}

@keyframes pulse-glow {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.footer-simples {
  padding: 40px;
  border-top: 1px solid var(--border);
  text-align: center;
  font-size: 0.85rem;
  color: var(--text);
}
</style>
