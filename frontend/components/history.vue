<template>
    <Selection
        title="Вы недавно слушали"
        leftText="Cмотреть все"
        :leftTextLink="{ name: routesNames.library.history }"
    >
        <CardsContainer> </CardsContainer>
    </Selection>
</template>
<script setup>
import { routesNames } from "@typed-router";
import { Service } from "~~/client";
const viewport = useViewport();
</script>
