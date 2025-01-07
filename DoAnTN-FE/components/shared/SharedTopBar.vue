<template>
  <div
    class="flex justify-between items-center px-4 relative"
    style="height: 50px"
  >
    <Menubar :model="items">
      <template #item="{ item, props, hasSubmenu }">
        <NuxtLink
          v-if="item.route"
          v-slot="{ href, navigate }"
          :to="item.route"
        >
          <a
            v-ripple
            :href="href"
            v-bind="props.action"
            target="_blank"
            @click="navigate"
          >
            <span :class="item.icon" />
            <span>{{ item.label }}</span>
          </a>
        </NuxtLink>
      </template>
    </Menubar>
  </div>
</template>

<script setup>
const items = ref([
  {
    label: 'Trang chủ',
    route: '/#',
  },
  {
    label: 'Đánh Giá Mô Hình',
    route: '/#',
  },
]);
</script>

<style>
</style>
