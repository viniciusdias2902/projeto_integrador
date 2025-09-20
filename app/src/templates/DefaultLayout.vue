<template>
  <div class="flex h-screen flex-col items-center">
    <NavBar />
    <main class="flex-1 flex items-center justify-center">
      <slot></slot>
    </main>
    <FooterComponent />
  </div>
</template>
