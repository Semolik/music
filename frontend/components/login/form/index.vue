<template>
    <div class="login-form-container">
        <div class="login-form shadow-2xl">
            <div
                :class="[
                    'message',
                    { active: messageIsShowed },
                    { error: isErrorMessage },
                ]"
            >
                {{ message }}
            </div>
            <div class="headline">
                {{ register ? "Зарегистрироваться" : "Войти в свой аккаунт" }}
            </div>
            <template v-if="register">
                <AppInput
                    placeholder="Имя"
                    show-word-limit
                    :maxLength="MAX_FIRSTNAME_LENGTH"
                    v-model="firstName"
                />
                <AppInput
                    placeholder="Фамилия"
                    show-word-limit
                    :maxLength="MAX_LASTNAME_LENGTH"
                    v-model="lastName"
                />
            </template>
            <AppInput
                v-model="login"
                placeholder="Имя пользователя"
                :show-word-limit="showLoginLimit"
                :maxLength="MAX_LOGIN_LENGTH"
                :minLength="MIN_LOGIN_LENGTH"
                :formatter="validateLogin"
            />
            <AppInput
                v-model="password"
                placeholder="Пароль"
                type="password"
                :maxLength="MAX_PASSWORD_LENGTH"
                :minLength="MIN_PASSWORD_LENGTH"
            />
            <LoginFormPasswordStrength :password="password" v-if="register" />
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
import { useAuthStore } from "~~/stores/auth";
import { HandleOpenApiError } from "~~/composables/errors";
import { useToast } from "vue-toastification";
import { routesNames } from "@typed-router";
const authStore = useAuthStore();
const runtimeConfig = useRuntimeConfig();
const { register } = defineProps({
    register: {
        type: Boolean,
        default: false,
    },
});
const toast = useToast();
const login = ref("");
const password = ref("");
const firstName = ref("");
const lastName = ref("");
const {
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
    MAX_LOGIN_LENGTH,
    MIN_LOGIN_LENGTH,
    MAX_FIRSTNAME_LENGTH,
    MAX_LASTNAME_LENGTH,
} = runtimeConfig.public;

const showLoginLimit = computed(
    () => register || login.value.length === MAX_LOGIN_LENGTH
);
const message = ref("");
const messageIsShowed = ref(false);
const messageTimer = ref(null);
const messageNestedTimer = ref(null);
const isErrorMessage = ref(false);
const showMessage = (messageText, isError) => {
    if (messageTimer.value) {
        clearTimeout(messageTimer.value);
        if (messageNestedTimer.value) {
            clearTimeout(messageNestedTimer.value);
        }
    }
    isErrorMessage.value = isError;
    message.value = messageText;
    messageIsShowed.value = true;
    messageTimer.value = setTimeout(() => {
        messageIsShowed.value = false;
        messageNestedTimer.value = setTimeout(() => {
            message.value = "";
        }, 500);
    }, 3000 * (isError ? 2 : 1));
};

const loginHandler = async () => {
    if (login.value.length < MIN_LOGIN_LENGTH) {
        showMessage(`Логин должен быть не менее ${MIN_LOGIN_LENGTH} символов`);
        return;
    }
    if (password.value.length < MIN_PASSWORD_LENGTH) {
        showMessage(
            `Пароль должен быть не менее ${MIN_PASSWORD_LENGTH} символов`
        );
        return;
    }
    if (password.value.length > MAX_PASSWORD_LENGTH) {
        showMessage(
            `Пароль должен быть не более ${MAX_PASSWORD_LENGTH} символов`
        );
        return;
    }
    if (login.value.length > MAX_LOGIN_LENGTH) {
        showMessage(`Логин должен быть не более ${MAX_LOGIN_LENGTH} символов`);
        return;
    }
    const error = register
        ? await authStore.registerRequest(
              login.value,
              password.value,
              firstName.value,
              lastName.value
          )
        : await authStore.loginRequest(login.value, password.value);
    if (error) {
        toast.error(HandleOpenApiError(error).message);
        return;
    }
    const router = useRouter();
    router.push({
        name: register ? routesNames.setupGenres : routesNames.settings.profile,
    });
};
const validateLogin = (value) => {
    const regex = /[^a-zA-Z0-9_]/g;
    if (regex.test(value)) {
        showMessage(
            "Логин может содержать только латинские буквы, цифры и нижнее подчеркивание"
        );
    }
    return value.replace(regex, "");
};
</script>
<style scoped lang="scss">
.login-form-container {
    @include flex-center;
    flex-direction: column;
    gap: 20px;
    height: 100%;
    padding-top: 20vh;

    .login-form {
        color: $primary-text;
        width: 100%;
        max-width: 400px;
        padding: 30px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        position: relative;
        background-color: $primary-bg-2;
        border-radius: 10px;
        --app-input-border-radius: 5px;
        @include md(true) {
            padding: 20px;
        }
        .message {
            position: absolute;
            bottom: 110%;
            left: 0;
            width: 100%;
            font-size: 14px;
            text-align: center;
            color: transparent;

            &.active {
                color: $secondary-text;
                &.error {
                    color: $accent-error;
                }
            }
        }
        .headline {
            font-size: 20px;
            font-weight: 500;
            text-align: center;
            color: $secondary-text;
            margin-bottom: 10px;
        }

        .login-button {
            @include flex-center;
            height: 40px;

            border-radius: 5px;

            font-weight: 500;
            cursor: pointer;
            user-select: none;
            background-color: $tertiary-bg;
            &:hover {
                background-color: $quaternary-bg;
            }
            color: $secondary-text;
            cursor: pointer;
            &:hover {
                color: $primary-text;
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
