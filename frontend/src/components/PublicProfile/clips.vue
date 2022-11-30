<template>
    <selectionHead text="Клипы" :back-url="`/musician/${id}`" />
    <ClipsList :clips="clips" @clip-click="$emit('clip-click', $event)"/>
    <div class="clip-buttons">
        <div class="load-more" @click="getNextPage" v-if="isbuttonShowed">Загрузить еще</div>
    </div>
</template>
<script>

import selectionHead from './selectionHead.vue';
import titleMixin from './titleMixin';
import ClipsList from '/src/components/Settings/Musician/Clips/clipsList.vue';

import { useClipsGetter } from '/src/composables/clips';
export default {
    setup(props) {
        const { getNextPage, clips, isbuttonShowed } = useClipsGetter(props.id);
        return { getNextPage, clips, isbuttonShowed }
    },
    props: {
        id: String
    },
    mixins: [titleMixin],
    components: { selectionHead, ClipsList },
    data() {
        return {
            buttonShowed: true,
            countOnPage: Number(this.VITE_CLIP_PAGE_COUNT),
        }
    },
    
}
</script>
<style scoped lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/components';

.clip-buttons {
    @include helpers.flex-center;

    .load-more {
        @include components.button;
        padding: 5px 20px;
    }
}
</style>