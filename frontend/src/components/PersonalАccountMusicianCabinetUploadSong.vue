<template>
    <div class="upload-song-container">
        <SelectImage @changed="pictureUpdated" :pictureUrl="picture" name="userPicture" ref="selectPic" />
    </div>
</template>
<script>
import SelectImage from './SelectImage.vue';

export default {
    data() {
        return {
            picture: null,
        };
    },
    components: { SelectImage },
    methods: {
        pictureUpdated() {

        }
    }
}
</script>
<style lang="scss">
.upload-song-container {
    display: grid;
    grid-template-columns: 120px 1fr;
    background-color: var(--color-background-mute-3);
    border-radius: 10px;
    border: 1px solid var(--color-background-mute-6);
    padding: 10px;
}
</style>