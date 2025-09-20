<template>
  <div class="max-w-md mx-auto bg-base-100 shadow-md rounded-box p-6 mb-4 lg:w-96 w-60">
    <h2 class="text-xl font-bold mb-4">Segunda-feira</h2>

    <form class="space-y-3">
      <label class="flex items-center gap-3 cursor-pointer">
        <input type="radio" name="segunda" class="radio checked" value="vou_e_volto" />
        <span class="label-text">Vou e volto</span>
      </label>

      <label class="flex items-center gap-3 cursor-pointer">
        <input type="radio" name="segunda" class="radio checked" value="apenas_vou" />
        <span class="label-text">Apenas vou</span>
      </label>

      <label class="flex items-center gap-3 cursor-pointer">
        <input type="radio" name="segunda" class="radio checked" value="apenas_volto" />
        <span class="label-text">Apenas volto</span>
      </label>

      <label class="flex items-center gap-3 cursor-pointer">
        <input type="radio" name="segunda" class="radio checked" value="nao_vou" />
        <span class="label-text">Não vou</span>
      </label>

      <button type="submit" class="btn btn-success btn-block mt-4">Enviar resposta</button>
    </form>
  </div>
</template>
