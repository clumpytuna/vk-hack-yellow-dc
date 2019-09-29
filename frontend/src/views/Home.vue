<template>
  <v-layout column v-if="dialogueId">
    <div class="messages-wrapper">
      <div class="messages hide-scrollbar" ref="messages">
        <div v-for="message of messages" class="message-wrapper">
          <div :class="{'message': true, 'message-question': message.isQuestion, 'message-answer': !message.isQuestion}">{{ message.text }}</div>
        </div>
        <div style="height: 75px; content: '';"></div>
      </div>
    </div>
    <voice-input
      class="input"
      :isLoadingResponse="isLoadingResponse"
      @sendTextMessage="sendTextMessage"
      @sendVoiceMessage="sendVoiceMessage"
      @switchInputMethod="scrollToTop"
    />
  </v-layout>
  <v-layout v-else align-center justify-center>Loading...</v-layout>
</template>

<style scoped>
  .messages-wrapper {
    flex: 1;
    position: relative;
  }

  .input {
    background: white;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
  }

  .messages {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    overflow-y: auto;
  }

  .hide-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  .hide-scrollbar::-webkit-scrollbar {
    display: none;
  }

  .messages::-webkit-scrollbar {
    display: none;
  }

  .message-wrapper {
    margin-top: 10px;
    display: flex;
  }

  .message {
    --radius: 30px;
    padding: 7px 15px;
    display: flex;
    align-content: center;
    white-space: pre-line;
  }

  .message-question {
    margin-left: auto;;
    /*background: var(--v-primary-base);*/
    background: #5100d3;
    color: white;
    border-radius: var(--radius) var(--radius) 0 var(--radius);
  }

  .message-answer {
    /*background: #efeff7;*/
    background: #e9e9e9;
    border-radius: 0 var(--radius) var(--radius) var(--radius);
  }

  .increased-font .message {
    font-size: 24px;
  }
</style>

<script>
  import VoiceInput from '@/components/VoiceInput';
  import axios from 'axios';
  import { baseURL, postForm } from '@/plugins/axios';

  export default {
    name: 'home',
    components: { VoiceInput },
    props: ['increasedFont'],
    watch: {
      async increasedFont(newValue, oldValue) {
        if (newValue === true && oldValue === false) {
          await this.sendTextMessage('xvf', false);
        }
      },
    },
    data() {
      return {
        dialogueId: null,
        messages: [{ text: 'Привет, я голосовой помощник Пушкинского музея Александр', isQuestion: false }],
        isLoadingResponse: false,
      };
    },
    async mounted() {
      const response = await axios.post('/create', null);
      this.dialogueId = response.data.id;
    },
    methods: {
      scrollToTop() {
        this.$refs.messages.scrollTop = this.$refs.messages.scrollHeight;
      },
      async addMessage(text, isQuestion) {
        this.messages.push({ text, isQuestion });
        await this.$nextTick();
        this.scrollToTop();

        const sleep = milliseconds => new Promise(resolve => setTimeout(resolve, milliseconds));
        await sleep(500);
        this.scrollToTop();
      },
      async sendTextMessage(text, callAddMessage = true) {
        if (callAddMessage) {
          this.addMessage(text, true);
        }
        this.isLoadingResponse = true;
        try {
          await postForm('/request_text', { id: this.dialogueId, request: text });
        } catch {
          this.onSendError();
          return;
        }

        await this.requestTextAnswer();
      },
      async sendVoiceMessage(blob) {
        this.isLoadingResponse = true;
        let response;
        try {
          response = await postForm('/request_audio', { id: this.dialogueId, 'speech': blob });
        } catch {
          this.onSendError();
          return;
        }

        const text = response.data.speech;
        this.addMessage(text, true);
        await this.requestTextAnswer();
      },
      async requestTextAnswer() {
        let response;
        try {
          response = await postForm('/response_text', { id: this.dialogueId });
        } catch {
          this.onSendError();
          return;
        }
        this.addMessage(response.data, false);
        this.isLoadingResponse = false;

        await this.requestVoiceAnswer();
      },
      async requestVoiceAnswer() {
        const formData = new FormData();
        formData.append('id', this.dialogueId);
        const requestOptions = { method: 'POST', body: formData };
        const response = await fetch(baseURL + '/response_audio', requestOptions);
        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);
        const audio = new Audio();
        audio.src = url;
        await audio.play();
      },
      onSendError() {
        this.isLoadingResponse = false;
        this.addMessage('Хм. Давайте попробуем по-другому.', false);
      },
    },
  };
</script>
