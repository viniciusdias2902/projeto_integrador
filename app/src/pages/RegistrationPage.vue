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
                    <option value="M">Manhã</option>
                    <option value="A">Tarde</option>
                    <option value="E">Noite</option>
                    <option value="M-A">Manhã e Tarde</option>
                    <option value="A-E">Tarde e Noite</option>
                </select>
            </div>
            <button type="submit" class="btn bg-black text-white hover:bg-gray-800 w-full">Cadastrar</button>
        </form>
        <p v-if="sucessMessage" class="mt-4 text-green-600 text-center">Bem-vindo, {{ sucessMessage }}!</p>
        <p v-if="errorMessage" class="mt-4 text-red-600 text-center">{{ errorMessage }}</p>
    </div>
    </div>
</template>

<script>
export default {
    name: 'RegistrationPage',
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
        async submitForm() {
            try{
            const response = await fetch('https://localhost:8000/api/v1/students/1/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.form)
            });

            if(!response.ok) {
                throw new Error('Erro ao cadastrar aluno');
            }

            const data = await response.json();
            console.log('Success:', data);

            this.sucessMessage = "Cadastro realizado com sucesso!";
            this.errorMessage = '';

            this.form = {
                name: '',
                email: '',
                password: '',
                phone: '',
                university: '',
                shift: ''
            };
        } catch (error) {
            console.error('Error:', error);
            this.errorMessage = 'Erro ao cadastrar aluno. Tente novamente.';
            this.sucessMessage = '';
        }
        },
    },
};
</script>