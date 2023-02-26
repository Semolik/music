<template>
    <div class="login-form-container">
        <div class="login-form">
            <div class="headline">
                {{ register ? "Зарегистрироваться" : "Войти в свой аккаунт" }}
            </div>
            <AppInput
                v-model="login"
                placeholder="Юзернейм"
                :show-word-limit="register"
                :maxlength="MAX_LOGIN_LENGTH"
                :formatter="(value) => value.replace(/[^a-zA-Z0-9_]/g, '')"
            />
            <AppInput v-model="password" placeholder="Пароль" type="password" />
            <div class="login-button" @click="loginHandler">
                {{ register ? "Зарегистрироваться" : "Войти" }}
            </div>
        </div>
        <nuxt-link class="bottom-text" :to="register ? '/login' : '/sign-in'">
            {{ register ? "Уже есть аккаунт?" : "Нет аккаунта?" }}
        </nuxt-link>
    </div>
</template>
<script setup>
import { useToast } from "vue-toastification";
import { useAuthStore } from "~~/stores/auth";
import { HandleAxiosError } from "~~/composables/errors";
const authStore = useAuthStore();
const runtimeConfig = useRuntimeConfig();
const { register } = defineProps({
    register: {
        type: Boolean,
        default: false,
    },
});
const login = ref("");
const password = ref("");
const toast = useToast();
const { MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH, MAX_LOGIN_LENGTH } =
    runtimeConfig.public;

const loginHandler = async () => {
    if (password.value.length < MIN_PASSWORD_LENGTH) {
        toast.error(
            `Пароль должен быть не менее ${MIN_PASSWORD_LENGTH} символов`
        );
        return;
    }
    try {
        await authStore.loginRequest(login.value, password.value);
    } catch (e) {
        console.log(e);
        toast.error(HandleAxiosError(e));
    }
};
</script>
<style scoped lang="scss">
.login-form-container {
    @include flex-center;
    flex-direction: column;

    height: 100%;

    .login-form {
        color: $primary-text;
        width: 100%;
        max-width: 400px;
        padding: 20px;
        background-color: $primary-bg;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        .headline {
            font-size: 20px;
            font-weight: 500;
            text-align: center;
            color: $secondary-text;
        }

        .login-button {
            @include flex-center;
            height: 40px;
            background-color: $tertiary-bg;
            border-radius: 5px;
            color: $primary-text;
            font-weight: 500;
            cursor: pointer;

            &:hover {
                background-color: $quaternary-bg;
            }
        }
    }
    .bottom-text {
        font-size: 14px;
        color: $secondary-text;
        cursor: pointer;
        &:hover {
            color: $primary-text;
        }
    }
}
</style>
