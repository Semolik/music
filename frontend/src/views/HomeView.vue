<template>
  <div class="home-container">
    <aside>
      <div class="item" >
        <div class="button-content">
          <div class="text">наушники</div>
        </div>
        <div class="list">
          <div class="item">dfsfsdfs</div>
        </div>
      </div>
    </aside>
  </div>
</template>

<script>
// import BaseContainer from '../components/BaseContainer.vue';
// import { library } from '@fortawesome/fontawesome-svg-core';
// import { faCaretDown } from '@fortawesome/free-solid-svg-icons';
// import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
// library.add(faCaretDown);
export default {
  components: {  }
}
</script>

<style lang="scss">
@use '../assets/styles/breakpoints';

.home-container {
  display: grid;
  width: 100%;
  grid-template-columns: 280px 1fr;

  aside {
    background-color: var(--color-background-soft);
    padding: 5px;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    gap: 5px;
    min-height: 600px;

    .item {
      background-color: var(--color-background-mute);
      padding: 10px;
      border-radius: 15px;
      display: flex;
      cursor: pointer;
      flex-direction: column;
      gap: 5px;

      .button-content {
        display: flex;
        flex-grow: 1;
      }

      .list {
        display: none;
        // display: flex;
      }

      &:not(.active):hover {
        background-color: var(--color-background-mute-2);
      }

      &.active {
        background-color: var(--color-background-mute-3);

        .list {
          display: flex;
        }
      }

      .icon {
        margin-left: auto;
      }
    }
  }
}
</style>