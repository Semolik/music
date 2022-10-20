<template>
    <div class="buttons">
        <div :class="['button', {active: activeSelection==='single'}]" @click="activeSelection='single'">
            <div class="text">Сингл</div>
        </div>
        <div :class="['button', {active: activeSelection==='album'}]" @click="activeSelection='album'">
            <div class="text">Альбом</div>
        </div>
    </div>
    <div class="songs">
        <UploadSong v-if="activeSelection==='single'" />
        <template v-else>
            <UploadSong />
            <div class="add-button-container">
                <div class="add-button">
                    <FontAwesomeIcon icon="fa-plus" />
                </div>
            </div>
        </template>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import UploadSong from '../components/PersonalАccountMusicianCabinetUploadSong.vue'

library.add(faPlus);
export default {
    components: [UploadSong, FontAwesomeIcon],
    data() {
        return {
            activeSelection: 'single',
        }
    }
}
</script>
<style lang="scss" scoped>
@use '@/assets/styles/components';

.buttons {
    display: grid;
    gap: 5px;
    grid-template-columns: repeat(2, 1fr);

    .button {
        @include components.button;
    }
}
</style>