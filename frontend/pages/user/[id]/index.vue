<template>
    <ContentHead
        :name="fullName"
        hide-all-buttons
        type="Пользователь"
        :picture="user.picture"
        :icon="IconsNames.userIcon"
    >
        <div class="user-page">
            <Selection
                title="Плейлисты"
                leftText="Все плейлисты"
                :leftTextLink="{
                    name: routesNames.userIdPlaylists,
                    params: { id },
                }"
            >
                <CardsContainer class="cards-contaner">
                    <PlaylistCard
                        v-for="playlist in user.last_playlists"
                        :playlist="playlist"
                        :key="playlist.id"
                        is-link
                    />
                </CardsContainer>
            </Selection>
        </div>
    </ContentHead>
</template>
<script setup>
import { Service } from "~/client";
import { IconsNames } from "~/configs/icons";
import { routesNames } from "@typed-router";
definePageMeta({
    disableDefaultLayoutPadding: true,
});
const { id } = useRoute().params;
const user = await Service.getUserInfoByIdApiV1UsersUserIdGet(id);
const fullName = useFullName(user);
</script>
<style lang="scss" scoped>
.cards-contaner {
    grid-template-rows: repeat(2, 1fr);
    grid-auto-rows: 0;
    overflow-y: hidden;
    &.min {
        *:nth-child(n + 5) {
            display: none;
        }
    }
}
.user-page {
    display: flex;
    flex-direction: column;
    padding: 10px;
    gap: 10px;
}
</style>
