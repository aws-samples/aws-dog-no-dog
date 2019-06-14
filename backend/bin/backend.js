#!/usr/bin/env node

// @ts-ignore: Cannot find declaration file
require('source-map-support/register');
const cdk = require('@aws-cdk/cdk');
const { BackendStack } = require('../lib/backend-stack');

const app = new cdk.App();
new BackendStack(app, 'BackendStack');
