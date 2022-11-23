<template>
    <div class="selections">
        <router-link to="/lk/edit-musician-section/genres" class="selection">
            <div class="text">Жанры</div>
        </router-link>
    </div>
    <router-view></router-view>
</template>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/components';

.selections {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;

    .selection {
        @include components.button;
    }
}
</style>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlus, faMusic } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import FormField from '../../FormField.vue';
library.add(faPlus, faMusic);
export default {
    components: {
        FontAwesomeIcon,
        FormField
    }
}
</script>