<template>
    <Selection
        title="Вы недавно слушали"
        leftText="Cмотреть все"
        :leftTextLink="{ name: routesNames.library.history }"
        v-if="items.length > 0"
    >
        <CardsContainer one-line>
            <template v-for="item in items">
                <AlbumCard
                    v-model:album="item.info"
                    v-if="item.type == 'album'"
                    is-link
                />
                <MusicianCard
                    v-model:musician="item.info"
                    v-else-if="item.type == 'musician'"
                    is-link
                />
                <PlaylistCard
                    v-model:playlist="item.info"
                    v-else-if="item.type == 'playlist'"
                    is-link
                />
            </template>
        </CardsContainer>
    </Selection>
</template>
<script setup>
import { routesNames } from "@typed-router";
import { Service } from "~~/client";
const items = ref(await Service.getHistoryApiV1HistoryGet());
</script>
