<template>
  <div class="flex justify-center items-center min-h-[92vh] bg-gradient-to-br from-gray-50 to-gray-100">
    <div class="flex w-screen max-w-7xl mx-4">
      <!-- Sidebar with Date-based Chat History -->
      <div class="w-80 bg-white rounded-lg shadow-lg overflow-hidden mr-4">
        <div class="p-4">
          <div class="font-semibold text-gray-800 mb-4 text-lg flex items-center">
            <i class="pi pi-comments mr-2"></i>
            Lịch sử trò chuyện
          </div>
          
          <Button 
            @click="startNewChat"
            class="w-full mb-4 p-button-secondary"
            severity="secondary"
          >
            <i class="pi pi-plus-circle mr-2"></i>
            Cuộc trò chuyện mới
          </Button>
          
          <div class="space-y-4">
            <div v-for="(chats, date) in groupedChats" :key="date">
              <div class="text-sm font-medium text-gray-600 mb-2 flex items-center">
                <i class="pi pi-calendar mr-2"></i>
                {{ formatDate(date) }}
              </div>
              <div class="space-y-2">
                <div 
                  v-for="chat in chats" 
                  :key="chat.id"
                  class="group flex items-center justify-between text-gray-800 hover:bg-gray-50 rounded-lg p-3 cursor-pointer text-sm transition-all duration-200"
                  :class="{'bg-blue-50 border border-blue-200': currentChat?.id === chat.id}"
                >
                  <div 
                    class="flex-1 min-w-0 mr-2"
                    @click="loadChat(chat.id)"
                  >
                    <div class="truncate font-medium flex items-center">
                      <i class="pi pi-comments mr-2 text-gray-500"></i>
                      {{ chat.title || 'Cuộc trò chuyện mới' }}
                    </div>
                    <div class="text-xs text-gray-500 flex items-center mt-1">
                      <i class="pi pi-clock mr-1"></i>
                      {{ formatTime(chat.timestamp) }}
                    </div>
                  </div>
                  <Button
                    @click.stop="confirmDeleteChat(chat.id)"
                    class="p-button-text p-button-danger p-button-sm opacity-0 group-hover:opacity-100 transition-all"
                    icon="pi pi-trash"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Chat Area -->
      <div class="flex-1 bg-white rounded-lg shadow-lg overflow-hidden">
        <div class="h-[94.75vh] flex flex-col">
          <div class="p-4 border-b bg-white flex items-center">
            <i class="pi pi-user text-xl text-gray-600 mr-2"></i>
            <span class="font-semibold text-gray-800">
              {{ currentChat?.title || 'Cuộc trò chuyện mới' }}
            </span>
          </div>
          
          <div
            ref="chatMessagesRef"
            class="flex-1 p-6 overflow-y-auto scroll-smooth space-y-4 bg-gradient-to-b from-gray-50 to-white"
          >
            <div
              v-for="(message, index) in currentChat?.messages"
              :key="index"
              class="flex"
              :class="message.isUser ? 'justify-end' : 'justify-start'"
            >
              <div
                :class="[
                  'max-w-[80%] px-5 py-3 rounded-lg shadow-sm',
                  message.isUser
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-100 text-gray-800',
                ]"
              >
                <p class="text-sm md:text-base leading-relaxed">{{ message.content }}</p>
                <span class="text-xs opacity-75 flex items-center mt-1">
                  <i class="pi pi-clock mr-1"></i>
                  {{ formatTime(message.timestamp) }}
                </span>
              </div>
            </div>
          </div>

          <div class="border-t bg-white p-4">
            <form
              @submit.prevent="sendMessage"
              class="flex items-center space-x-3"
            >
              <InputText
                v-model="newMessage"
                placeholder="Nhập tin nhắn của bạn..."
                class="flex-1 rounded-full border-gray-300 focus:ring-blue-500 focus:border-blue-500 py-2 px-4"
                :disabled="loading"
              />
              <Button
                type="submit"
                :disabled="!newMessage.trim() || loading"
                class="p-button-rounded p-button-primary w-12 h-12"
              >
                <i class="pi pi-send"></i>
              </Button>
            </form>
            <div v-if="loading" class="text-sm text-gray-600 mt-2 ml-4 flex items-center">
              <i class="pi pi-spinner pi-spin mr-2"></i>
              Đang trả lời...
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Dialog -->
    <Dialog
      v-model:visible="showDeleteDialog"
      header="Xác nhận xóa"
      :modal="true"
      class="w-[90vw] md:w-[400px] rounded-xl"
    >
      <div class="flex items-center text-gray-700">
        <i class="pi pi-exclamation-triangle text-yellow-500 text-xl mr-3"></i>
        <p class="m-0">
          Bạn có chắc chắn muốn xóa cuộc trò chuyện này không?
        </p>
      </div>
      <template #footer>
        <Button
          label="Hủy"
          icon="pi pi-times"
          @click="showDeleteDialog = false"
          class="p-button-text"
        />
        <Button
          label="Xóa"
          icon="pi pi-trash"
          @click="deleteChat"
          class="p-button-danger"
          severity="danger"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, computed, watch, nextTick, onMounted } from 'vue';

