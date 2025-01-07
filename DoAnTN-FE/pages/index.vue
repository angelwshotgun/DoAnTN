<template>
  <div class="flex justify-center items-center min-h-[92vh] bg-gray-100">
    <div class="flex w-screen">
      <!-- Sidebar -->
      <div class="w-64 bg-gray-100 rounded-xl shadow-lg overflow-hidden">
        <div class="p-4">
          <div v-for="(value, key) in data1" :key="key" class="mb-2">
            <div
              @click="selectContext(key)"
              class="text-gray-800 hover:bg-gray-200 rounded-lg p-2 cursor-pointer"
            >
              {{ key }}
            </div>
          </div>
          <input type="file" @change="uploadFile" class="mt-4" />
        </div>
      </div>

      <!-- Chat -->
      <div class="flex-1 bg-white rounded-xl shadow-lg overflow-hidden">
        <div class="h-[94.75vh] flex flex-col">
          <div
            ref="chatHistory"
            class="flex-1 p-4 overflow-y-auto scroll-smooth space-y-4 bg-gray-50"
          >
            <div
              v-for="(message, index) in messages"
              :key="index"
              class="flex"
              :class="message.isUser ? 'justify-end' : 'justify-start'"
            >
              <div
                :class="[
                  'max-w-[80%] px-4 py-2 rounded-full shadow-sm',
                  message.isUser
                    ? 'bg-[#e8e8e880] text-black rounded'
                    : 'bg-white rounded',
                ]"
              >
                <p class="text-sm md:text-base">{{ message.content }}</p>
              </div>
            </div>
          </div>

          <div class="border-t bg-white p-4">
            <form
              @submit.prevent="sendMessage"
              class="flex items-center space-x-2"
            >
              <InputText
                v-model="newMessage"
                placeholder="Nhập câu hỏi..."
                class="flex-1 rounded-full border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                :disabled="loading || !selectedContext"
              />
              <Button
                type="submit"
                :disabled="!newMessage.trim() || loading || !selectedContext"
                class="p-button-rounded p-button-primary"
                icon="pi pi-send"
              >
              </Button>
            </form>
            <div v-if="loading" class="text-xs text-gray-500 mt-2 ml-4">
              Đang trả lời...
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
const newMessage = ref('');
const loading = ref(false);
const messages = ref([]);
const chatHistory = ref(null);
const selectedContext = ref(null);

const data = ref({});
const data1 = ref({
  'Số: 3981/QĐ-BYT':
    'Hà Nội ngày 30 tháng 12 năm 2024 QUYẾT ĐỊNH Ban hành Kế hoạch Cải cách hành chính năm 2025 của Bộ Y tế Thủ trưởng các đơn vị thuộc và trực thuộc Bộ Y tế; các đơn vị liên quan theo chức năng nhiệm vụ được giao có trách nhiệm tổ chức triển khai thực hiện Kế hoạch Cải cách hành chính năm 2025 của Bộ Y tế Đổi mới hệ thống tổ chức y tế theo hướng tinh giản tổ chức, thu gọn đầu môi, tăng cường phân cấp quản lý nhà nước trong lĩnh vực y tế.',
  'Số: 4561/SGDĐT-VP':
    'Hà Nội ngày 20 tháng 12 năm 2024 Vụ việc nghỉ Tết Dương lịch năm 2025 và Tết Nguyên đán Ất Tỵ năm 2025 của ngành Giáo dục và Đào tạo Hà Nội. Thời gian nghỉ Tết Dương lịch năm 2025: 01 ngày (ngày 01/01/2025, thứ Tư). Thời gian nghỉ Tết Nguyên đán Ất Tỵ năm 2025 09 ngày liên tục, từ thứ Bảy ngày 25/01/2025 đến hết Chủ nhật ngày 02/02/2025.',
});

const sendMessage = async () => {
  if (!newMessage.value.trim() || loading.value || !selectedContext.value) return;

  // Thêm tin nhắn người dùng
  messages.value.push({
    content: newMessage.value,
    isUser: true,
    timestamp: new Date(),
  });

  const userQuestion = newMessage.value;
  newMessage.value = '';
  loading.value = true;

  try {
    const response = await axios.post('http://localhost:5000/predict', {
      question: userQuestion,
      context: data.value[selectedContext.value],
    });

    const botResponse = response.data.answer || 'Không tìm thấy câu trả lời phù hợp.';

    messages.value.push({
      content: botResponse,
      isUser: false,
      timestamp: new Date(),
    });

    await nextTick();
    scrollToBottom();
  } catch (error) {
    console.error('Error:', error);
    messages.value.push({
      content: 'Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau.',
      isUser: false,
      timestamp: new Date(),
    });
  } finally {
    loading.value = false;
  }
};

const selectContext = (key) => {
  selectedContext.value = key;
};

const uploadFile = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    data.value[file.name] = e.target.result;
  };
  reader.readAsText(file);
};

const scrollToBottom = () => {
  if (chatHistory.value) {
    chatHistory.value.scrollTop = chatHistory.value.scrollHeight;
  }
};

watch(
  messages,
  (newMessages) => {
    localStorage.setItem('chatHistory', JSON.stringify(newMessages));
  },
  { deep: true }
);

onMounted(() => {
  const savedMessages = localStorage.getItem('chatHistory');
  if (savedMessages) {
    messages.value = JSON.parse(savedMessages);
  } else {
    messages.value = [{
      content: 'Chào mừng! Vui lòng chọn ngữ cảnh ở thanh bên và đặt câu hỏi.',
      isUser: false,
    }];
  }
  nextTick(() => scrollToBottom());
});
</script>

<style scoped>
.scroll-smooth {
  scroll-behavior: smooth;
}

/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c5c5c5;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
