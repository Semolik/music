<script >
import { RouterView } from 'vue-router';
import AppHeader from './components/AppHeader.vue';
import { computed } from 'vue';
import AppError from './components/AppError.vue';
import handleError from './composables/errors';

export default {
  components: {
    RouterView,
    AppHeader,
    AppError
  },
  data() {
    return {

      loading: false,
      windowWidth: window.innerWidth,
      blur_content: false,
      error: null,
    }
  },
  provide() {
    return {
      loading: computed(() => this.loading),
      windowWidth: computed(() => this.windowWidth),
      disableLoading: false,
    }
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', this.onResize);
    });
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  },
  methods: {
    setLoading(status) {
      this.loading = status;
    },
    blurAppContent(value) {
      console.log(value)
      this.blur_content = value;
    },
    onResize() {
      this.windowWidth = window.innerWidth
    },
    hideBodyOverflow(value) {
      console.log(value)
      document.body.style.overflow = value ? 'hidden' : '';
    },
    setError(data) {
      this.error = data;
    },
    handleAppError(error) {
      this.error = handleError(error);
    }
  },

}

</script>

<template >
  <AppHeader @blur_content="blurAppContent" @hide_body_overflow="hideBodyOverflow" @reset_error="error = null" />
  <div :class="['app-content', { blur: blur_content }]">
    <router-view v-slot="{ Component, route }">
      <transition name="list" mode="out-in">
        <div :key="route.name" class="transition-wrapper">
          <component :is="Component" @loading="setLoading" @request_error="handleAppError" @error="setError"
            v-if="!error" />
          <AppError @reset_error="error = null" v-else :inputMessage="error.message" :inputStatusCode="error.status" />
        </div>
      </transition>
    </router-view>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/animations';

.app-content {
  margin-right: calc(-1 * (100vw - 100%));
  padding-inline: 20px;
  transition: filter .3s;
  width: 100%;
  height: 100%;

  @media only screen and (hover: none) {
    padding-inline: 10px;
  }

  &.blur {
    filter: blur(10px);
  }

  .transition-wrapper {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  @include animations.list;
}
</style>
