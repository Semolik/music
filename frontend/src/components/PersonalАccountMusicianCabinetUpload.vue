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
        <FormField :borderRadius="10" label="Название альбома" v-if="!singleMode" off-margin/>
        <UploadSong :track="track" @update="trackUpdate($event,index)" :is-single="singleMode"
            v-for="(track, index) in tracks" />
        <div class="add-buttons-container" v-if="!singleMode">
            <div class="add-button" @click="addTrack">
                <FontAwesomeIcon icon="fa-plus" />
            </div>
        </div>

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
            tracks: [{}],
        };
    },
    watch: {
        singleMode(value) {
            if (value && this.tracks.length > 1) {
                this.tracks = [this.tracks[0]];
            }
        }
    },
    methods: {
        trackUpdate(event, index) {
            console.log(event, index)
        },
        addTrack() {
            this.tracks.push(this.trackTemplate);
        }
    },
    components: { FormField, UploadSong, FontAwesomeIcon },
    computed: {
        singleMode() {
            return this.activeSelection === 'single'
        }
    }
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