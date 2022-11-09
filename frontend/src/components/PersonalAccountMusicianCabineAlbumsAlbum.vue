<template>
    <div class="album-editor" v-if="albumInfo">
        <div class="album-head">
            <AlbumPicture :src="albumInfo.picture" offHover />
            <div class="album-info">
                <div class="headline">{{ albumInfo.name }}</div>
                <div class="extra-info">
                    <div class="item">Год: {{ albumInfo.year }}</div>
                    <router-link to="" class="item">Музыкант: {{ albumInfo.musician.name }}</router-link>
                    <router-link to="" class="item">сюда жанр</router-link>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { HTTP } from '../http-common.vue';
import { useToast } from "vue-toastification";
import handleError from '../composables/errors';
import AlbumPicture from './AlbumPicture.vue';
export default {
    setup() {
        const toast = useToast();
        return {
            toast
        };
    },
    props: {
        id: {
            type: [Number, String],
        },
    },
    data() {
        return {
            albumInfo: null
        };
    },
    mounted() {
        HTTP.get("get_album", { params: { id: this.id } })
            .then(response => {
                this.albumInfo = response.data;
            })
            .catch(error => {
                this.toast.error(handleError(error).message);
            });
    },
    components: { AlbumPicture }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
.album-editor {
    display: flex;
    flex-direction: column;

    .album-head {
        display: grid;
        grid-template-columns: 200px 1fr;
        gap: 10px;

        .album-info {
            display: flex;
            flex-direction: column;

            .headline {
                text-align: center;
                font-weight: 600;
                font-size: x-large;
                margin-bottom: 10px;
                width: 100%;
                @include helpers.flex-center;
            }

            .extra-info {
                display: flex;
                // justify-content: center;
                gap: 10px;


                .item {
                    color: var(--color-header-text);
                    text-decoration: none;
                    display: flex;
                    align-items: center;
                    transition: .2s color;
                    background-color: var(--color-background-mute-3);
                    padding: 8px 16px;
                    border-radius: 10px;

                    // &:not(:last-child)::after {
                    //     content: '';
                    //     background-color: var(--vt-c-white-100);
                    //     height: 3px;
                    //     width: 3px;
                    //     border-radius: 50%;
                    //     margin-inline: 5px;
                    // }
                }

                a.item:hover {
                    color: #fc0;
                }
            }
        }
    }
}
</style>