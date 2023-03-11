<template>
    <SetupContainer
        @skip="$router.push({ name: routesNames.settings.profile })"
        skip-button
        :next-button="false"
        v-model:search="search"
        :placeholder="typingText"
    >
        <template #headline>
            Выберите музыкантов,<br v-if="$viewport.isGreaterOrEquals('lg')" />
            которые вам нравятся
        </template>
        <template #description>
            Это поможет получать более точные и интересные рекомендации
        </template>
        <template #items>
            <SetupMusiciansCard
                v-for="(musician, index) in musicians"
                :musician="musician"
                @liked="(liked) => onLike(liked, index)"
                :key="musician.id"
            />
        </template>
    </SetupContainer>
</template>
<script setup>
import { Service } from "~~/client";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
import { routesNames } from "~~/.nuxt/typed-router";
const { logined } = storeToRefs(useAuthStore());
const router = useRouter();
if (!logined.value) {
    router.push({ name: routesNames.login });
}
const search = ref("");
const randomMusicians =
    await Service.getRandomMusicianProfilesApiV1MusicianRandomGet();
const randomMusiciansNames = randomMusicians.map((m) => m.name);
const { typingText } = useTyping(
    randomMusiciansNames,
    "Найдите своего любимого исполнителя"
);

const popularMusicians = ref(
    await Service.getPopularMusicianProfilesApiV1MusicianPopularGet()
);
const musicians = ref(popularMusicians.value);
const onLike = (liked, index) => {
    musicians.value[index].liked = liked;
    if (musicians.value === popularMusicians.value) {
        return;
    }
    var removeArray = musicians.value.filter(function (item) {
        return item.liked == false;
    });
    var keepArray = musicians.value.filter(function (item) {
        return item.liked == true;
    });
    musicians.value = keepArray.concat(removeArray);
};
watch(
    search,
    async (value) => {
        if (!value) {
            musicians.value = popularMusicians.value;
            return;
        }
        musicians.value = await Service.searchMusicianApiV1SearchMusicianGet(
            value
        );
    },
    { immediate: true }
);
</script>
