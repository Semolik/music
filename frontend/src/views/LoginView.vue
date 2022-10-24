<template>
    <FormContainer :formWidth="350" class="login-form">
        <div class="message" v-if="message">
            <FontAwesomeIcon icon="fa-triangle-exclamation" />
            <div class="text">{{ message }}</div>
        </div>
        <div class="selector">
            <div :class="['item', { active: loginActive }]" @click="loginActive = true">Вход</div>
            <div :class="['item', { active: !loginActive }]" @click="loginActive = false">Регистрация</div>
        </div>
        <div class="fields-area">
            <template v-if="!loginActive">
                <div class="field">
                    <div class="label">Имя</div>
                    <div class="input-container">
                        <input type="text" v-model="name" :class="[{ wrong: nameMessage.length !== 0 }]"
                            @blur="nameFocus = false" @focus="nameFocus = true">
                        <span :class="['tooltiptext', { active: name }, { show: nameFocus }]">
                            <div class="item" v-for="message in nameMessage">{{ message }}</div>
                        </span>
                    </div>
                </div>
                <div class="field">
                    <div class="label">Фамилия</div>
                    <div class="input-container">
                        <input type="text" v-model="lastName" :class="[{ wrong: lastNameMessage.length !== 0 }]"
                            @blur="lastNameFocus = false" @focus="lastNameFocus = true">
                        <span :class="['tooltiptext', { active: lastName }, { show: lastNameFocus }]">
                            <div class="item" v-for="message in lastNameMessage">{{ message }}</div>
                        </span>
                    </div>
                </div>
            </template>
            <div class="field">
                <div class="label">Логин</div>
                <div class="input-container">
                    <input type="text" :class="[{ wrong: loginMessage.length !== 0 }]" v-model="login"
                        @blur="loginFocus = false" @focus="loginFocus = true">
                    <span :class="['tooltiptext', { active: login }, { show: loginFocus }]">
                        <div class="item" v-for="message in loginMessage">{{ message }}</div>
                    </span>
                </div>
            </div>
            <div class="field">
                <div class="label">Пароль</div>
                <div class="input-container">
                    <input type="password" :class="[{ wrong: passwordMessage.length !== 0 }]" v-model="password"
                        @blur="passwordFocus = false" @focus="passwordFocus = true">
                    <span :class="['tooltiptext', { active: password }, { show: passwordFocus }]">
                        <div class="item" v-for="message in passwordMessage">{{ message }}</div>
                    </span>
                </div>
            </div>
        </div>
        <div :class="['button', { active: isButtonActive }]" @click="buttonHandler">
            <span v-if="loginActive">Войти</span>
            <span v-else>Зарегистрироваться</span>
        </div>
    </FormContainer>
</template>
<script>
import { storeToRefs } from 'pinia';
import { useAuthStore } from '../stores/auth';
import FormContainer from '../components/FormContainer.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faTriangleExclamation } from '@fortawesome/free-solid-svg-icons';
import { library } from '@fortawesome/fontawesome-svg-core';
library.add(faTriangleExclamation);

