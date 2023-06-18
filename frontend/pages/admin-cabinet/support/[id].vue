<template>
    <SettingsPage :title="title" max-width="100%">
        <InfoItems :items="items" />
        <AppSelect :values="statuses" v-model="status" class="select" />
        <AppButton @click="updateStatus" :active="buttonActive">
            Сохранить
        </AppButton>
    </SettingsPage>
</template>
<script setup>
import { Service } from "~/client";
const { id } = useRoute().params;
import { SupportMessageType, SupportMessageStatus } from "~/client";
const getStatusName = (status) => {
    switch (status) {
        case SupportMessageStatus.REJECTED:
            return "Отклонен";
        case SupportMessageStatus.PENDING:
            return "В ожидании";
        case SupportMessageStatus.RESOLVED:
            return "Решен";
    }
};

const support_request = ref(
    await Service.getSupportMessageApiV1SupportMessagesMessageIdGet(id)
);
var statuses_full = Object.values(SupportMessageStatus).map((status) => ({
    title: getStatusName(status),
    value: status,
}));
const statuses = statuses_full.map((status) => status.title);
const status = ref(getStatusName(support_request.value.status));
const { $toast } = useNuxtApp();
const items = computed(() => [
    {
        title: "Тип сообщения",
        value:
            support_request.value.type == SupportMessageType.SUPPORT
                ? "Техническая поддержка"
                : "Запрос на восстановление пароля",
    },
    {
        title: "Текст сообщения",
        value: support_request.value.message,
        vertical: true,
        left: true,
    },
    {
        title: "Указанная почта",
        value: support_request.value.email,
    },
    {
        title: "Статус",
        value: getStatusName(support_request.value.status),
    },
    {
        title: "Дата создания",
        value: support_request.value.created_at,
    },
]);
const title = computed(() => {
    switch (support_request.value.type) {
        case SupportMessageType.PASSWORD_RECOVERY:
            return "Запрос на восстановление пароля";
        case SupportMessageType.SUPPORT:
            return "Техническая поддержка";
    }
});
const buttonActive = computed(() => {
    return status.value != getStatusName(support_request.value.status);
});
const updateStatus = async () => {
    if (!buttonActive.value) return;
    const newStatus = statuses_full.find((find_status) => {
        return find_status.title === status.value;
    }).value;
    try {
        support_request.value =
            await Service.updateSupportMessageApiV1SupportMessagesMessageIdPut(
                id,
                newStatus
            );
    } catch (e) {
        $toast.error(HandleOpenApiError(e).message);
    }
};
</script>
<style lang="scss" scoped>
.select {
    --app-select-bg: #{$secondary-bg};
}
</style>
