<template>
    <div class="edit-genre" v-if="genreData">
        <SelectImage @changed="pictureUpdated" :pictureUrl="genreData.picture" name="genrePicture" ref="selectPic" />
        <div class="left-area">
            <FormField :border-radius="10" label="Название жанра" v-model="genreName" not-empty>
                <span :class="['count', { wrong: genreNameLimit < 0 }]">{{ genreNameLimit }}</span>
            </FormField>
            <ButtonsBlock @click="save" :active="buttonActive" :wrong="dataWrong" :delete-button="!add"
                @delete="deleteGenre" />
        </div>
    </div>
</template>
<script>
import FormField from '/src/components/FormField.vue';
import SelectImage from '/src/components/SelectImage.vue';
import handleError from '/src/composables/errors';
import ButtonsBlock from '/src/components/Settings/ButtonsBlock.vue';
import { HTTP } from '/src/http-common.vue';
import { useToast } from "vue-toastification";
import { library } from '@fortawesome/fontawesome-svg-core';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faTrash);

export default {
    props: {
        id: {
            type: [Number, String],
        },
        add: Boolean,
    },
    components: { SelectImage, FormField, ButtonsBlock, FontAwesomeIcon },
    setup() {
        const { VITE_MAX_GENRE_NAME_LENGTH } = import.meta.env;
        const toast = useToast();
        return {
            VITE_MAX_GENRE_NAME_LENGTH,
            toast
        }
    },
    data() {
        return {
            genreData: null,
            genreName: '',
            isPictureUpdated: false,
            targetPicture: null
        }
    },
    mounted() {
        if (this.add) {
            this.genreData = {
                name: '',
                picture: ''
            }
            return;
        }
        HTTP.get('genres/genre', { params: { id: this.id } })
            .then(response => {
                this.genreData = response.data;
                this.genreName = this.genreData.name;
            }).catch(error => {
                this.toast.error(handleError(error).message);
            })
    },
    methods: {
        save() {
            if (!this.buttonActive) return
            var form = new FormData();
            let picture = this.genrePicture;
            if (picture) {
                form.append('genrePicture', picture)
            }
            form.append('name', this.genreName);
            if (this.add) {
                HTTP.post('genres/genre', form)
                    .then(response => {
                        this.$router.push({ path: `/lk/edit-musician-section/genres/${response.data.id}`, props: { add: false } })
                    }).catch(error => {
                        this.toast.error(handleError(error).message);
                    })
                return
            }
            form.append('id', this.genreData.id);
            HTTP.put('genres/genre', form)
                .then(response => {
                    this.genreData = response.data;
                    this.isPictureUpdated = false;
                }).catch(error => {
                    this.toast.error(handleError(error).message);
                })
        },
        deleteGenre() {
            HTTP.delete('genres/genre', { params: { id: this.genreData.id } })
                .then(response => {
                    this.$router.push({ path: '/lk/edit-musician-section/genres' })
                }).catch(error => {
                    this.toast.error(handleError(error).message);
                })
        },
        pictureUpdated(target) {
            this.isPictureUpdated = true;
            this.targetPicture = target;
        }
    },
    computed: {
        genreNameLimit() {
            let length = this.genreName?.length;
            if (!length) return null
            return this.VITE_MAX_GENRE_NAME_LENGTH - length
        },
        dataWrong() {
            if (this.add) {
                return this.genreNameLimit < 0 || this.genreName.length === 0 || !this.targetPicture
            }
            if (this.genreNameLimit === null) return true
            return this.genreNameLimit < 0 || this.genreName.length === 0
        },
        dataChanged() {
            if (!this.genreData) return
            if (this.add) {
                return this.genreData.name !== this.genreName && this.isPictureUpdated
            }
            return this.genreData.name !== this.genreName || this.isPictureUpdated
        },
        genrePicture() {
            let target = this.$refs.selectPic?.target;
            return target ? target[0] : target
        },
        buttonActive() {
            return this.dataChanged && !this.dataWrong
        }
    }
}
</script>
<style lang="scss" scoped>
@use '@/assets/styles/helpers';
@use '@/assets/styles/breakpoints';

.edit-genre {
    display: grid;
    grid-template-columns: 150px 1fr;
    gap: 10px;

    .left-area {
        display: flex;
        flex-direction: column;

    }

}
</style>