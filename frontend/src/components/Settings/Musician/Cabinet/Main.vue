<template>
    <div class="buttons">
        <router-link to="/lk/my-music/upload" class="button">
            <div class="icon">
                <FontAwesomeIcon icon="fa-plus" />
            </div>
            <div class="text">Загрузить</div>
        </router-link>
        <router-link to="/lk/my-music/albums" class="button">
            <div class="icon">
                <FontAwesomeIcon icon="fa-music" />
            </div>
            <div class="text">Альбомы</div>
        </router-link>
    </div>
    <FormField placeholder="Поиск" :borderRadius="7"></FormField>
</template>
<style lang="scss" scoped>
@use '@/assets/styles/helpers';
@use '@/assets/styles/components';

.buttons {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;

    .button {
        @include components.button;
    }
}
</style>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlus, faMusic } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import FormField from '/src/components/FormField.vue';
library.add(faPlus, faMusic);
export default {
    components: {
        FontAwesomeIcon,
        FormField
    }
}
</script>
