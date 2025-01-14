<template>
  <div class="flex justify-center items-center min-h-[92vh] bg-gray-100">
    <div class="flex w-screen">
      <!-- Sidebar with Date-based Chat History -->
      <div class="w-64 bg-gray-100 rounded-xl shadow-lg overflow-hidden">
        <div class="p-4">
          <div class="font-medium text-gray-700 mb-3">Lịch sử trò chuyện</div>
          <Button 
            @click="startNewChat"
            class="w-full mb-4 p-button-secondary"
            icon="pi pi-plus"
            label="Cuộc trò chuyện mới"
          />
          
          <div class="space-y-4">
            <div v-for="(chats, date) in groupedChats" :key="date">
              <div class="text-sm font-medium text-gray-600 mb-2">{{ formatDate(date) }}</div>
              <div class="space-y-2">
                <div 
                  v-for="chat in chats" 
                  :key="chat.id"
                  @click="loadChat(chat.id)"
                  class="text-gray-800 hover:bg-gray-200 rounded-lg p-2 cursor-pointer text-sm"
                  :class="{'bg-gray-200': currentChat?.id === chat.id}"
                >
                  <div class="truncate">{{ chat.title || 'Cuộc trò chuyện mới' }}</div>
                  <div class="text-xs text-gray-500">{{ formatTime(chat.timestamp) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Chat Area -->
      <div class="flex-1 bg-white rounded-xl shadow-lg overflow-hidden">
        <div class="h-[94.75vh] flex flex-col">
          <div
            ref="chatMessagesRef"
            class="flex-1 p-4 overflow-y-auto scroll-smooth space-y-4 bg-gray-50"
          >
            <div
              v-for="(message, index) in currentChat?.messages"
              :key="index"
              class="flex"
              :class="message.isUser ? 'justify-end' : 'justify-start'"
            >
              <div
                :class="[
                  'max-w-[80%] px-4 py-2 rounded-lg shadow-sm',
                  message.isUser
                    ? 'bg-[#e8e8e880] text-black'
                    : 'bg-white',
                ]"
              >
                <p class="text-sm md:text-base">{{ message.content }}</p>
                <span class="text-xs text-gray-500">
                  {{ formatTime(message.timestamp) }}
                </span>
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
                placeholder="Nhập tin nhắn..."
                class="flex-1 rounded-full border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                :disabled="loading"
              />
              <Button
                type="submit"
                :disabled="!newMessage.trim() || loading"
                class="p-button-rounded p-button-primary"
                icon="pi pi-send"
              />
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
import { ref, computed, watch, nextTick, onMounted } from 'vue';

const newMessage = ref('');
const loading = ref(false);
const chatMessagesRef = ref(null);
const chatHistory = ref([]);
const currentChatId = ref(null);

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

// Format date to Vietnamese locale
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

const sendMessage = async () => {
  if (!newMessage.value.trim() || loading.value || !currentChat.value) return;

  const messageTime = new Date().getTime();
  
  // Add user message
  currentChat.value.messages.push({
    content: newMessage.value,
    isUser: true,
    timestamp: messageTime
  });

  // Update chat timestamp
  currentChat.value.timestamp = messageTime;

  // Update title if it's the first user message
  if (currentChat.value.messages.length === 2 && !currentChat.value.title) {
    currentChat.value.title = newMessage.value.slice(0, 30) + (newMessage.value.length > 30 ? '...' : '');
  }

  const userInput = newMessage.value;
  newMessage.value = '';
  loading.value = true;

  try {
    const response = await axios.post(API_URL, {
      input: userInput
    });

    if (response.data.status === 'success') {
      const botResponse = response.data.answer || 'Không thể trả lời câu hỏi này.';
      currentChat.value.messages.push({
        content: botResponse,
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
      content: 'Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau.',
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