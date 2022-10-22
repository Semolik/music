<template>
    <div class="upload-song-container">
        <FormField :borderRadius="borderRadius" label="Название" v-model="name">
            <span :class="['count',{wrong: upToNameLimit < 0}]" v-if="nameLenght">{{upToNameLimit}}</span>
        </FormField>
        <div class="block">
            <SelectImage @changed="pictureUpdated" :pictureUrl="picture" name="userPicture" ref="selectPic" />
            <div class="fields-container">
                <FormField :borderRadius="borderRadius" label="Альбом" v-if="isSingle">
                    <template v-slot:side>
                        <div :class="['button',{active: followingName}]" @click="followingName = !followingName">
                            <FontAwesomeIcon icon='fa-paperclip' />
                        </div>
                    </template>
                </FormField>
                <FormField :borderRadius="borderRadius" label="Создан совместно с" v-model="feat">
                    <span :class="['count',{wrong: upToFeatLimit < 0}]" v-if="featLenght">{{upToFeatLimit}}</span>
                </FormField>
            </div>
        </div>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPaperclip } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import SelectImage from './SelectImage.vue';
import FormField from './FormField.vue';
library.add(faPaperclip);

export default {
    props: {
        isSingle: Boolean,
    },
    data() {
        return {
            picture: null,
            name: '',
            feat: '',
            borderRadius: 5,
            nameLimit: 30,
            featLimit: 50,
            followingName: false,
        };
    },
    components: { SelectImage, FormField, FontAwesomeIcon },
    methods: {
        pictureUpdated() {

        }
    },
    computed: {
        nameLenght() {
            return this.name.length
        },
        featLenght() {
            return this.feat.length
        },
        upToNameLimit() {
            return this.nameLimit - this.nameLenght
        },
        upToFeatLimit() {
            return this.featLimit - this.featLenght
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';

.upload-song-container {

    background-color: var(--color-background-mute-3);
    border-radius: 10px;
    border: 1px solid var(--color-background-mute-6);
    padding: 10px;

    .block {
        display: grid;
        grid-template-columns: 150px 1fr;
        gap: 10px;

        .fields-container {
            display: flex;
            flex-direction: column;

            .button {
                box-shadow: 0 0 0 1px var(--fields-border-color);
                border-radius: 5px;
                padding: 0px 10px;
                @include helpers.flex-center;
                cursor: pointer;

                &.active {
                    background-color: var(--purple-1);
                }

                svg {
                    width: 18px;
                    height: 18px;
                }
            }
        }
    }
}
</style>