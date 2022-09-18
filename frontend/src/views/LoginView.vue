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
                    <input type="text" v-model="name" :class="[{wrong: nameMessage}]" @blur="nameFocus = false"
                        @focus="nameFocus = true">
                    <span :class="['tooltiptext', {active: name}, {show: nameFocus}]">{{nameMessage}}</span>
                </div>
            </div>
            <div class="field">
                <div class="label">Логин</div>
                <div class="input-container">
                    <input type="text" :class="[{wrong: loginMessage}]" v-model="login" @blur="loginFocus = false"
                        @focus="loginFocus = true">
                    <span :class="['tooltiptext', {active: login}, {show: loginFocus}]">{{loginMessage}}</span>
                </div>

            </div>
            <div class="field">
                <div class="label">Пароль</div>
                <div class="input-container">
                    <input type="password" :class="[{wrong: passwordMessage}]" v-model="password"
                        @blur="passwordFocus = false" @focus="passwordFocus = true">
                    <span :class="['tooltiptext', {active: password}, {show: passwordFocus}]">{{passwordMessage}}</span>
                </div>
            </div>
        </div>
        <div :class="['button', {active: isButtonActive}]" @click="buttonHandler">
            <span v-if="loginActive">Войти</span>
            <span v-else>Зарегистрироваться</span>
        </div>
    </FormContainer>
</template>
<script>
import { storeToRefs } from 'pinia';
import FormContainer from '../components/FormContainer.vue';
import { useAuthStore } from '../stores/auth';
export default {
    setup() {
        const { token, loading, message } = storeToRefs(useAuthStore());
        const { loginRequest } = useAuthStore();
        return {
            loginRequest,
            token,
            loading,
            message
        }
    },
    components: { FormContainer },
    data() {
        return {
            loginActive: true,

            login: '',
            loginMessage: '',
            loginFocus: false,

            password: '',
            passwordMessage: '',
            passwordFocus: false,

            name: '',
            nameMessage: '',
            nameFocus: false,
        }
    },
    methods: {
        buttonHandler() {
            if (this.loginActive) {
                this.loginRequest(this.login, this.password)
            }
        }
    },
    computed: {
        loginIsValid() {
            if (!this.login) return
            if (this.loginActive) {
                this.loginMessage = '';
                return true
            }
            let value = this.login;
            if (/[\s]/.test(value)) {
                this.loginMessage = 'В логине зарещены пробельные символы';
                return
            }
            if (value.length < 5) {
                this.loginMessage = 'Логин должен быть более 5 символов';
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
            if (this.loginActive) {
                this.passwordMessage = '';
                return true
            }
            let value = this.password;
            var messageBase = 'Пароль должен содержать ';
            if (!/[A-Z]/.test(value)) {
                this.passwordMessage = messageBase + 'ПРОПИСНЫЕ английские Абуквы';
                return
            }
            if (!/[a-z]/.test(value)) {
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
            if (this.password.length < 8) {
                this.passwordMessage = messageBase + ' более 8 символов';
                return
            }
            this.passwordMessage = '';
            return true
        },
        nameIsValid() {
            if (!this.name) return
            let value = this.name;
            if (value.length < 3) {
                this.nameMessage = 'Имя должено быть более 3 символов';
                return
            }
            if (value.length > 15) {
                this.nameMessage = 'Имя должено быть менее 15 символов';
                return
            }
            this.nameMessage = '';
            return true
        },
        fieldsIsEmpty() {
            return this.login.length === 0 || this.password.length === 0 || (this.loginActive ? false : this.nameIsValid)
        },
        isButtonActive() {
            return (this.loginIsValid & this.passwordIsValid) & (this.loginActive ? true : this.nameIsValid)
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/themes';
@use '@/assets/styles/breakpoints';

.selector,
.fields-area,
.button {
    background-color: var(--color-background-mute-2);
    padding: 5px;
    border-radius: 20px;
    user-select: none;
}

.selector {
    gap: 5px;
    @include helpers.flex-center;

    .item {
        text-align: center;
        flex-grow: 1;
        border-radius: 15px;
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
        padding: 5px 2px;
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
                padding: 2px 10px;
                height: 35px;
                color: var(--color-text);
                font-size: 1.02em;
                outline: none;
                width: 100%;
                border-radius: 10px;
                border: 1px solid transparent;

                &.wrong {
                    border-color: var(--red-0);

                    @include themes.light {
                        border-color: red;
                    }
                }
            }

            .tooltiptext {
                visibility: hidden;
                width: 200px;
                background-color: black;
                color: #fff;
                text-align: center;
                padding: 5px;
                border-radius: 6px;
                position: absolute;
                z-index: 1;

                &.show.active:not(:empty) {
                    visibility: visible;
                }

                @include breakpoints.md {
                    top: -20%;
                    left: calc(100% + 5px);
                }

                @include breakpoints.md(true) {
                    bottom: 110%;
                    left: 50%;
                    margin-left: -100px;
                }

                &::after {
                    content: " ";
                    position: absolute;
                    top: 50%;
                    right: 100%;

                    @include breakpoints.md(true) {
                        top: 100%;
                        left: 50%;
                    }

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
    user-select: none;
    min-height: 31px;
    color: var(--color-header-text);

    &.active {
        color: var(--color-text);
        cursor: pointer;
        background-color: var(--color-background-mute-3);
    }

}
</style>