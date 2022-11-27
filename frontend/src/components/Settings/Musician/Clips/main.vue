<template>
    <router-link to="/lk/my-music/clips/add" class="add-clip-button">
        <FontAwesomeIcon icon='fa-plus' />
    </router-link>
    <ClipsList base-url="/lk/my-music/clips/" :clips="filteredClips" />
    <div class="clip-buttons">
        <div class="load-more" @click="getNextPage" v-if="isbuttonShowed">Загрузить еще</div>
    </div>
</template>
<script>
import { useClipsGetter } from '/src/composables/clips';
import FormField from '/src/components/FormField.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import ClipsList from './clipsList.vue';
library.add(faPlus)
export default {
    components: { FormField, FontAwesomeIcon, ClipsList },
    async setup() {
        const { getNextPage, clips, isbuttonShowed } = useClipsGetter(null, true, true);
        return { getNextPage, clips, isbuttonShowed }
    },
    data() {
        return {
            text: ''
        }
    },
    computed: {
        filteredClips() {
            if (!this.text) return this.clips
            return this.clips.filter(clip => clip.name.toLowerCase().includes(this.text.toLowerCase()))
        }
    }
}
</script>
<style lang="scss" scoped>
@use '@/assets/styles/components';
@use '@/assets/styles/helpers';

.add-clip-button {
    @include components.button;
    @include helpers.flex-center;
    padding: 10px !important;
    outline: 1px solid var(--fields-border-color);
    background-color: var(--color-background-mute-4);
    padding: 0;

    &:hover {
        background-color: var(--color-background-mute-5);
    }
}

.clip-buttons {
    @include helpers.flex-center;

    .load-more {
        @include components.button;
        padding: 5px 20px;
    }
}
</style>