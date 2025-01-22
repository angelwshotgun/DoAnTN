<template>
  <div
    class="flex gap-4 items-center px-4 shadow-md bg-white"
    style="height: 64px"
  >
    <img 
      src="~/assets/images/logo2.png"
      class="h-10 w-auto object-contain"
    />
    <Menubar :model="items" class="border-none bg-transparent">
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
            class="px-4 py-2 text-gray-700 hover:text-blue-600 transition-colors duration-200 flex items-center gap-2"
          >
            <span :class="item.icon" />
            <span class="font-medium">{{ item.label }}</span>
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
    route: '/',
  },
  {
    label: 'Đánh Giá Mô Hình',
    route: '/danhgiamohinh',
  },
  {
    label: 'Hướng dẫn sử dụng',
    route: '/huongdan'
  }
]);
</script>

<style scoped>
.p-menubar {
  padding: 0;
}

.p-menubar-root-list {
  gap: 1rem;
}

:deep(.p-menuitem-link) {
  padding: 0.5rem 1rem !important;
}

:deep(.p-menuitem-text) {
  color: #374151;
}

:deep(.p-menuitem-link:hover .p-menuitem-text) {
  color: #2563eb;
}

/* Tạo nền nổi bật và border cho Topbar */
div {
  background-color: #f3f4f6; /* Màu xám nhạt */
  transition: background-color 0.3s ease;
}
</style>
