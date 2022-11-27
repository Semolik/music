<template>
    <div class="description" v-if="publicProfileData.description">
        {{ publicProfileData.description }}
    </div>
    <div class="musician-clips">
        <div class="headline">Клипы</div>
        <ClipsList :clips="publicProfileData.clips" :watch-more-link="`/musician/${publicProfileData.id}/clips`" />
    </div>
</template>
<script>
import ClipsList from '/src/components/Settings/Musician/Clips/clipsList.vue';
import titleMixin from './titleMixin';
export default {
    inject: ['publicProfileData'],
    components: {
        ClipsList
    },
    mixins: [titleMixin]
}
</script>
<style scoped lang="scss">
.musician-clips {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .clips-slider {
        .flicking-camera {
            gap: 10px;

            .clip-item {
                width: 300px;
            }
        }
    }
}
</style>