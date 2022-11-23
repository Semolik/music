<template>
    <a class="file" :href="file.url">
        <div class="icon">
            <img :src="file.url" alt="" v-if="file.type==='image'">
            <FontAwesomeIcon v-else icon="fa-file" />
        </div>
        <div class="name">{{file.original_file_name}}</div>
    </a>

</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faFile } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faFile);

export default {
    props: {
        file: Object
    },
    components: { FontAwesomeIcon }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';

.file {
    color: var(--color-text);
    text-decoration: none;
    background-color: var(--color-background-mute-4);
    border-radius: 15px;
    padding: 5px;
    cursor: pointer;
    gap: 5px;
    flex-grow: 1;
    display: flex;
    text-align: center;


    .icon {
        width: 50px;
        height: 50px;
        position: relative;
        background-color: var(--color-background-mute-5);
        border-radius: 10px;
        @include helpers.flex-center;

        svg {
            width: 30px;
            height: 30px;
        }

        img {
            position: absolute;
            inset: 0;
            width: 50px;
            height: 50px;
            object-fit: cover;
            border-radius: 10px;
        }
    }

    &:hover {
        background-color: var(--color-background-mute-6);
    }

    .name {
        @include helpers.flex-center;
        overflow-wrap: anywhere;
        white-space: break-spaces;
        text-align: center;
        flex-grow: 1;
    }
}
</style>