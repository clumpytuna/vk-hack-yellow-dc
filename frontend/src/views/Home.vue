<template>
  <v-layout column v-if="dialogueId">
    <div class="messages-wrapper">
      <div class="messages hide-scrollbar" ref="messages">
        <div v-for="message of messages" class="message-wrapper">
          <div
            :class="{'message': true, 'message-question': message.isQuestion, 'message-answer': !message.isQuestion}"
          >
            {{ message.text }}
          </div>
        </div>
      </div>
    </div>
    <voice-input
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
  }

  .message-question {
    margin-left: auto;;
    /*background: var(--v-primary-base);*/
    background: #4a76a8;
    color: white;
    border-radius: var(--radius) var(--radius) 0 var(--radius);
  }

  .message-answer {
    background: #efeff7;
    border-radius: 0 var(--radius) var(--radius) var(--radius);
  }
</style>

<script>
  import VoiceInput from '@/components/VoiceInput';
  import axios from 'axios';
  import { postForm } from '@/plugins/axios';

  export default {
    name: 'home',
    components: { VoiceInput },
    data() {
      return {
        dialogueId: null,
        messages: [{ text: `Как вам помочь?`, isQuestion: false }],
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
      async sendTextMessage(text) {
        this.messages.push({ text, isQuestion: true });
        this.isLoadingResponse = true;
        try {
          await postForm('/request_text', { id: this.dialogueId, request: text });
        } catch {
          this.onSendError();
          return;
        }

        await this.requestAnswer();
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
        this.messages.push({ text, isQuestion: true });
        this.requestAnswer();
      },
      async requestAnswer() {
        const response = await postForm('/response_text', { id: this.dialogueId });
        this.messages.push({ text: response.data, isQuestion: false });
        this.isLoadingResponse = false;
      },
      onSendError() {
        this.isLoadingResponse = false;
        this.messages.push({ text: 'Что-то пошло не так. Пожалуйста, попробуйте ещё раз.', isQuestion: false });
      },
    },
  };
</script>
