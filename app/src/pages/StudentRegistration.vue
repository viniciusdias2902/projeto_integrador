<template>
    <div class="student-registration">
        <h2>Cadastro de Alunos</h2>
        <form @submit.prevent="submitForm">
            <div>
                <label for="name">Nome:</label>
                <input id="name" v-model="form.name" required />
            </div>
            <div>
                <label for="email">E-mail:</label>
                <input id="email" type="email" v-model="form.email" required />
            </div>
            <div>
                <label for="password">Senha:</label>
                <input id="password" type="password" v-model="form.password" required />
            </div>
            <div>
                <label for="phone">Telefone:</label>
                <input id="phone" v-model="form.phone" required />
            </div>
            <div>
                <label for="university">Universidade:</label>
                <input id="university" v-model="form.university" required />
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
            <button type="submit">Cadastrar</button>
        </form>
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

<style scoped>
.student-registration {
    max-width: 400px;
    margin: 40px auto;
    padding: 24px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background: #fafafa;
}
.student-registration h2 {
    text-align: center;
    margin-bottom: 24px;
}
.student-registration form > div {
    margin-bottom: 16px;
}
.student-registration label {
    display: block;
    margin-bottom: 4px;
    font-weight: bold;
}
.student-registration input,
.student-registration select {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
}
.student-registration button {
    width: 100%;
    padding: 10px;
    background: #1976d2;
    color: #fff;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
}
.student-registration button:hover {
    background: #1565c0;
}
</style>