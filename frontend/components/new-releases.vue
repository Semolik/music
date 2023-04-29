<template>
    <Selection
        title="Новые релизы"
        leftText="Cмотреть все"
        :leftTextLink="{ name: routesNames.newReleases }"
    >
        <CardsContainer one-line>
            <AlbumCard
                v-for="album in newAlbums"
                :key="album.id"
                :album="album"
            />
        </CardsContainer>
    </Selection>
</template>
<script setup>
import { Service } from "~/client";
import { routesNames } from "@typed-router";
const newAlbums = await Service.getLastAlbumsApiV1AlbumsLastGet(1, 10);
</script>
