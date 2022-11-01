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
        <template v-if="!singleMode">
            <div class="columns">
                <FormField :borderRadius="10" label="Название альбома" off-margin notEmpty />
                <date-picker v-model="date" is-dark mode="dateTime" is24hr>
                    <template v-slot="{ inputValue, inputEvents }">
                        <FormField class="calendar" :modelValue="inputValue" :inputEvents="inputEvents" label="Начало активности"
                            :borderRadius="10" off-margin>
                            <FontAwesomeIcon icon="fa-calendar" />
                        </FormField>
                    </template>
                </date-picker>
            </div>
        </template>
        <UploadSong :track="track" ref="track" @update="trackUpdate($event)" is-single v-if="singleMode" />
        <template v-else>
            <UploadSong :ref="`track-${index}`" :id="index" :track="track" @update="trackUpdate($event, index)"
                v-for="(track, index) in tracks" />
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
import { faPlus, faCalendar } from '@fortawesome/free-solid-svg-icons';
import { faFloppyDisk } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { computed } from '@vue/reactivity';
import UploadSong from '../components/PersonalАccountMusicianCabinetUploadSong.vue'
import { HTTP } from '../http-common.vue';
import FormField from './FormField.vue';
import { useToast } from "vue-toastification";
import { DatePicker } from 'v-calendar';

library.add(faPlus, faFloppyDisk, faCalendar);
export default {
    setup() {
        const toast = useToast();
        return {
            toast
        }
    },
    data() {
        return {
            activeSelection: "single",
            tracks: [{}],
            track: {},
            runValidation: false,
            date: new Date(),
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
        async save() {
            this.toggleRunValidation();
            if (this.buttonActive) {
                let album = await HTTP.post('/create-album')
                    .then(response => response.data)
                    .catch(error => { });
                if (!album) {
                    this.toast.error('Произошла ошибка при создании альбома');
                }
                // if (this.singleMode) {
                //     this.$refs.sendFile();
                // } else {
                //     for (let index = 0; index < this.tracks.length; index++) {
                //         this.$refs[`track-${index}`].sendFile();
                //     }
                // }
            }
        }
    },
    components: { FormField, UploadSong, FontAwesomeIcon, DatePicker },
    computed: {
        singleMode() {
            return this.activeSelection === 'single'
        },
        buttonActive() {
            console.log(this.track);
            if (this.activeSelection === 'single') {
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
@use '@/assets/styles/breakpoints';


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

    .columns {
        display: grid;
        grid-template-columns: 1fr 200px;
        gap: 10px;

        @include breakpoints.md(true) {
            grid-template-columns: 1fr;
        }

        .calendar {
            svg {
                padding: 10px;
            }
        }
    }

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