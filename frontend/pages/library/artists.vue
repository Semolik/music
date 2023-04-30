<template>
    <div class="favorite-musicians">
        <CardsContainer>
            <MusicianCard
                v-for="(musician, index) in musicians"
                :key="musician.id"
                v-model:musician="musicians[index]"
            />
        </CardsContainer>
        <NotFound v-if="!musicians.length" />
        <AppButton v-if="loadMoreButton" @click="loadMore">
            Загрузить еще
        </AppButton>
    </div>
</template>
<script setup>
import { Service } from "~/client";
const { FAVORITE_MUSICIANS_LIMIT } = useRuntimeConfig().public;
const musicians = ref([]);
const page = ref(0);
const loadMoreButton = ref(false);
const loadMore = async () => {
    page.value++;
    const new_musicians =
        await Service.getLikedMusicianProfilesApiV1MusicianLikedGet(page.value);
    musicians.value = musicians.value.concat(new_musicians);
    loadMoreButton.value = new_musicians.length == FAVORITE_MUSICIANS_LIMIT;
};
loadMore();
</script>
<style lang="scss" scoped>
.favorite-musicians {
    display: flex;
    flex-direction: column;
    height: 100%;
}
</style>
