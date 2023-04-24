<template>
    <Selection
        title="Новые релизы"
        leftText="Cмотреть все"
        :leftTextLink="{ name: routesNames.newReleases }"
    >
        <CardsContainer> </CardsContainer>
    </Selection>
</template>
<script setup>
import { routesNames } from "@typed-router";
</script>
