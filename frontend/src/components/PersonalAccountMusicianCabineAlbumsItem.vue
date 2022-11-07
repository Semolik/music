<template>
    <router-link class="album" :to="`/lk/my-music/albums/${albumInfo.id}`">
        <AlbumPicture :src="albumInfo.picture" />
        <div class="name">{{ albumInfo.name }}</div>
        <div class="year">{{ albumInfo.year }}</div>
    </router-link>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faMusic } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import AlbumPicture from './AlbumPicture.vue';
library.add(faMusic);

export default {
    props: {
        albumInfo: Object
    },
    components: {
        FontAwesomeIcon,
        AlbumPicture
    }
}
</script>
<style lang="scss">
.album {
    display: flex;
    flex-direction: column;
    cursor: pointer;
    color: var(--color-text);
    text-decoration: none;
    text-align: center;


    .name {
        font-weight: 600;
        padding-left: 10px;

    }

    .year {
        color: var(--vt-c-white-150);
        font-size: 0.9em;
    }

}
</style>