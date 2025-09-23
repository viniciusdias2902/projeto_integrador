<template>
  <div class="flex h-screen flex-col">
    <NavBar />
    <main class="flex-1 flex items-center justify-center bg-red-200">
      <slot></slot>
    </main>
    <FooterComponent />
  </div>
</template>
