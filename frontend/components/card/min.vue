<template>
    <div class="card-min">
        <CardPicture
            :picture="picture"
            :icon="icon"
            :borderRadius="borderRadius"
            min
        />
        <div class="card-min-content">
            <slot name="content" />
        </div>
        <slot name="card-end" />
    </div>
</template>
<script setup>
const { text, picture, icon, borderRadius } = defineProps({
    text: {
        type: String,
        required: true,
    },
    picture: {
        type: [String, null],
        required: true,
    },
    icon: {
        type: String,
        required: true,
    },
    borderRadius: {
        type: Number,
        required: false,
        default: 5,
    },
});
</script>
<style lang="scss">
.card-min {
    padding: 7px;
    display: flex;
    min-height: 70px;
    max-height: 70px;
    gap: 10px;
    background-color: $quaternary-bg;
    border-radius: 10px;
    &:hover {
        background-color: $quinary-bg;
        cursor: pointer;
    }
    .card-min-content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        flex-grow: 1;
    }
}
</style>
