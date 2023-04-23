<template>
    <div class="clips-page">
        <AddSearch
            v-model:search="search"
            placeholder="Поиск по вашим клипам"
            :to="{ name: 'musician-cabinet-clips-add' }"
        />
        <CardsContainer :mdWidth="200" :width="250">
            <ClipCard
                v-for="clip in clips"
                :key="clip.id"
                :clip="clip"
                :link="{
                    name: routesNames.musicianCabinet.cabinetClipsId,
                    params: { id: clip.id },
                }"
            />
        </CardsContainer>
        <NotFound :text="notFoundClipsMessage" v-if="notFoundClips" />
    </div>
</template>
<script setup>
import { routesNames } from "@typed-router";
import { Service } from "@/client";
const my_clips = await Service.getMyClipsApiV1ClipsMyGet();
const clips = ref(my_clips);
const search = ref("");
const fetching = ref(false);
const notFoundClips = computed(() => {
    if (fetching.value) return false;

    return clips.value.length === 0;
});
const notFoundClipsMessage = computed(() => {
    if (search.value === "") return "У вас нет клипов";
    return null;
});
watch(search, async (value) => {
    if (value === "") {
        clips.value = my_clips;
        return;
    }
    clips.value = await Service.searchMyClipsApiV1ClipsMySearchGet(value);
});
</script>
<style lang="scss" scoped>
.clips-page {
    color: $primary-text;
    display: flex;
    flex-direction: column;
    gap: 10px;
    --clip-card-hover-bg: #{$quaternary-bg};
}
</style>
