<script setup>
import LigaLogo from './assets/Liga.svg'
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
}
.header-estilizado {
  background: var(--bg);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.navegacao {
  display: flex;
  align-items: center;
  gap: 24px; /* Espaço entre os links */
}

.nav-link {
  text-decoration: none;
  color: var(--text); /* Cor suave vinda do seu style.css */
  font-weight: 500;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.nav-link:hover {
  color: var(--accent); /* Roxo ao passar o mouse */
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
}

.footer-simples {
  padding: 40px;
  border-top: 1px solid var(--border);
  text-align: center;
  font-size: 0.85rem;
  color: var(--text);
}
</style>