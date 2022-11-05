<template>
    <FormField placeholder="Поиск" :borderRadius="10"></FormField>
    <div class="albums">
        <Album :albumInfo="album" v-for="album in albums" />
    </div>
</template>
<script>
import { HTTP } from '../http-common.vue';
import FormField from './FormField.vue';
import { useToast } from "vue-toastification";
import handleError from '../composables/errors';
import Album from '../components/PersonalAccountMusicianCabineAlbumsItem.vue';
export default {
    setup() {
        const toast = useToast();
        return {
            toast
        }
    },
    components: {
        FormField,
        Album
    },
    data() {
        return {
            albums: []
        }
    },
    mounted() {
        HTTP.get('get_my_albums')
            .then(response => {
                this.albums = response.data;
            })
            .catch(error => {
                this.toast.error(handleError(error, `При получении альбомов произошла ошибка`).message)
            });
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/breakpoints';
.albums {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px
    // @include breakpoints.lg(true) {
    //     grid-template-columns: repeat(4, 1fr);
    // }
    // @include breakpoints.md(true) {
    //     grid-template-columns: repeat(3, 1fr);
    // }
    // @include breakpoints.sm(true) {
    //     grid-template-columns: repeat(2, 1fr);
    // }
}
</style>