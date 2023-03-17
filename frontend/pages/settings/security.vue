<template>
    <div class="security-container">
        <div class="security-container-title">Изменить пароль</div>
        <div class="security-container-fields">
            <AppInput
                v-model="oldPassword"
                label="Старый пароль"
                type="password"
                :max-length="MAX_PASSWORD_LENGTH"
                :min-length="MIN_PASSWORD_LENGTH"
                show-word-limit
            />
            <AppInput
                v-model="newPassword"
                label="Новый пароль"
                type="password"
                :max-length="MAX_PASSWORD_LENGTH"
                :min-length="MIN_PASSWORD_LENGTH"
                show-word-limit
            />
            <LoginFormPasswordStrength :password="newPassword" />
            <AppButton
                @click="changePassword"
                :active="buttonIsActive"
                class="change-password-button"
            >
                Изменить пароль
            </AppButton>
        </div>
    </div>
</template>
<script setup>
import { Service } from "@/client";
import { useToast } from "vue-toastification";
definePageMeta({
    middleware: ["auth"],
});
const toast = useToast();
const runtimeConfig = useRuntimeConfig();
const { MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH } = runtimeConfig.public;

const oldPassword = ref("");
const newPassword = ref("");

const buttonIsActive = computed(() => {
    return (
        oldPassword.value.length >= MIN_PASSWORD_LENGTH &&
        newPassword.value.length >= MIN_PASSWORD_LENGTH
    );
});
const changePassword = async () => {
    if (!buttonIsActive.value) return;
    try {
        await Service.changePasswordApiV1AuthChangePasswordPut({
            password: oldPassword.value,
            new_password: newPassword.value,
        });
        toast.success("Пароль успешно изменен");
    } catch (e) {
        toast.error(HandleOpenApiError(e).message);
    } finally {
        oldPassword.value = "";
        newPassword.value = "";
    }
};
</script>
<style lang="scss" scoped>
.security-container {
    @include flex-center;
    flex-direction: column;
    @include sm {
        padding: 2rem;
    }

    .security-container-title {
        font-size: 20px;
        font-weight: 500;
        margin-bottom: 20px;
        color: $secondary-text;
    }
    .security-container-fields {
        max-width: 400px;
        display: flex;
        flex-direction: column;
        width: 100%;
        gap: 10px;

        .change-password-button {
            margin-top: 10px;
        }
    }
}
</style>
