<template>
  <div class="layout-wrapper">
    <!-- Nội dung trang -->
    <SharedTopBar />
    <div class="layout-main-container min-h-85vh">
      <div class="layout-main">
        <NuxtPage />
      </div>
    </div>
    <div class="layout-mask animate-fadein" />
    <Toast />
  </div>
</template>

<style scoped>
/* Vùng chứa tổng thể */
.layout-wrapper {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

/* Video nền */
.background-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -1; /* Nằm dưới các nội dung khác */
}

/* Lớp phủ màu tối */
.dark-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.1); /* Độ tối 50% */
  z-index: -1;
}

/* Container chính và các thành phần khác */
.layout-main-container,
.layout-mask,
Toast {
  position: relative;
  z-index: 1; /* Đảm bảo nội dung hiển thị phía trên video */
}
</style>