export default {
    setup() {
        const { logined, loading, message } = storeToRefs(useAuthStore());
        const { loginRequest, registerRequest, clearMessage } = useAuthStore();
        const {
            VITE_MAX_FIRSTNAME_LENGTH,
            VITE_MIN_PASSWORD_LENGTH,
            VITE_MAX_LASTNAME_LENGTH,
            VITE_MIN_LOGIN_LENGTH,
            VITE_MAX_LOGIN_LENGTH
        } = import.meta.env;
        return {
            loginRequest,
            registerRequest,
            logined,
            loading,
            message,
            clearMessage,
            VITE_MAX_FIRSTNAME_LENGTH,
            VITE_MIN_PASSWORD_LENGTH,
            VITE_MAX_LASTNAME_LENGTH,
            VITE_MAX_LOGIN_LENGTH,
            VITE_MIN_LOGIN_LENGTH
        }
    },
    components: { FormContainer, FontAwesomeIcon },
    mounted() {
        if (this.logined === true) {
            this.$router.push({ path: '/lk' })
        }
    },
    data() {
        return {
            loginActive: true,

            login: '',
            loginMessage: [],
            loginFocus: false,

            password: '',
            passwordMessage: [],
            passwordFocus: false,

            name: '',
            nameMessage: [],
            nameFocus: false,

            lastName: '',
            lastNameMessage: [],
            lastNameFocus: false,
        }
    },
    methods: {
        buttonHandler() {
            if (!this.isButtonActive) return;
            if (this.loginActive) {
                this.loginRequest(this.login, this.password)
            } else {
                this.registerRequest(this.login, this.password, this.name, this.lastName)
            }
        },
    },
    watch: {
        login() {
            this.clearMessage();
        },
        password() {
            this.clearMessage();
        },
        name() {
            this.clearMessage();
        },
        lastName() {
            this.clearMessage();
        },
        logined(value) {
            if (value === true) {
                this.$router.push({ path: '/lk' })
            }
        }
    },
    computed: {
        loginIsValid() {
            if (!this.login) return
            if (this.loginActive) {
                this.loginMessage = [];
                return true
            }
            var messages = [];
            let value = this.login;
            if (/[\s]/.test(value)) {
                messages.push('В логине зарещены пробельные символы');
            }
            if (value.length < this.VITE_MIN_LOGIN_LENGTH) {
                messages.push(`Логин должен быть более ${this.VITE_MIN_LOGIN_LENGTH} символов`);
            }
            if (value.length >= this.VITE_MAX_LOGIN_LENGTH) {
                messages.push(`Логин должен быть не более ${this.VITE_MAX_LOGIN_LENGTH} символов`);
            }
            this.loginMessage = messages;
            return messages.length === 0
        },
        passwordIsValid() {
            if (!this.password) return
            if (this.loginActive) {
                this.passwordMessage = '';
                return true
            }
            var messages = [];
            let value = this.password;
            var messageBase = 'Пароль должен содержать ';
            if (!/[A-Z]/.test(value)) {
                messages.push(messageBase + 'ПРОПИСНЫЕ английские буквы');
            }
            if (!/[a-z]/.test(value)) {
                messages.push(messageBase + 'строчные английские буквы');
            }
            if (!/[0-9]/.test(value)) {
                messages.push(messageBase + 'цифры');
            }
            if (!/[#?!@$%^&*-]/.test(value)) {
                messages.push(messageBase + 'специальные символы (#?!@$%^&*-)');
            }
            if (this.password.length < this.VITE_MIN_PASSWORD_LENGTH) {
                messages.push(`Пароль должен иметь длину от ${this.VITE_MIN_PASSWORD_LENGTH} символов`);
            }
            this.passwordMessage = messages;
            return messages.length === 0
        },
        nameIsValid() {
            if (!this.name) return
            let value = this.name;
            var messages = [];
            if (/[\s]/.test(value)) {
                messages.push('В имени зарещены пробельные символы');
            }
            if (value.length > this.VITE_MAX_FIRSTNAME_LENGTH) {
                messages.push(`Имя должено быть менее ${this.VITE_MAX_FIRSTNAME_LENGTH} символов`);
            }
            this.nameMessage = messages;
            return messages.length === 0
        },
        lastNameIsValid() {
            if (!this.lastName) return
            let value = this.lastName;
            var messages = [];
            if (/[\s]/.test(value)) {
                messages.push('В фамилии зарещены пробельные символы');
            }
            if (value.length > this.VITE_MAX_LASTNAME_LENGTH) {
                messages.push(`Фамилия должена быть менее ${this.VITE_MAX_LASTNAME_LENGTH} символов`);
            }
            this.lastNameMessage = messages;
            return messages.length === 0
        },
        isButtonActive() {
            return (this.loginIsValid & this.passwordIsValid) & (this.loginActive ? true : this.nameIsValid & this.lastNameIsValid)
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/themes';
@use '@/assets/styles/breakpoints';

#app:has(.login-form) {
    height: 100%;
}

.login-form {
    position: relative;

    .message,
    .selector,
    .fields-area,
    .button {
        background-color: var(--color-background-mute-2);
        padding: 5px;
        border-radius: 20px;
        user-select: none;
    }

    .message {
        position: absolute;
        width: 100%;
        left: 0;
        bottom: calc(100% + 10px);
        background-color: var(--red-0-hover);
        @include helpers.flex-center;
        padding: 10px;
        flex-wrap: wrap;

        .text {
            text-align: center;
            font-size: 0.95em;
        }
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
                    display: flex;
                    flex-direction: column;
                    gap: 5px;

                    .item {
                        border-radius: 3px;
                    }

                    &.show.active:not(:empty) {
                        visibility: visible;
                    }

                    @include breakpoints.md {
                        bottom: 0;
                        left: calc(100% + 5px);
                    }

                    @include breakpoints.md(true) {
                        bottom: 110%;
                        left: 50%;
                        margin-left: -100px;
                    }

                    // &::after {
                    //     content: " ";
                    //     position: absolute;
                    //     top: 50%;
                    //     right: 100%;

                    //     @include breakpoints.md(true) {
                    //         top: 100%;
                    //         left: 50%;
                    //     }

                    //     margin-top: -5px;
                    //     border-width: 5px;
                    //     border-style: solid;
                    //     border-color: transparent black transparent transparent;
                    // }
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
}
</style>