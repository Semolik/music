<template>
    <Selection
        title="Вы недавно слушали"
        leftText="Cмотреть все"
        :leftTextLink="{ name: routesNames.library.history }"
    >
        <CardsContainer>
            <template v-for="item in items">
                <AlbumCard
                    :album="item.info"
                    v-if="item.type == 'album'"
                    is-link
                />
                <MusicianCard
                    :musician="item.info"
                    v-else-if="item.type == 'musician'"
                    is-link
                />
                <PlaylistCard
                    :playlist="item.info"
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
const items = await Service.getHistoryApiV1HistoryGet();
const viewport = useViewport();
</script>
