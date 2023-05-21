<template>
    <div class="card-min">
        <CardPicture
            :picture="picture"
            :icon="icon"
            :borderRadius="borderRadius"
            min
            @click="emit('picture-click', $event)"
        >
            <slot name="card-picture" />
        </CardPicture>
        <div class="card-min-content">
            <slot name="content" />
        </div>
        <slot name="card-end" />
    </div>
</template>
<script setup>
const emit = defineEmits(["picture-click"]);
const { text, picture, icon, borderRadius } = defineProps({
    picture: {
        type: [String, null],
        required: true,
    },
    icon: {
        type: String,
        required: true,
    },
    borderRadius: {
        type: String,
        required: false,
        default: "5px",
    },
});
</script>
<style lang="scss">
.card-min {
    padding: 7px;
    display: grid;
    grid-template-columns: min-content 1fr min-content;
    min-height: 70px;
    max-height: 70px;
    gap: 10px;
    background-color: $quaternary-bg;
    border-radius: 10px;
    color: $secondary-text;
    cursor: pointer;
    @include lg {
        &:hover {
            background-color: $quinary-bg;
            cursor: pointer;
        }
    }
    .card-min-content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        flex-grow: 1;
        width: 100%;
    }
}
</style>
