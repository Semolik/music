<template>
    <div class="clip-card">
        <div class="clip-card-picture">
            <img :src="clip.picture" />
        </div>
        <div class="clip-info">
            <div class="name">
                {{ clip.name }}
            </div>
            <div class="splitter">-</div>
            <div class="musician">
                {{ musicianName }}
            </div>
        </div>
    </div>
</template>
<script setup>
const { clip, musicianInfo } = defineProps({
    clip: Object,
    musicianInfo: {
        type: Object,
        required: false,
    },
});
const musicianName = computed(() => musicianInfo?.name || clip.musician?.name);
</script>
<style lang="scss" scoped>
.clip-card {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 5px;
    border-radius: 10px;
    cursor: pointer;

    &:hover {
        background-color: $tertiary-bg;
    }
    .clip-card-picture {
        background-color: $secondary-bg;
        aspect-ratio: 16 / 9;
        border-radius: 5px;
        overflow: hidden;
        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    }
    .clip-info {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;

        .splitter {
            color: $secondary-text;
        }
        .name {
            color: $primary-text;
        }
        .musician {
            color: $secondary-text;
        }
    }
}
</style>
