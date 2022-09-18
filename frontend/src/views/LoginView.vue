<template>
    <FormContainer :formWidth="350">
        <div class="selector">
            <div :class="['item', {active: loginActive}]" @click="loginActive = true">Вход</div>
            <div :class="['item', {active: !loginActive}]" @click="loginActive = false">Регистрация</div>
        </div>
        <div class="fields-area">
            <div class="field" v-if="!loginActive">
                <div class="label">Отображаемое имя</div>
                <div class="input-container">
                    <input type="text" v-model="name" @blur="e => e.target.classList.remove('focus')"
                        @focus="e => e.target.classList.add('focus')">
                </div>
            </div>
            <div class="field">
                <div class="label">Логин</div>
                <div class="input-container">
                    <input type="text" v-model="login" @blur="e => e.target.classList.remove('focus')"
                        @focus="e => e.target.classList.add('focus')">
                    <span :class="['tooltiptext', {active: login}]">{{loginMessage}}</span>
                </div>

            </div>
            <div class="field">
                <div class="label">Пароль</div>
                <div class="input-container">
                    <input type="password" v-model="password" @blur="e => e.target.classList.remove('focus')"
                        @focus="e => e.target.classList.add('focus')">
                    <span :class="['tooltiptext', {active: password}]">{{passwordMessage}}</span>
                </div>
            </div>
        </div>
        <div :class="['button', {active: isButtonActive}]">
            <span v-if="loginActive">Войти</span>
            <span v-else>Зарегистрироваться</span>
        </div>
    </FormContainer>
</template>
<script>
import FormContainer from '../components/FormContainer.vue';
export default {
    components: { FormContainer },
    data() {
        return {
            loginActive: true,
            login: '',
            loginMessage: '',
            password: '',
            passwordMessage: '',
            name: ''
        }
    },
    computed: {
        loginIsValid() {
            if (!this.login) return
            let value = this.login;
            if (value.length < 3) {
                this.loginMessage = 'Логин должен быть более 3 символов';
                return
            }
            if (value.length > 20) {
                this.loginMessage = 'Логин должен быть менее 20 символов';
                return
            }
            this.loginMessage = '';
            return true
        },
        passwordIsValid() {
            if (!this.password) return
            if (this.loginActive) return true
            let value = this.password;
            var messageBase = 'Пароль должен содержать ';
            if (this.password.length < 8) {
                this.passwordMessage = messageBase + ' более 8 символов';
                return
            }
            if (!/\W/.test(value)) {
                this.passwordMessage = messageBase + 'ПРОПИСНЫЕ английские Абуквы';
                return
            }
            if (!/\w/.test(value)) {
                this.passwordMessage = messageBase + 'строчные английские буквы';
                return
            }
            if (!/[0-9]/.test(value)) {
                this.passwordMessage = messageBase + 'цифры';
                return
            }
            if (!/[#?!@$%^&*-]/.test(value)) {
                this.passwordMessage = messageBase + 'специальные символы (#?!@$%^&*-)';
                return
            }
            this.passwordMessage = '';
            return true
        },
        fieldsIsEmpty() {
            return this.login.length === 0 || this.password.length === 0
        },
        isButtonActive() {
            return this.loginIsValid & this.passwordIsValid
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/themes';

.selector,
.fields-area,
.button {
    background-color: var(--color-background-mute-2);
    padding: 5px;
    border-radius: 15px;
    user-select: none;
}

.selector {
    gap: 5px;
    @include helpers.flex-center;


    .item {
        text-align: center;
        flex-grow: 1;
        border-radius: 10px;
        padding: 5px;
        cursor: pointer;
        border: 1px solid transparent;

        &:not(.active):hover {
            @include themes.light {
                border-color: var(--color-background-mute-4);
            }

            @include themes.dark {
                background-color: var(--color-background-mute-3);
            }
        }

        &.active {
            cursor: auto;

            @include themes.light {
                background-color: var(--color-background-mute-3);
            }

            @include themes.dark {
                background-color: var(--color-background-mute-4);
            }
        }
    }
}

.fields-area {
    display: flex;
    flex-direction: column;

    .field {
        display: flex;
        flex-direction: column;
        padding: 5px;
        gap: 5px;

        .label {
            margin-left: 5px;
            font-size: calc(1em - 2px);
            color: var(--color-header-text);
        }

        .input-container {
            position: relative;
            display: inline-block;

            input {
                background-color: var(--color-background-mute-3);
                border: none;
                padding: 2px 10px;
                height: 35px;
                color: var(--color-text);
                font-size: 1.02em;
                outline: none;
                width: 100%;
                border-radius: 5px;
            }

            .tooltiptext {
                &.active:not(:empty) {
                    visibility: visible;
                }

                visibility: hidden;
                width: 200px;
                background-color: black;
                color: #fff;
                text-align: center;
                padding: 5px;
                border-radius: 6px;
                position: absolute;
                z-index: 1;
                top: -20%;
                left: 105%;

                &::after {
                    content: " ";
                    position: absolute;
                    top: 50%;
                    right: 100%;
                    margin-top: -5px;
                    border-width: 5px;
                    border-style: solid;
                    border-color: transparent black transparent transparent;
                }
            }
        }
    }
}

.button {
    text-align: center;
    padding: 10px;
    user-select: none;

    &.active {
        color: var(--color-text);
        cursor: pointer;
        background-color: var(--color-background-mute-3);
    }

    color: var(--color-header-text);
}
</style>