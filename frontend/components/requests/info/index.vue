<template>
    <div class="request-page">
        <div class="user">
            <RequestsItemContent :request="request" :show-status="showStatus" />
        </div>
        <div class="message">
            {{ request.message }}
        </div>
        <slot />
    </div>
</template>
<script setup>
defineProps({
    request: {
        type: Object,
        required: true,
    },
    showStatus: {
        type: Boolean,
        default: false,
    },
});
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
}
</style>
