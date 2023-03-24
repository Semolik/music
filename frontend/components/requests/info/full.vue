<template>
    <RequestsInfo :request="request" show-status>
        <div v-if="request.answer" class="answer">
            <div>Ответ администратора</div>
            <div class="answer-text">
                {{ request.answer?.message }}
            </div>
        </div>
    </RequestsInfo>
</template>
<script setup>
const { request } = defineProps({
    request: {
        type: Object,
        required: true,
    },
});
</script>
<style lang="scss" scoped>
.answer {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
    border-radius: 5px;
    background-color: $quinary-bg;

    .answer-text {
        padding: 10px;
        background-color: $quaternary-bg;
        border-radius: 5px;
    }
}
</style>
