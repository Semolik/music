<template>
    <FormContainer
        :headline="register ? 'Зарегистрироваться' : 'Войти в свой аккаунт'"
        ref="formContainer"
    >
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
            placeholder="Никнейм"
            :show-word-limit="showLoginLimit"
            :maxLength="MAX_LOGIN_LENGTH"
            :minLength="MIN_LOGIN_LENGTH"
            :formatter="validateLogin"
            :error="loginError || usernameAlreadyExists"
        />
        <AppInput
            v-model="password"
            placeholder="Пароль"
            type="password"
            :maxLength="MAX_PASSWORD_LENGTH"
            :minLength="MIN_PASSWORD_LENGTH"
            :error="passwordError"
        />
        <LoginFormPasswordStrength :password="password" v-if="register" />

        <nuxt-link
            v-if="!register"
            class="bottom-text forgot-password"
            :to="routesNames.resetPassword"
        >
            Забыли пароль?
        </nuxt-link>
        <div class="login-button" @click="loginHandler">
            {{ register ? "Зарегистрироваться" : "Войти" }}
        </div>

        <template #bottom>
            <nuxt-link
                class="bottom-text"
                :to="register ? '/login' : '/sign-in'"
            >
                {{ register ? "Уже есть аккаунт?" : "Нет аккаунта?" }}
            </nuxt-link>
        </template>
    </FormContainer>
</template>
<script setup>
import { useAuthStore } from "~~/stores/auth";
import { HandleOpenApiError } from "~~/composables/errors";
import { routesNames } from "@typed-router";
import { Service } from "~~/client";
import FormContainer from "~/components/form-container.vue";
const authStore = useAuthStore();
const runtimeConfig = useRuntimeConfig();
const { register } = defineProps({
    register: {
        type: Boolean,
        default: false,
    },
});
const formContainer = ref(null);
const { $toast } = useNuxtApp();
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
const loginError = ref(false);
const passwordError = ref(false);
const usernameAlreadyExists = ref(false);
watch(login, async (newUsername) => {
    if (!register || !newUsername) {
        usernameAlreadyExists.value = false;
        return;
    }

    usernameAlreadyExists.value =
        await Service.checkUsernameExistsApiV1UsersUsernameExistsGet(
            newUsername
        );
    if (usernameAlreadyExists.value) {
        formContainer.value?.showMessage(
            "Пользователь с таким именем уже существует"
        );
    } else {
        formContainer.value?.hideMessage();
    }
});

const loginHandler = async () => {
    if (login.value.length < MIN_LOGIN_LENGTH) {
        loginError.value = true;
        formContainer.value?.showMessage(
            `Логин должен быть не менее ${MIN_LOGIN_LENGTH} символов`
        );
        return;
    } else {
        loginError.value = false;
    }
    if (password.value.length < MIN_PASSWORD_LENGTH) {
        passwordError.value = true;
        formContainer.value?.showMessage(
            `Пароль должен быть не менее ${MIN_PASSWORD_LENGTH} символов`
        );
        return;
    } else {
        passwordError.value = false;
    }
    if (usernameAlreadyExists.value) {
        formContainer.value?.showMessage(
            "Пользователь с таким именем уже существует"
        );
        return;
    }
    if (password.value.length > MAX_PASSWORD_LENGTH) {
        passwordError.value = true;
        formContainer.value?.showMessage(
            `Пароль должен быть не более ${MAX_PASSWORD_LENGTH} символов`
        );
        return;
    } else {
        passwordError.value = false;
    }
    if (login.value.length > MAX_LOGIN_LENGTH) {
        loginError.value = true;
        formContainer.value?.showMessage(
            `Логин должен быть не более ${MAX_LOGIN_LENGTH} символов`
        );
        return;
    } else {
        loginError.value = false;
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
        $toast.error(HandleOpenApiError(error).message);
        return;
    }
    const router = useRouter();
    router.push({
        name: register ? routesNames.setupGenres : routesNames.settings.profile,
    });
};
const validateLogin = (value) => {
    const { login, error } = useLoginValidation(value);
    if (error) {
        formContainer.value?.showMessage(error);
    }
    return login;
};
</script>
<style scoped lang="scss">
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

.bottom-text {
    font-size: 14px;
    color: $secondary-text;
    cursor: pointer;
    &:hover {
        color: $primary-text;
    }

    &.forgot-password {
        line-height: 1;
    }
}
</style>
