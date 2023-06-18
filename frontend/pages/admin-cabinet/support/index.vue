<template>
    <div class="support-messages-page">
        <FiltersPanel :items="types" v-model:active="type" />
        <ItemsPaginate
            is-tracks
            :onNextPage="onNextPage"
            :page-size="SUPPORT_MESSAGES_PAGE_SIZE"
            ref="itemsPaginate"
        >
            <template v-slot="{ items }">
                <div class="support-messages-list">
                    <SupportItem v-for="message in items" :item="message" />
                </div>
            </template>
        </ItemsPaginate>
    </div>
</template>
<script setup>
import { SupportMessageType } from "~/client/models/SupportMessageType";
import { Service } from "~/client";

const { SUPPORT_MESSAGES_PAGE_SIZE } = useRuntimeConfig().public;
const itemsPaginate = ref(null);
const types = {
    all: "Все",
    [SupportMessageType.PASSWORD_RECOVERY]: "Восстановление пароля",
    [SupportMessageType.SUPPORT]: "Техническая поддержка",
};
const type = ref(SupportMessageType.PASSWORD_RECOVERY);
watch(type, () => {
    itemsPaginate.value.resetPage();
});
const onNextPage = async (page) => {
    const data = await Service.getSupportMessagesApiV1SupportMessagesGet(
        type.value === "all" ? null : type.value,
        page
    );
    return data;
};
</script>
<style lang="scss" scoped>
.support-messages-page {
    display: flex;
    flex-direction: column;
    gap: 5px;

    .support-messages-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 5px;
    }
}
</style>
