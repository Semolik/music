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
            name: ''
        }
    },
    computed: {
        loginIsValid() {
            if (!this.login) return
            if (this.login.length < 5) {
                this.loginMessage = 'Логин должен быть более 5 символов';
                return
            }
            this.loginMessage = '';
            return true
        },
        isButtonActive() {
            return this.loginIsValid
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';

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

        &:not(.active):hover {
            background-color: var(--color-background-mute-3);
        }

        &.active {
            cursor: auto;
            background-color: var(--color-background-mute-4);
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

        @keyframes shake {

            10%,
            90% {
                transform: translate3d(-1px, 0, 0);
            }

            20%,
            80% {
                transform: translate3d(2px, 0, 0);
            }

            30%,
            50%,
            70% {
                transform: translate3d(-4px, 0, 0);
            }

            40%,
            60% {
                transform: translate3d(4px, 0, 0);
            }
        }

        .apply-shake {
            animation: shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
        }

        .input-container {
            position: relative;
            display: inline-block;

            input {
                background-color: var(--color-background-mute-4);
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