const newMessage = ref('');
const loading = ref(false);
const chatMessagesRef = ref(null);
const chatHistory = ref([]);
const currentChatId = ref(null);
const showDeleteDialog = ref(false);
const chatToDelete = ref(null);

const API_URL = 'http://127.0.0.1:5000/predict';

// Generate unique ID for chats
const generateId = () => `chat_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

// Group chats by date
const groupedChats = computed(() => {
  const groups = {};
  chatHistory.value.forEach(chat => {
    const date = new Date(chat.timestamp).toDateString();
    if (!groups[date]) {
      groups[date] = [];
    }
    groups[date].push(chat);
  });
  
  // Sort dates in descending order
  const sortedGroups = {};
  Object.keys(groups)
    .sort((a, b) => new Date(b) - new Date(a))
    .forEach(key => {
      sortedGroups[key] = groups[key].sort((a, b) => b.timestamp - a.timestamp);
    });
  
  return sortedGroups;
});

// Get current chat
const currentChat = computed(() => 
  chatHistory.value.find(chat => chat.id === currentChatId.value)
);

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  if (date.toDateString() === today.toDateString()) {
    return 'Hôm nay';
  } else if (date.toDateString() === yesterday.toDateString()) {
    return 'Hôm qua';
  } else {
    return date.toLocaleDateString('vi-VN', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
};

const formatTime = (timestamp) => {
  if (!timestamp) return '';
  return new Date(timestamp).toLocaleTimeString('vi-VN', {
    hour: '2-digit',
    minute: '2-digit'
  });
};

const confirmDeleteChat = (chatId) => {
  chatToDelete.value = chatId;
  showDeleteDialog.value = true;
};

const deleteChat = () => {
  const index = chatHistory.value.findIndex(chat => chat.id === chatToDelete.value);
  if (index > -1) {
    chatHistory.value.splice(index, 1);
    if (currentChatId.value === chatToDelete.value) {
      currentChatId.value = chatHistory.value[0]?.id || null;
      if (!currentChatId.value) {
        startNewChat();
      }
    }
  }
  showDeleteDialog.value = false;
  chatToDelete.value = null;
};

const startNewChat = () => {
  const newChat = {
    id: generateId(),
    title: '',
    timestamp: new Date().getTime(),
    messages: [{
      content: 'Xin chào! Tôi có thể giúp gì cho bạn?',
      isUser: false,
      timestamp: new Date().getTime()
    }]
  };
  chatHistory.value.unshift(newChat);
  currentChatId.value = newChat.id;
};

const loadChat = (chatId) => {
  currentChatId.value = chatId;
  nextTick(() => scrollToBottom());
};

const processMessageContent = (content) => {
  // Thay thế @@ bằng dấu . ở cuối câu
  let processedContent = content.replace(/@@/g, '.');
  
  // Thay \n bằng thẻ xuống dòng <br>
  processedContent = processedContent.replace(/\n/g, '<br>');
  
  return processedContent;
};

const sendMessage = async () => {
  if (!newMessage.value.trim() || loading.value || !currentChat.value) return;

  const messageTime = new Date().getTime();
  
  currentChat.value.messages.push({
    content: processMessageContent(newMessage.value),
    isUser: true,
    timestamp: messageTime
  });

  currentChat.value.timestamp = messageTime;

  if (currentChat.value.messages.length === 2 && !currentChat.value.title) {
    currentChat.value.title = newMessage.value.slice(0, 30) + (newMessage.value.length > 30 ? '...' : '');
  }

  const userInput = newMessage.value;
  newMessage.value = '';
  loading.value = true;

  try {
    const response = await axios.post(API_URL, { input: userInput });

    if (response.data.status === 'success') {
      const botResponse = response.data.answer || 'Không thể trả lời câu hỏi này.';
      currentChat.value.messages.push({
        content: processMessageContent(botResponse),
        isUser: false,
        timestamp: new Date().getTime()
      });
    } else {
      throw new Error(response.data.error || 'Unknown error');
    }

    await nextTick();
    scrollToBottom();
  } catch (error) {
    console.error('Error:', error);
    currentChat.value.messages.push({
      content: processMessageContent('Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau.'),
      isUser: false,
      timestamp: new Date().getTime()
    });
  } finally {
    loading.value = false;
  }
};


const scrollToBottom = () => {
  if (chatMessagesRef.value) {
    chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight;
  }
};

// Save to localStorage whenever chat history changes
watch(
  chatHistory,
  (newHistory) => {
    localStorage.setItem('chatHistory', JSON.stringify(newHistory));
  },
  { deep: true }
);

// Initialize on component mount
onMounted(() => {
  const savedHistory = localStorage.getItem('chatHistory');
  if (savedHistory) {
    chatHistory.value = JSON.parse(savedHistory);
    if (chatHistory.value.length > 0) {
      currentChatId.value = chatHistory.value[0].id;
    }
  } else {
    startNewChat();
  }
  nextTick(() => scrollToBottom());
});
</script>

<style scoped>
.scroll-smooth {
  scroll-behavior: smooth;
}

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