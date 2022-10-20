<template>
    <div class="buttons">
        <div :class="['button', {active: activeSelection==='single'}]" @click="activeSelection='single'">
            <div class="text">Сингл</div>
        </div>
        <div :class="['button', {active: activeSelection==='album'}]" @click="activeSelection='album'">
            <div class="text">Альбом</div>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            activeSelection: 'single',
        }
    }
}
</script>
<style lang="scss">
.buttons {
    grid-template-columns: repeat(2, 1fr);

    .button.active {
        background-color: var(--purple);
    }
}
</style>