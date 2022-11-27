<template>
    <selectionHead text="Клипы" :back-url="`/musician/${id}`" />
    <ClipsList :clips="clips" @clip-click="showVideo" />
    <ModalDialog :active="Boolean(modalData)" padding="" @close="closeVideo" max-width="1200px" >
        <iframe :style="{ aspectRatio: '16 / 9', width: '100%', borderRadius: '10px' }"
            :src="`https://www.youtube.com/embed/${modalData.video_id}`" title="YouTube video player" frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen v-if="modalData"></iframe>
    </ModalDialog>
    <div class="clip-buttons">
        <div class="load-more" @click="getNextPage" v-if="isbuttonShowed">Загрузить еще</div>
    </div>
</template>
<script>

import selectionHead from './selectionHead.vue';
import titleMixin from './titleMixin';
import ClipsList from '/src/components/Settings/Musician/Clips/clipsList.vue';
import ModalDialog from '/src/components/ModalDialog.vue';
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
    components: { selectionHead, ClipsList, ModalDialog },
    data() {
        return {
            buttonShowed: true,
            countOnPage: Number(this.VITE_CLIP_PAGE_COUNT),
            modalData: null,
        }
    },
    methods: {
        showVideo(videoInfo) {
            this.modalData = videoInfo;
        },
        closeVideo() {
            this.modalData = null;
        }
    }
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