import axios from "axios";
import { endpoint } from "@/config.js";
import MockAdapter from "axios-mock-adapter";

// Mocking requests
if (process.env.VUE_APP_MOCK == "enabled") {
  let mock = new MockAdapter(axios, { delayResponse: 1000 });
  mock.onPost("/").reply(200, { dog: true });
  mock.onPost("/feedback").reply(200, { message: "Feedback received" });
}
// End of the mock implementation section

export function sendPhoto(photo) {
  return new Promise(function(resolve, reject) {
    axios
      .post(endpoint + "/", {
        photo: btoa(photo)
      })
      .then(response => {
        resolve({
          dog: response.data.dog
        });
      })
      .catch(error => {
        reject(error);
      });
  });
}

export function feedbackPhoto(photo, dog) {
  return new Promise(function(resolve, reject) {
    axios
      .post(endpoint + "/feedback", {
        photo: btoa(photo),
        dog: dog
      })
      .then(() => {
        resolve();
      })
      .catch(error => {
        reject(error);
      });
  });
}

export default {
  sendPhoto,
  feedbackPhoto
};
