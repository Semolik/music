<template>
    <div class="request-page">
        <div class="user">
            <RequestsItemContent :request="request" :show-status="false" />
        </div>
        <div class="message">
            {{ request.message }}
        </div>
        <AppInput
            v-model="message"
            class="message-input"
            placeholder="Введите сообщение"
            type="textarea"
            resize="none"
            :rows="6"
        />
        <div class="statuses">
            <div
                :class="['status', { active: request_status === key }, key]"
                v-for="(status, key) in statusesNames"
                :key="key"
                @click="request_status = key"
            >
                {{ status }}
            </div>
        </div>
        <AppButton
            @click="sendAnswer"
            :active="buttonActive"
            class="send"
            border-radius="5px"
        >
            {{ request.answer ? "Изменить" : "Отправить" }}
        </AppButton>
    </div>
</template>
<script setup>
import { Service, ChangeRoleRequestStatus } from "@/client";
definePageMeta({
    middleware: ["admin"],
});
const route = useRoute();
const { id } = route.params;
const request = ref(
    await Service.getChangeRoleRequestApiV1RolesChangeRequestIdGet(id)
);
const statusesNames = {
    [ChangeRoleRequestStatus.ACCEPTED]: "Принято",
    [ChangeRoleRequestStatus.REJECTED]: "Отклонено",
};
const message = ref(request.value.answer?.message || "");
const request_status = ref(
    request.value.request_status !== ChangeRoleRequestStatus.IN_PROGRESS
        ? request.value.request_status
        : null
);
const buttonActive = computed(() => {
    return (
        message.value.length > 0 &&
        (request.value.answer
            ? request_status.value !== request.value.request_status ||
              request.value.answer.message !== message.value
            : request_status.value)
    );
});

const sendAnswer = async () => {
    if (!buttonActive.value) return;
    request.value.answer =
        await Service.sendUpdateRoleRequestAnswerApiV1RolesChangeRequestIdAnswerPost(
            id,
            {
                message: message.value,
                request_status: request_status.value,
            }
        );
    request.value.request_status = request_status.value;
};
</script>
<style lang="scss" scoped>
.request-page {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
    border-radius: 10px;
    background-color: $quaternary-bg;

    .user {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .message {
        padding: 10px;
        background-color: $quinary-bg;
        border-radius: 5px;
    }
    .message-input {
        --app-input-bg: #{$tertiary-bg};
        --app-input-border-radius: 5px;
    }

    .statuses {
        display: flex;
        gap: 10px;

        .status {
            @include flex-center;
            cursor: pointer;
            padding: 10px;
            height: min-content;
            border-radius: 5px;
            width: 100%;
            cursor: pointer;
            user-select: none;
            background-color: $quinary-bg;
            border: 1px solid transparent;
            &:hover {
                &.rejected {
                    border-color: $accent-error;
                }

                &.accepted {
                    border-color: $accent-success;
                }
            }

            &.active {
                color: $primary-bg;
                color: black;
                cursor: pointer;

                &.rejected {
                    background-color: $accent-error;
                }

                &.accepted {
                    background-color: $accent-success;
                }
            }
        }
    }
    .send {
        --app-button-bg: #{$quinary-bg};
    }
}
</style>
