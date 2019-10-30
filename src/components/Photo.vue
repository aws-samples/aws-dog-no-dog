<template>
  <div id="photo">
    <p class="error" v-if="error">
      <i class="fas fa-sad-tear"></i> {{ error }}
    </p>
    <p id="image" v-if="photo">
      <img :src="photo.url" />
      <span class="stamp" v-if="checkIsDog && isDog">
        <i :class="'fas ' + this.dogIcon"></i>
      </span>
      <span class="stamp" v-if="checkIsDog && !isDog">
        <i class="fas fa-times"></i>
      </span>
      <span v-if="checkIsDog && isDog" class="label">{{ label }}</span>
      <span class="loading" v-if="loading"><i class="fas fa-bone"></i></span>
    </p>
    <div id="actions" v-if="checkIsDog">
      <p @click="cancel"><i class="fas fa-undo"></i></p>
      <p @click.once="hasNoDog" class="has-no-dog" v-if="!sentFeedback">
        <i class="fas fa-times"></i>
      </p>
      <p @click.once="hasDog" class="has-dog" v-if="!sentFeedback">
        <i class="fas fa-dog"></i>
      </p>
    </div>
    <form v-if="!photo">
      <p>
        <label for="photo-select"
          ><i class="fas fa-paw"></i> Pick a picture</label
        >
        <input
          id="photo-select"
          type="file"
          @change="send"
          ref="photo"
          accept="image/png,image/jpeg"
        />
      </p>
    </form>
  </div>
</template>

<script>
import api from "../backend/api.js";

const dogIcons = ["fa-paw", "fa-heart"];

const dogMessages = [
  "Such a cutie!",
  "That's a cute dog!",
  "Such a good dog!",
  "Beautiful!"
];

// Limit the photo size to 2 MB
const photoMaxSize = 2000000;

export default {
  data: function() {
    return {
      error: "",

      photo: null,

      label: "",
      dogIcon: dogIcons[0],

      loading: false,
      checkIsDog: false,
      isDog: false,
      sentFeedback: false
    };
  },
  methods: {
    send() {
      let photo = this.$refs.photo.files[0];
      if (photo.size >= photoMaxSize) {
        this.error = "This photo is too big.";
        return;
      }
      this.photo = {
        url: URL.createObjectURL(photo),
        file: photo
      };

      let fReader = new FileReader();
      let component = this;
      fReader.onload = function() {
        component.checkIsDog = false;
        component.loading = true;
        api
          .sendPhoto(this.result)
          .then(response => {
            component.isDog = response.dog;
            component.checkIsDog = true;
            component.loading = false;

            if (component.isDog) {
              component.label =
                dogMessages[Math.floor(Math.random() * dogMessages.length)];
              component.dogIcon =
                dogIcons[Math.floor(Math.random() * dogIcons.length)];
            }
          })
          .catch(error => {
            component.error = error;
          });
      };
      fReader.readAsBinaryString(photo);
    },
    cancel() {
      this.photo = null;
      this.checkIsDog = false;
      this.sentFeedback = false;
      this.label = "";
    },
    hasDog() {
      let component = this;
      let fReader = new FileReader();
      fReader.onload = function() {
        component.loading = true;
        api
          .feedbackPhoto(this.result, true)
          .then(() => {
            component.sentFeedback = true;
          })
          .catch(error => {
            component.error = error;
          })
          .finally(() => {
            component.loading = false;
          });
      };
      fReader.readAsBinaryString(this.photo.file);
    },
    hasNoDog() {
      let component = this;
      let fReader = new FileReader();
      fReader.onload = function() {
        component.loading = true;
        api
          .feedbackPhoto(this.result, false)
          .then(() => {
            component.sentFeedback = true;
          })
          .catch(error => {
            component.error = error;
          })
          .finally(() => {
            component.loading = false;
          });
      };
      fReader.readAsBinaryString(this.photo.file);
    }
  }
};
</script>

<style lang="less" scoped>
#image {
  position: relative;
  transform: rotate(-3deg);
  margin: 40px auto;
  img {
    margin: 0px auto;
    max-width: 450px;
    max-height: 450px;
    border: 10px solid #fff;
    box-shadow: 0px 0px 5px 0px rgba(75, 118, 121, 1);
  }
  .stamp {
    position: absolute;
    right: 0%;
    bottom: 20%;
    font-size: 96px;
    color: #ffffff;
    text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);

    animation-name: stamp;
    animation-duration: 0.5s;
    opacity: 0;
    animation-fill-mode: forwards;
  }
  .label {
    position: absolute;
    bottom: 20px;
    left: 0px;
    width: 100%;
    font-weight: bold;
    color: #fff;
  }
  .loading {
    position: absolute;
    display: flex;
    justify-content: space-around;
    align-items: center;
    top: 0px;
    width: 100%;
    height: 100%;
    font-size: 100px;
    color: #fff;
    text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);

    i {
      animation-name: loading;
      animation-duration: 1.2s;
      animation-iteration-count: infinite;
      transition-timing-function: cubic-bezier(0.17, 0.67, 83, 0.67);
    }
  }
}
label {
  i {
    display: block;
    font-size: 128px;
    transform: rotate(5deg);
  }
}

input[type="file"] {
  border: 0;
  clip: rect(0, 0, 0, 0);
  height: 1px;
  overflow: hidden;
  padding: 0;
  position: absolute !important;
  white-space: nowrap;
  width: 1px;
}

#actions {
  max-width: 500px;
  margin: 0px auto;
  display: flex;
  justify-content: space-around;
  align-items: center;
  font-size: 64px;

  p {
    margin: 0px;
  }

  .has-no-dog {
    color: #bc4b51;
  }
  .has-dog {
    color: #5b8e7d;
  }
}

@keyframes stamp {
  0% {
    opacity: 0;
  }
  10% {
    opacity: 0.5;
    transform-origin: 50% 50%;
    transform: rotate(-2deg) scale(3);
  }
  100% {
    opacity: 1;
    transform: rotate(10deg) scale(1);
  }
}

@keyframes loading {
  0% {
    transform: scale(0.95);
  }
  5% {
    transform: scale(1.1);
  }
  39% {
    transform: scale(0.85);
  }
  100% {
    transform: scale(0.9);
  }
}
</style>
