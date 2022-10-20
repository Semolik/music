<template>
    <div class="buttons">
        <router-link to="/lk/my-music/upload" class="button">
            <div class="icon">
                <FontAwesomeIcon icon="fa-plus" />
            </div>
            <div class="text">Загрузить</div>
        </router-link>
        <div class="button">
            <div class="icon">
                <FontAwesomeIcon icon="fa-music" />
            </div>
            <div class="text">Плейлисты</div>
        </div>
    </div>
    <FormField placeholder="Поиск" :borderRadius="10"></FormField>
</template>
<style lang="scss">
@use '@/assets/styles/helpers';

.buttons {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;

    .button {
        display: flex;
        flex-direction: column;
        background-color: var(--color-background-mute-3);
        padding: 10px;
        gap: 5px;
        border-radius: 15px;
        cursor: pointer;
        text-decoration: none;
        color: var(--color-text);

        &:hover {
            background-color: var(--color-background-mute-4);
        }

        .icon {
            @include helpers.flex-center;

            svg {
                height: 25px;
            }
        }

        .text {
            text-align: center;
        }
    }
}
</style>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlus, faMusic } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import FormField from './FormField.vue';
library.add(faPlus, faMusic);
export default {
    components: {
        FontAwesomeIcon,
        FormField
    }
}
</script>
