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
        <UploadSong v-if="activeSelection==='single'" isSingle/>
        <template v-else>
            <FormField :borderRadius="10" label="Название альбома" />
            <UploadSong />
            <div class="add-buttons-container">
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
import FormField from './FormField.vue';

library.add(faPlus);
export default {
    data() {
        return {
            activeSelection: "single",
        };
    },
    components: { FormField, UploadSong, FontAwesomeIcon }
}
</script>
<style lang="scss" scoped>
@use '@/assets/styles/components';
@use '@/assets/styles/helpers';

.buttons {
    display: grid;
    gap: 5px;
    grid-template-columns: repeat(2, 1fr);

    .button {
        @include components.button;
    }

}

.songs {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .add-buttons-container {
        display: flex;
        justify-content: right;

        .add-button {
            @include components.button;
            @include helpers.flex-center;
            height: 45px;
            width: 45px;
        }
    }
}
</style>