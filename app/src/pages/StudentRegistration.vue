<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="w-full max-w-[500px] p-6 bg-gray-100 rounded-xl shadow-lg">
        <h2 class="text-2xl font-bold text-center mb-6">Cadastro de Alunos</h2>
       
        <form @submit.prevent="submitForm" class="space-y-4">
            <div class="form-control">
                <label for="name" class="label">
                <span class="label-text">Nome</span>
                </label>
                <input id="name" v-model="form.name" required class="input input-bordered w-full" />
            </div>

            <div class="form-control">
              <label for="email" class="label">
                <span class="label-text">E-mail</span>
                </label>
                <input id="email" type="email" v-model="form.email" required class="input input-bordered w-full" />
            </div>

            <div class="form-control">
              <label for="password" class="label">
                <span class="label-text">Senha</span>
                </label>
                <input id="password" type="password" v-model="form.password" required class="input input-bordered w-full" />
            </div>

              <div class="form-control">
              <label for="phone" class="label">
                <span class="label-text">Telefone</span>
                </label>
                <input id="phone" v-model="form.phone" required class="input input-bordered w-full" />
            </div>
            <div>
                <label for="university">Universidade:</label>
                <select id="university" v-model="form.university" required>
                    <option value="" disabled>Selecione</option>
                    <option value="UESPI">UESPI</option>
                    <option value="IFPI">IFPI</option>
                    <option value="CHRISFAPI">CHRISFAPI</option>
                </select>
            </div>
            <div>
                <label for="shift">Turno:</label>
                <select id="shift" v-model="form.shift" required>
                    <option value="" disabled>Selecione</option>
                    <option value="Manhã">Manhã</option>
                    <option value="Tarde">Tarde</option>
                    <option value="Noite">Noite</option>
                </select>
            </div>
            <button type="submit" class="btn bg-black text-white hover:bg-gray-800 w-full">Cadastrar</button>
        </form>
    </div>
    </div>
</template>

<script>
export default {
    name: 'StudentRegistration',
    data() {
        return {
            form: {
                name: '',
                email: '',
                password: '',
                phone: '',
                university: '',
                shift: ''
            }
        };
    },
    methods: {
        submitForm() {
            alert('Cadastro realizado com sucesso!');

            this.form = {
                name: '',
                email: '',
                password: '',
                phone: '',
                university: '',
                shift: ''
            };
        }
    }
};
</script>