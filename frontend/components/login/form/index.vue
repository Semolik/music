<template>
    <div class="login-form-container">
        <div class="login-form">
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
            <AppInput
                v-model="login"
                placeholder="Юзернейм"
                :show-word-limit="showLoginLimit"
                :maxLength="MAX_LOGIN_LENGTH"
                :minLength="MIN_LOGIN_LENGTH"
                :formatter="validateLogin"
            />
            <AppInput
                v-model="password"
                placeholder="Пароль"
                type="password"
                :show-word-limit="showPasswordLimit"
                :maxLength="MAX_PASSWORD_LENGTH"
                :minLength="MIN_PASSWORD_LENGTH"
            />
            <LoginFormPasswordStrength :password="password" />

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
const {
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
    MAX_LOGIN_LENGTH,
    MIN_LOGIN_LENGTH,
} = runtimeConfig.public;
const showPasswordLimit = computed(
    () => password.value.length === MAX_PASSWORD_LENGTH
);
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

    const error = register
        ? await authStore.registerRequest(login.value, password.value)
        : await authStore.loginRequest(login.value, password.value);
    if (error) {
        showMessage(HandleAxiosError(error).message, true);
        return;
    }
    const router = useRouter();
    router.push({ name: "profile" });
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
        position: relative;
        .message {
            position: absolute;
            bottom: 100%;
            left: 0;
            width: 100%;
            font-size: 14px;
            text-align: center;
            color: transparent;

            &.active {
                color: $secondary-text;
                &.error {
                    color: $accent-red;
                }
            }
        }
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
            user-select: none;

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
