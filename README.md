## Dog no Dog

Dog no Dog is a sample application to showcase how to build a minimum viable product with serverless technologies on AWS.

With the Dog no Dog application, users can submit a picture and the backend should check if there is a dog in it. After this, the user has the possibility to leave a feedback if the picture contains a dog or not.

The standard frontend implementation uses a mock that will always returns that there is a dog in the picture..

This repository is comprised of three branches:

* __master__: The backend only contains helpers (Makefile, boilerplate code for your AWS Lambda functions) and it is up to you to implement the backend.
* __no-boilerplate__: There is nothing for the backend. You will have to implement everything yourself.
* __complete__: A complete implementation of both the frontend and backend for reference.

As this is meant as a challenge and hands-on workshop with limited help, a few hints are available below but you are encouraged to try things by yourself as much as possible.

If you are new to Serverless applications on AWS or are looking for a more guided workshop to learn about Serverless technologies, you should look at the [AWS Serverless Workshops](https://github.com/aws-samples/aws-serverless-workshops).

## Hints

<details>
<summary><strong>
What do I need to build on the backend? <small>(expand to see the answer)</small>
</strong></summary>

There is no formal API definition, but you can find all the API calls made by the frontend in the [api.js file](./src/backend/api.js) in the frontend.

</details>

<details>
<summary><strong>
Where can I configure the API endpoint in the frontend? <small>(expand to see the answer)</small>
</strong></summary>

The API endpoint value is held in the [.env.development](./.env.development) and [.env.production](./.env.production) files.

</details>

<details>
<summary><strong>
How can I deploy the frontend to AWS? <small>(expand to see the answer)</small>
</strong></summary>

You can leverage [AWS Amplify Console](https://aws.amazon.com/amplify/console/) to create a CI/CD pipeline for the frontend.

For this, you will need to initialise the frontend folder as a git repository and push it to a repository service provider supported by AWS Amplify Console.

You can find more details in the [Getting Started](https://docs.aws.amazon.com/amplify/latest/userguide/getting-started.html) section of the documentation.

</details>

## License Summary

This sample code is made available under the MIT-0 license. See the [LICENSE file](./LICENSE).
