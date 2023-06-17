<template>
    <template v-if="!request">
        <AppInput
            v-model="login"
            placeholder="Никнейм"
            :formatter="validateLogin"
            :error="usernameDoesNotExist"
        />
        <AppInput
            v-model="mail"
            placeholder="Почта для связи"
            :error="emailError"
            :max-length="MAX_EMAIL_LENGTH"
        />
        <AppInput
            v-model="message"
            placeholder="Напишите сообщение для администрации"
            type="textarea"
            rows="7"
            resize="none"
            :max-length="MAX_SUPPORT_MESSAGE_LENGTH"
        />
        <AppButton :active="buttonIsActive" @click="send">
            Отправить
        </AppButton>
    </template>
    <template v-else>
        <div class="info-blocks" id="request-info">
            <div :class="['status', request.status]">
                {{ status_message }}
            </div>
            <div
                class="mail-message"
                v-if="request.status === SupportMessageStatus.RESOLVED"
            >
                Проверьте почту
            </div>
            <div class="info-block">
                <div class="title">Указанный никнейм</div>
                <div class="value">
                    {{ request.login }}
                </div>
            </div>
            <div class="info-block">
                <div class="title">Указанная почта</div>
                <div class="value">
                    {{ request.email }}
                </div>
            </div>
            <div class="info-block column">
                <div class="title">Сообщение</div>
                <div class="value message">
                    {{ request.message }}
                </div>
            </div>
        </div>
        <AppButton
            @click="
                () => {
                    requestId = null;
                    request = null;
                }
            "
            active
        >
            Написать еще раз
        </AppButton>
    </template>
</template>
<script setup>
import { Service } from "~/client";
import { SupportMessageType } from "~/client/models/SupportMessageType";
import { SupportMessageStatus } from "~/client/models/SupportMessageStatus";
const { $toast: toast } = useNuxtApp();
const { requestId } = defineProps({
    requestId: {
        type: String,
        default: null,
    },
    formContainer: {
        type: Object,
        default: null,
    },
});
const emit = defineEmits(["update:requestId"]);
const request = ref(null);
if (requestId) {
    try {
        request.value =
            await Service.getSupportMessageApiV1SupportMessagesMessageIdGet(
                requestId
            );
    } catch (e) {
        emit("update:requestId", null);
    }
}
const status_message = computed(() => {
    if (!request.value) {
        return null;
    }
    switch (request.value.status) {
        case SupportMessageStatus.PENDING:
            return "Ваше сообщение находится в обработке";
        case SupportMessageStatus.RESOLVED:
            return "Ваше сообщение было рассмотрено";
        case SupportMessageStatus.REJECTED:
            return "Ваше сообщение было отклонено";
    }
});

const { MAX_EMAIL_LENGTH, MAX_SUPPORT_MESSAGE_LENGTH } =
    useRuntimeConfig().public;
const validateLogin = (value) => {
    const { login, error } = useLoginValidation(value);
    if (error) {
        formContainer.value?.showMessage(error);
    }
    return login;
};
const mail = ref("");
const emailError = computed(() => {
    if (!mail.value) {
        return false;
    }
    const { error } = useEmailValidation(mail.value);
    return !error;
});

const message = ref("");
const login = ref("");
const usernameDoesNotExist = ref(false);
watch(login, async (value) => {
    usernameDoesNotExist.value =
        !(await Service.checkUsernameExistsApiV1UsersUsernameExistsGet(value));
});
const buttonIsActive = computed(() => {
    return (
        !usernameDoesNotExist.value &&
        login.value.length > 0 &&
        message.value.length > 0 &&
        message.value.length <= MAX_SUPPORT_MESSAGE_LENGTH &&
        mail.value.length > 0 &&
        !emailError.value
    );
});

const send = async () => {
    if (!buttonIsActive.value) {
        return;
    }
    try {
        request.value =
            await Service.createSupportMessageApiV1SupportMessagesPost({
                login: login.value,
                email: mail.value,
                message: message.value,
                type: SupportMessageType.PASSWORD_RECOVERY,
            });
        emit("update:requestId", request.value.id);
        toast.success("Письмо отправлено");
    } catch (e) {
        toast.error(HandleOpenApiError(e).message);
    }
};
</script>
<style lang="scss">
#request-info {
    display: flex;
    flex-direction: column;
    gap: 10px;
    .status {
        background-color: $accent-2;
        color: $primary-bg;
        padding: 10px;
        border-radius: 10px;
        text-align: center;

        &.resolved {
            background-color: $accent;
        }
    }
    .mail-message {
        color: $secondary-text;
        text-align: center;
    }
    .info-block {
        display: grid;
        grid-template-columns: 1fr 1fr;
        border-radius: 10px;
        overflow: hidden;
        &.column {
            grid-template-columns: 1fr;
        }
        .title,
        .value {
            background-color: $tertiary-bg;
            padding: 10px;
            text-align: center;

            &:not(.message) {
                @include flex-center;
            }
        }
        .value {
            background-color: $quaternary-bg;
            overflow-wrap: anywhere;

            &.message {
                text-align: left;
            }
        }
    }
}
</style>
