<template>
  <div class="input">
    <template v-if="isVoiceMode">
      <div class="voice-wrapper">
        <div style="flex: 1"></div>
        <img
          v-if="!isRecording"
          width="48"
          height="48"
          src="/img/record.png"
          @click="isRecording ? stopRecording() : startRecording()"
        >
        <v-icon
          v-else
          x-large
          color="primary"
          @click="stopRecording"
        >
          mdi-stop
        </v-icon>

        <div style="flex: 1; display: flex; justify-content: center">
          <v-icon v-if="isRecording" medium @click="cancelRecording">mdi-close</v-icon>
          <v-icon v-else large @click="setVoiceMode(false)">mdi-keyboard</v-icon>
        </div>
      </div>
    </template>
    <template v-else>
      <form @submit.prevent="sendTextMessage">
        <v-text-field
          v-model="textInput"
          autofocus
          outlined
          rounded
          hide-details
          dense
          autocomplete="off"
          placeholder="Напишите свой запрос..."
          ref="textInput"
        >
          <template v-slot:append-outer>
            <v-icon v-if="textInput" color="primary" @click="sendTextMessage">mdi-send</v-icon>
            <img
              v-else
              width="24"
              height="24"
              src="/img/record.png"
              @click="setVoiceMode(true)"
            >
          </template>
        </v-text-field>
      </form>
    </template>
  </div>
</template>

<style scoped>
  .input {
    padding: 10px;
    padding-top: 15px;
  }

  .voice-wrapper {
    display: flex;
  }
</style>

<script>
  export default {
    name: 'VoiceInput',
    props: ['isLoadingResponse'],
    data() {
      return {
        isVoiceMode: true,
        // isVoiceMode: false,
        isRecording: false,
        textInput: '',
      };
    },
    methods: {
      async setVoiceMode(value) {
        if (this.isRecording) return;
        this.isVoiceMode = value;
        this.textInput = '';

        await this.$nextTick();
        if (!value) {
          this.$refs.textInput.focus();
        }
        this.$emit('switchInputMethod');
      },
      async initVoice() {
        const constraints = {
          audio: true,
          video: false,
        };
        return await navigator.mediaDevices.getUserMedia(constraints);
      },
      async startRecording() {
        if (this.isRecording || this.isLoadingResponse) return;

        const stream = await this.initVoice();
        this.isRecording = true;

        this.mediaRecorder = new MediaRecorder(stream);
        this.chunks = [];
        this.mediaRecorder.addEventListener('dataavailable', e => this.chunks.push(e.data));
        this.mediaRecorder.onstop = this.processRecord;
        this.mediaRecorder.start();
      },
      stopRecording() {
        this.mediaRecorder.stop();
      },
      cancelRecording() {
        this.isRecording = false;
        this.mediaRecorder.stop();
      },
      async processRecord() {
        if (!this.isRecording) return;
        this.isRecording = false;
        const blob = new Blob(this.chunks);
        this.$emit('sendVoiceMessage', blob);
      },
      async sendTextMessage() {
        if (this.isLoadingResponse) return;
        this.$emit('sendTextMessage', this.textInput);
        this.textInput = '';
      },
    },
  };
</script>

