<template>
    <div class="buttons">
        <div :class="['button', { active: activeSelection === 'single' }]" @click="activeSelection = 'single'">
            <div class="text">Сингл</div>
        </div>
        <div :class="['button', { active: activeSelection === 'album' }]" @click="activeSelection = 'album'">
            <div class="text">Альбом</div>
        </div>
    </div>
    <div class="songs">
        <FormField :borderRadius="10" label="Название альбома" v-if="!singleMode" off-margin notEmpty/>
        <UploadSong :track="track" @update="trackUpdate($event, index)" is-single v-if="singleMode" />
        <template v-else>
            <UploadSong :id="index" :track="track" @update="trackUpdate($event, index)" v-for="(track, index) in tracks" />
        </template>
        <div class="buttons-container">
            <div class="button-block" @click="addTrack" v-if="!singleMode">
                <FontAwesomeIcon icon="fa-plus" />
            </div>
            <div :class="['button-block', { active: buttonActive }]" @click="save">
                <FontAwesomeIcon icon="fa-floppy-disk" />
            </div>
        </div>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import { faFloppyDisk } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { computed } from '@vue/reactivity';
import UploadSong from '../components/PersonalАccountMusicianCabinetUploadSong.vue'
import FormField from './FormField.vue';

library.add(faPlus, faFloppyDisk);
export default {
    data() {
        return {
            activeSelection: "single",
            tracks: [{}],
            track: {},
            runValidation: false,
        };
    },
    provide() {
        return {
            runValidation: computed(() => this.runValidation)
        }
    },
    watch: {
        singleMode(value) {
            this.tracks = [{}];
            this.track = {};
        },

    },
    methods: {
        toggleRunValidation() {
            this.runValidation = false;
            this.runValidation = true;
            setTimeout(() => {
                this.runValidation = false;
            }, 300)
        },
        trackUpdate(event, index) {
            if (this.singleMode) {
                this.track = event;
            } else {
                this.tracks[index] = event;
            }
        },
        addTrack() {
            this.tracks.push(this.trackTemplate);
        },
        save() {
            this.toggleRunValidation();
        }
    },
    components: { FormField, UploadSong, FontAwesomeIcon },
    computed: {
        singleMode() {
            return this.activeSelection === 'single'
        },
        buttonActive() {
            if (this.singleMode) {
                return this.track.isValid
            }
            else {
                return this.tracks.filter(el => el?.isValid).length == this.tracks.length
            }
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

    .buttons-container {
        display: flex;
        justify-content: right;
        gap: 5px;

        .button-block {
            @include components.button;
            @include helpers.flex-center;
            height: 45px;
            width: 45px;

            &.active {
                background-color: var(--purple-1);
            }

            svg {
                width: 20px;
                height: 20px;
            }
        }
    }
}
</style>